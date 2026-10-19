"""Variables derivadas: distancia, atributos de tiempo y tipo de viaje."""
import numpy as np
import pandas as pd

EARTH_RADIUS_KM = 6371.0

# Coordenadas de los aeropuertos de Nueva York (lat, lon)
AIRPORTS = {
    "JFK": (40.6413, -73.7781),
    "LGA": (40.7769, -73.8740),
    "EWR": (40.6895, -74.1745),
}
AIRPORT_RADIUS_KM = 2.0

DIAS_SEMANA = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
MESES = [
    "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
    "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre",
]


def haversine_km(lat1, lon1, lat2, lon2):
    """Distancia en línea recta (km) entre dos puntos sobre la superficie terrestre."""
    lat1, lon1, lat2, lon2 = map(np.radians, [lat1, lon1, lat2, lon2])
    a = (
        np.sin((lat2 - lat1) / 2) ** 2
        + np.cos(lat1) * np.cos(lat2) * np.sin((lon2 - lon1) / 2) ** 2
    )
    return 2 * EARTH_RADIUS_KM * np.arcsin(np.sqrt(a))


def franja_horaria(hora):
    """Madrugada (0-5), Mañana (6-11), Tarde (12-17), Noche (18-23)."""
    return pd.cut(
        hora,
        bins=[-1, 5, 11, 17, 23],
        labels=["Madrugada", "Mañana", "Tarde", "Noche"],
    )


def add_time_features(df):
    """Deriva atributos de calendario de la fecha de recogida (hora local de Nueva York)."""
    df = df.copy()
    local = df["pickup_datetime"]
    df["fecha_local"] = local
    df["fecha"] = local.dt.normalize()
    df["anio"] = local.dt.year
    df["mes"] = local.dt.month
    df["trimestre"] = local.dt.quarter
    df["dia_semana_num"] = local.dt.dayofweek
    df["dia_semana"] = df["dia_semana_num"].map(dict(enumerate(DIAS_SEMANA)))
    df["hora"] = local.dt.hour
    df["franja_horaria"] = franja_horaria(df["hora"]).astype(str)
    df["es_fin_de_semana"] = df["dia_semana_num"] >= 5
    # Hora pico: días hábiles de 7 a 9 a.m. y de 4 a 7 p.m.
    df["es_hora_pico"] = (~df["es_fin_de_semana"]) & (
        df["hora"].between(7, 9) | df["hora"].between(16, 19)
    )
    return df


def add_distance_features(df):
    """Distancia del viaje, tarifa por km, categoría de distancia y viajes de aeropuerto."""
    df = df.copy()
    df["distancia_km"] = haversine_km(
        df["pickup_latitude"], df["pickup_longitude"],
        df["dropoff_latitude"], df["dropoff_longitude"],
    )
    df["tarifa_por_km"] = df["fare_amount"] / df["distancia_km"]
    df["categoria_distancia"] = pd.cut(
        df["distancia_km"],
        bins=[0, 2, 5, 10, 20, np.inf],
        labels=["0-2 km", "2-5 km", "5-10 km", "10-20 km", "> 20 km"],
    ).astype(str)

    df["aeropuerto"] = "Ninguno"
    for code, (lat, lon) in AIRPORTS.items():
        near_pickup = haversine_km(df["pickup_latitude"], df["pickup_longitude"], lat, lon)
        near_dropoff = haversine_km(df["dropoff_latitude"], df["dropoff_longitude"], lat, lon)
        mask = (near_pickup <= AIRPORT_RADIUS_KM) | (near_dropoff <= AIRPORT_RADIUS_KM)
        df.loc[mask, "aeropuerto"] = code
    df["es_aeropuerto"] = df["aeropuerto"] != "Ninguno"
    return df


def build_features(df):
    return add_distance_features(add_time_features(df))
