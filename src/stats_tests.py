"""Pruebas estadísticas para la validación de hipótesis.

Cada función devuelve un diccionario con el resultado listo para consolidar en una tabla.
Se reporta el tamaño del efecto porque, con ~190.000 registros, diferencias muy pequeñas
resultan estadísticamente significativas sin ser relevantes para el negocio.
"""
import numpy as np
import pandas as pd
from scipy import stats

from src.config import ALPHA, RANDOM_STATE


def _decision(p_value, alpha=ALPHA):
    return "Se rechaza H0" if p_value < alpha else "No se rechaza H0"


def normality_test(series, sample_size=5000):
    """Prueba de normalidad de D'Agostino-Pearson sobre una muestra aleatoria."""
    sample = series.dropna()
    if len(sample) > sample_size:
        sample = sample.sample(sample_size, random_state=RANDOM_STATE)
    stat, p_value = stats.normaltest(sample)
    return {
        "variable": series.name,
        "estadistico": stat,
        "p_valor": p_value,
        "asimetria": stats.skew(sample),
        "es_normal": p_value >= ALPHA,
    }


def spearman_test(x, y, hypothesis):
    """Correlación de Spearman (H1 unilateral: correlación positiva)."""
    rho, p_value = stats.spearmanr(x, y, alternative="greater")
    pearson_r, _ = stats.pearsonr(x, y)
    return {
        "hipotesis": hypothesis,
        "prueba": "Correlación de Spearman",
        "estadistico": rho,
        "p_valor": p_value,
        "efecto": f"rho = {rho:.3f} | Pearson r = {pearson_r:.3f}",
        "decision": _decision(p_value),
    }


def mann_whitney_test(group_a, group_b, hypothesis, labels=("A", "B")):
    """Mann-Whitney U bilateral con correlación biserial por rangos como tamaño del efecto.

    r biserial > 0 indica que el primer grupo tiende a tener valores mayores que el segundo.
    """
    u_stat, p_value = stats.mannwhitneyu(group_a, group_b, alternative="two-sided")
    n1, n2 = len(group_a), len(group_b)
    rank_biserial = 2 * u_stat / (n1 * n2) - 1
    return {
        "hipotesis": hypothesis,
        "prueba": "Mann-Whitney U",
        "estadistico": u_stat,
        "p_valor": p_value,
        "efecto": (
            f"r biserial = {rank_biserial:.3f} | mediana {labels[0]} = {np.median(group_a):.2f}, "
            f"{labels[1]} = {np.median(group_b):.2f}"
        ),
        "decision": _decision(p_value),
    }


def kruskal_test(df, value_col, group_col, hypothesis):
    """Kruskal-Wallis con épsilon cuadrado como tamaño del efecto."""
    groups = [g[value_col].values for _, g in df.groupby(group_col)]
    h_stat, p_value = stats.kruskal(*groups)
    n, k = len(df), len(groups)
    epsilon_sq = (h_stat - k + 1) / (n - k)
    return {
        "hipotesis": hypothesis,
        "prueba": "Kruskal-Wallis",
        "estadistico": h_stat,
        "p_valor": p_value,
        "efecto": f"épsilon² = {epsilon_sq:.4f} | {k} grupos",
        "decision": _decision(p_value),
    }


def chi_square_test(df, col_a, col_b, hypothesis):
    """Chi-cuadrado de independencia con V de Cramér como tamaño del efecto."""
    table = pd.crosstab(df[col_a], df[col_b])
    chi2, p_value, dof, _ = stats.chi2_contingency(table)
    cramers_v = np.sqrt(chi2 / (table.values.sum() * (min(table.shape) - 1)))
    return {
        "hipotesis": hypothesis,
        "prueba": "Chi-cuadrado de independencia",
        "estadistico": chi2,
        "p_valor": p_value,
        "efecto": f"V de Cramér = {cramers_v:.3f} | gl = {dof}",
        "decision": _decision(p_value),
    }


def linear_fare_model(distance, fare):
    """Regresión lineal simple tarifa ~ distancia: tarifa base (intercepto) y costo por km (pendiente)."""
    result = stats.linregress(distance, fare)
    return {
        "tarifa_base": result.intercept,
        "costo_por_km": result.slope,
        "r_cuadrado": result.rvalue ** 2,
        "p_valor": result.pvalue,
    }

