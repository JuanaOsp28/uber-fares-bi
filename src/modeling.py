"""Construcción del modelo dimensional (esquema estrella) para Power BI."""
import pandas as pd

from src.features import DIAS_SEMANA, MESES, franja_horaria

FACT_COLUMNS = [
    "id_viaje", "id_fecha", "hora", "fecha_local",
    "fare_amount", "distancia_km", "tarifa_por_km", "passenger_count",
    "categoria_distancia", "aeropuerto", "es_aeropuerto", "es_hora_pico",
    "pickup_latitude", "pickup_longitude", "dropoff_latitude", "dropoff_longitude",
]


def build_dim_fecha(df):
    fechas = pd.date_range(df["fecha"].min(), df["fecha"].max(), freq="D")
    dim = pd.DataFrame({"fecha": fechas})
    dim["id_fecha"] = dim["fecha"].dt.strftime("%Y%m%d").astype(int)
    dim["anio"] = dim["fecha"].dt.year
    dim["trimestre"] = dim["fecha"].dt.quarter
    dim["mes"] = dim["fecha"].dt.month
    dim["nombre_mes"] = dim["mes"].map(lambda m: MESES[m - 1])
    dim["anio_mes"] = dim["fecha"].dt.strftime("%Y-%m")
    dim["dia_semana_num"] = dim["fecha"].dt.dayofweek + 1
    dim["dia_semana"] = dim["fecha"].dt.dayofweek.map(dict(enumerate(DIAS_SEMANA)))
    dim["es_fin_de_semana"] = dim["dia_semana_num"] >= 6
    return dim[[
        "id_fecha", "fecha", "anio", "trimestre", "mes", "nombre_mes",
        "anio_mes", "dia_semana_num", "dia_semana", "es_fin_de_semana",
    ]]


def build_dim_hora():
    dim = pd.DataFrame({"hora": range(24)})
    dim["franja_horaria"] = franja_horaria(dim["hora"]).astype(str)
    dim["hora_texto"] = dim["hora"].map(lambda h: f"{h:02d}:00")
    dim["es_rango_pico"] = dim["hora"].between(7, 9) | dim["hora"].between(16, 19)
    return dim


def build_fact_viajes(df):
    fact = df.copy()
    fact["id_viaje"] = range(1, len(fact) + 1)
    fact["id_fecha"] = fact["fecha"].dt.strftime("%Y%m%d").astype(int)
    return fact[FACT_COLUMNS]


def build_star_schema(df):
    """Devuelve las tablas del modelo: hechos de viajes, dimensión fecha y dimensión hora."""
    return {
        "fact_viajes": build_fact_viajes(df),
        "dim_fecha": build_dim_fecha(df),
        "dim_hora": build_dim_hora(),
    }
