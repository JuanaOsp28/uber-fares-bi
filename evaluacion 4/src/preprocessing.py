"""Preprocesamiento del Bank Marketing Dataset.

Todo se construye como Pipeline de scikit-learn: las transformaciones se ajustan
(`fit`) solo con los datos de entrenamiento y luego se aplican a prueba, evitando
fuga de información (data leakage).
"""
import numpy as np
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.compose import ColumnTransformer, make_column_selector
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

MONTHS = ["jan", "feb", "mar", "apr", "may", "jun",
          "jul", "aug", "sep", "oct", "nov", "dec"]


class BankFeatureEngineer(BaseEstimator, TransformerMixin):
    """Ingeniería de características sin estado (no aprende nada de los datos).

    - pdays == -1 significa "no contactado antes": se crea `previously_contacted`
      y pdays pasa a NaN (se imputa después con la mediana de entrenamiento).
    - balance, campaign y previous tienen colas muy largas: se aplica log con signo.
    - month (texto) se convierte a número de mes y a sus componentes cíclicas.
    """

    def fit(self, X, y=None):
        self.columns_out_ = list(self.transform(X.head(5)).columns)
        return self

    def transform(self, X):
        X = X.copy()
        if "pdays" in X:
            X["previously_contacted"] = (X["pdays"] != -1).astype(int)
            X["pdays"] = X["pdays"].where(X["pdays"] != -1, np.nan)
        for col in ["balance", "campaign", "previous"]:
            if col in X:
                X[col] = np.sign(X[col]) * np.log1p(np.abs(X[col]))
        if "month" in X:
            m = X["month"].map({m: i + 1 for i, m in enumerate(MONTHS)})
            X["month_sin"] = np.sin(2 * np.pi * m / 12)
            X["month_cos"] = np.cos(2 * np.pi * m / 12)
            X = X.drop(columns="month")
        return X

    def get_feature_names_out(self, input_features=None):
        return np.array(self.columns_out_)


def build_preprocessor(scale_numeric=True):
    """Devuelve un Pipeline sin ajustar: features -> imputación/escalado/one-hot.

    Numéricas: imputación con mediana (+ estandarización).
    Categóricas: 'unknown' se conserva como categoría propia (puede ser informativa)
    y se aplica One-Hot; las categorías nuevas en prueba se ignoran.
    """
    numeric = [SimpleImputer(strategy="median")]
    if scale_numeric:
        numeric.append(StandardScaler())
    columns = ColumnTransformer([
        ("num", Pipeline([(f"s{i}", s) for i, s in enumerate(numeric)]),
         make_column_selector(dtype_include=np.number)),
        ("cat", OneHotEncoder(handle_unknown="ignore", sparse_output=False),
         make_column_selector(dtype_exclude=np.number)),
    ])
    return Pipeline([("features", BankFeatureEngineer()), ("columns", columns)])


def get_feature_names(fitted_preprocessor):
    """Nombres de columnas de salida de un preprocesador ya ajustado."""
    names = fitted_preprocessor.named_steps["columns"].get_feature_names_out()
    return [n.split("__", 1)[-1] for n in names]
