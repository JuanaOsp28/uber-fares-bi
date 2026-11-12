"""Modelos supervisados, selección de variables, optimización y métricas para predecir y."""
import time
from functools import partial

import pandas as pd
from scipy.stats import loguniform
from sklearn.decomposition import PCA
from sklearn.ensemble import HistGradientBoostingClassifier, RandomForestClassifier
from sklearn.feature_selection import SelectFromModel, SelectKBest, mutual_info_classif
from sklearn.inspection import permutation_importance
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (average_precision_score, confusion_matrix, f1_score,
                             precision_recall_curve, precision_score, recall_score,
                             roc_auc_score)
from sklearn.model_selection import RandomizedSearchCV, StratifiedKFold, cross_validate
from sklearn.pipeline import Pipeline

from src import config
from src.preprocessing import build_preprocessor

SCORING = ["precision", "recall", "f1", "roc_auc", "average_precision"]


def get_models():
    """Tres modelos de familias distintas; todos manejan el desbalance con pesos de clase."""
    rs = config.RANDOM_STATE
    return {
        "Regresión logística": LogisticRegression(
            max_iter=1000, class_weight="balanced", random_state=rs),
        "Random Forest": RandomForestClassifier(
            n_estimators=300, min_samples_leaf=5, class_weight="balanced_subsample",
            n_jobs=-1, random_state=rs),
        "Gradient Boosting": HistGradientBoostingClassifier(
            class_weight="balanced", random_state=rs),
    }


def get_selectors():
    """Estrategias de selección/reducción de variables (se aplican DESPUÉS del preprocesamiento).

    Cada selector vive dentro del Pipeline, así que se ajusta solo con los datos de
    entrenamiento de cada fold (sin fuga de información).
    """
    rs = config.RANDOM_STATE
    return {
        "Sin selección": None,
        "Información mutua (k=20)": SelectKBest(
            partial(mutual_info_classif, random_state=rs), k=20),
        "L1 (SelectFromModel)": SelectFromModel(LogisticRegression(
            penalty="l1", solver="liblinear", C=0.05, class_weight="balanced",
            random_state=rs)),
        "PCA (95 % varianza)": PCA(n_components=0.95, random_state=rs),
    }


def make_pipeline(model, selector=None):
    """Preprocesador [+ selector] + modelo; todo se ajusta solo con entrenamiento."""
    steps = [("prep", build_preprocessor())]
    if selector is not None:
        steps.append(("select", selector))
    steps.append(("model", model))
    return Pipeline(steps)


def _skf(cv):
    return StratifiedKFold(n_splits=cv, shuffle=True, random_state=config.RANDOM_STATE)


def cross_validate_models(models, X_train, y_train, cv=5):
    """Validación cruzada estratificada (solo sobre el conjunto de entrenamiento)."""
    rows = {}
    for name, model in models.items():
        res = cross_validate(make_pipeline(model), X_train, y_train, cv=_skf(cv), scoring=SCORING)
        rows[name] = {m: res[f"test_{m}"].mean() for m in SCORING}
    return pd.DataFrame(rows).T.rename(columns={"average_precision": "pr_auc"})


def compare_selectors(models, selectors, X_train, y_train, cv=5):
    """Compara estrategias de selección de variables por modelo con validación cruzada."""
    rows = {}
    for m_name, model in models.items():
        for s_name, selector in selectors.items():
            res = cross_validate(make_pipeline(model, selector), X_train, y_train,
                                 cv=_skf(cv), scoring=SCORING)
            rows[(m_name, s_name)] = {m: res[f"test_{m}"].mean() for m in SCORING}
    out = pd.DataFrame(rows).T.rename(columns={"average_precision": "pr_auc"})
    out.index.names = ["modelo", "selección"]
    return out


def get_param_distributions():
    """Espacios de búsqueda para la optimización de hiperparámetros."""
    return {
        "Regresión logística": {"model__C": loguniform(1e-3, 1e2)},
        "Random Forest": {
            "model__max_depth": [6, 10, 15, None],
            "model__min_samples_leaf": [1, 3, 5, 10, 20],
            "model__max_features": ["sqrt", 0.3, 0.5],
        },
        "Gradient Boosting": {
            "model__learning_rate": loguniform(0.02, 0.3),
            "model__max_leaf_nodes": [15, 31, 63],
            "model__min_samples_leaf": [20, 50, 100],
            "model__l2_regularization": loguniform(1e-3, 10),
        },
    }


def tune_model(name, model, X_train, y_train, selector=None, n_iter=15, cv=3,
               scoring="average_precision"):
    """Búsqueda aleatoria de hiperparámetros con CV estratificada. Optimiza PR-AUC por defecto
    (la métrica más informativa con clases desbalanceadas). Devuelve (búsqueda, segundos)."""
    search = RandomizedSearchCV(
        make_pipeline(model, selector), get_param_distributions()[name], n_iter=n_iter,
        scoring=scoring, cv=_skf(cv), random_state=config.RANDOM_STATE, n_jobs=-1)
    t0 = time.perf_counter()
    search.fit(X_train, y_train)
    return search, time.perf_counter() - t0


def evaluate(pipeline, X_test, y_test, threshold=0.5):
    """Métricas en prueba con un umbral dado. Devuelve (dict de métricas, matriz de confusión)."""
    proba = pipeline.predict_proba(X_test)[:, 1]
    pred = (proba >= threshold).astype(int)
    metrics = {
        "precision": precision_score(y_test, pred, zero_division=0),
        "recall": recall_score(y_test, pred),
        "f1": f1_score(y_test, pred),
        "roc_auc": roc_auc_score(y_test, proba),
        "pr_auc": average_precision_score(y_test, proba),
    }
    return metrics, confusion_matrix(y_test, pred)


def best_f1_threshold(y_true, proba):
    """Umbral que maximiza F1. IMPORTANTE: calcularlo con validación, no con prueba."""
    precision, recall, thresholds = precision_recall_curve(y_true, proba)
    f1 = 2 * precision[:-1] * recall[:-1] / (precision[:-1] + recall[:-1] + 1e-12)
    return thresholds[f1.argmax()]


def permutation_importances(pipeline, X_test, y_test, n_repeats=5):
    """Importancia por permutación sobre las variables originales (antes del one-hot)."""
    result = permutation_importance(
        pipeline, X_test, y_test, scoring="roc_auc", n_repeats=n_repeats,
        random_state=config.RANDOM_STATE, n_jobs=-1)
    return (pd.DataFrame({"variable": X_test.columns, "importancia": result.importances_mean})
            .sort_values("importancia", ascending=False).reset_index(drop=True))
