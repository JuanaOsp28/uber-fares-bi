"""Clustering de clientes: métricas, barridos de k, estabilidad, perfiles y relación con y.

Regla de la guía: la variable objetivo NO entra a los algoritmos; solo se usa
después para interpretar los grupos.
"""
import itertools

import numpy as np
import pandas as pd
from scipy.stats import chi2_contingency
from sklearn.cluster import AgglomerativeClustering, KMeans
from sklearn.decomposition import PCA
from sklearn.metrics import (adjusted_rand_score, calinski_harabasz_score,
                             davies_bouldin_score, silhouette_score)
from sklearn.mixture import GaussianMixture

from src import config
from src.preprocessing import build_preprocessor, get_feature_names


def prepare_matrix(X_train, X_other=None, n_components=0.90):
    """Preprocesa (ajustado con train) y reduce con PCA conservando ~90 % de la varianza.

    Se reduce porque con one-hot + numéricas las distancias euclídeas pierden sentido
    en alta dimensión. Devuelve (Z_train, Z_other, prep, pca).
    """
    prep = build_preprocessor().fit(X_train)
    pca = PCA(n_components=n_components, random_state=config.RANDOM_STATE)
    Z_train = pca.fit_transform(prep.transform(X_train))
    Z_other = pca.transform(prep.transform(X_other)) if X_other is not None else None
    return Z_train, Z_other, prep, pca


def clustering_metrics(Z, labels, sample_size=10000):
    """Silhouette (sobre muestra, es O(n²)), Davies-Bouldin y Calinski-Harabasz."""
    labels = np.asarray(labels)
    rng = np.random.RandomState(config.RANDOM_STATE)
    n = len(Z)
    idx = rng.choice(n, size=min(sample_size, n), replace=False)
    return {
        "silhouette": silhouette_score(Z[idx], labels[idx]),
        "davies_bouldin": davies_bouldin_score(Z, labels),
        "calinski_harabasz": calinski_harabasz_score(Z, labels),
    }


def sweep_kmeans(Z, k_values=range(2, 11)):
    """Inercia y métricas de KMeans para distintos k (método del codo + silhouette)."""
    rows = []
    for k in k_values:
        km = KMeans(n_clusters=k, n_init=10, random_state=config.RANDOM_STATE).fit(Z)
        rows.append({"k": k, "inercia": km.inertia_, **clustering_metrics(Z, km.labels_)})
    return pd.DataFrame(rows)


def fit_kmeans(Z, k):
    return KMeans(n_clusters=k, n_init=10, random_state=config.RANDOM_STATE).fit(Z)


def fit_gmm(Z, k, covariance_type="full"):
    """Mezcla gaussiana: asignación suave y clusters elípticos (más flexible que KMeans)."""
    return GaussianMixture(n_components=k, covariance_type=covariance_type,
                           random_state=config.RANDOM_STATE).fit(Z)


def sweep_gmm_bic(Z, k_values=range(2, 9), covariance_types=("full", "diag", "spherical")):
    """Optimización de la mezcla gaussiana: BIC/AIC por k y tipo de covarianza (menor = mejor)."""
    rows = []
    for cov, k in itertools.product(covariance_types, k_values):
        g = fit_gmm(Z, k, cov)
        rows.append({"covarianza": cov, "k": k, "bic": g.bic(Z), "aic": g.aic(Z)})
    return pd.DataFrame(rows)


def fit_agglomerative(Z, k, sample_size=8000, linkage="ward"):
    """Jerárquico sobre una muestra (memoria O(n²)). Devuelve (indices, etiquetas)."""
    rng = np.random.RandomState(config.RANDOM_STATE)
    idx = rng.choice(len(Z), size=min(sample_size, len(Z)), replace=False)
    labels = AgglomerativeClustering(n_clusters=k, linkage=linkage).fit_predict(Z[idx])
    return idx, labels


def compare_linkages(Z, k, sample_size=4000, linkages=("ward", "average", "complete")):
    """Compara criterios de enlace del clustering jerárquico sobre una muestra."""
    rows = {}
    for link in linkages:
        idx, labels = fit_agglomerative(Z, k, sample_size, link)
        sizes = np.bincount(labels) / len(labels)
        rows[link] = {**clustering_metrics(Z[idx], labels), "cluster_mas_grande": sizes.max()}
    return pd.DataFrame(rows).T


def kmeans_stability(Z, k, n_runs=10):
    """Estabilidad: ARI promedio entre ejecuciones de K-Means con distinta semilla (1 = idéntico)."""
    runs = [KMeans(n_clusters=k, n_init=1, random_state=s).fit_predict(Z) for s in range(n_runs)]
    aris = [adjusted_rand_score(a, b) for a, b in itertools.combinations(runs, 2)]
    return {"ari_medio": float(np.mean(aris)), "ari_min": float(np.min(aris))}


def profile_clusters(X, labels):
    """Perfil de cada cluster: media de numéricas y categoría más frecuente de categóricas."""
    df = X.copy().reset_index(drop=True)
    df["cluster"] = np.asarray(labels)
    num = df.select_dtypes(include=np.number).drop(columns="cluster").columns
    cat = df.columns.difference(num).difference(["cluster"])
    numeric_profile = df.groupby("cluster")[list(num)].mean().round(2)
    categorical_profile = df.groupby("cluster")[list(cat)].agg(lambda s: s.mode().iloc[0])
    sizes = df["cluster"].value_counts(normalize=True).sort_index().rename("proporcion")
    return pd.concat([sizes, numeric_profile, categorical_profile], axis=1)


def cluster_vs_target(labels, y):
    """Tasa de aceptación por cluster y prueba chi-cuadrado de independencia."""
    df = pd.DataFrame({"cluster": np.asarray(labels), "y": np.asarray(y)})
    table = df.groupby("cluster")["y"].agg(clientes="size", tasa_aceptacion="mean")
    chi2, p, _, _ = chi2_contingency(pd.crosstab(df["cluster"], df["y"]))
    return table, {"chi2": chi2, "p_valor": p}


__all__ = ["prepare_matrix", "clustering_metrics", "sweep_kmeans", "fit_kmeans", "fit_gmm",
           "sweep_gmm_bic", "fit_agglomerative", "compare_linkages", "kmeans_stability",
           "profile_clusters", "cluster_vs_target", "get_feature_names"]
