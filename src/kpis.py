"""Cálculo de los KPIs del proyecto (los mismos que se implementan como medidas DAX en Power BI)."""
import pandas as pd

KPI_INFO = {
    "ingreso_total": ("Ingreso total", "USD"),
    "total_viajes": ("Total de viajes", "viajes"),
    "tarifa_promedio": ("Tarifa promedio por viaje", "USD"),
    "tarifa_por_km": ("Tarifa por km", "USD/km"),
    "distancia_promedio": ("Distancia promedio por viaje", "km"),
    "pct_hora_pico": ("% de viajes en hora pico", "%"),
    "ocupacion_promedio": ("Ocupación promedio", "pasajeros/viaje"),
    "pct_ingreso_aeropuerto": ("% de ingresos de aeropuertos", "%"),
}


def compute_kpis(df):
    """KPIs globales sobre un conjunto de viajes."""
    ingreso = df["fare_amount"].sum()
    return {
        "ingreso_total": ingreso,
        "total_viajes": len(df),
        "tarifa_promedio": df["fare_amount"].mean(),
        # Promedio ponderado: ingresos totales sobre kilómetros totales
        "tarifa_por_km": ingreso / df["distancia_km"].sum(),
        "distancia_promedio": df["distancia_km"].mean(),
        "pct_hora_pico": df["es_hora_pico"].mean() * 100,
        "ocupacion_promedio": df["passenger_count"].mean(),
        "pct_ingreso_aeropuerto": df.loc[df["es_aeropuerto"], "fare_amount"].sum() / ingreso * 100,
    }


def kpi_table(df):
    """Tabla legible con nombre, valor y unidad de cada KPI."""
    values = compute_kpis(df)
    rows = [
        {"kpi": KPI_INFO[k][0], "valor": round(v, 2), "unidad": KPI_INFO[k][1]}
        for k, v in values.items()
    ]
    return pd.DataFrame(rows)


def kpis_by(df, column):
    """KPIs desagregados por una dimensión (año, franja horaria, etc.)."""
    return pd.DataFrame(
        {name: compute_kpis(group) for name, group in df.groupby(column, observed=True)}
    ).T


def yoy_growth(df, value_col="fare_amount", year_col="anio"):
    """Variación porcentual interanual de la tarifa promedio."""
    by_year = df.groupby(year_col)[value_col].mean().to_frame("tarifa_promedio")
    by_year["variacion_pct"] = by_year["tarifa_promedio"].pct_change() * 100
    return by_year
