"""Reglas de limpieza del dataset de tarifas de Uber."""
import pandas as pd

from src.config import NYC_BOUNDS
from src.features import haversine_km

# Tarifa mínima oficial de un viaje en NYC (bajada de bandera) y máximo razonable
MIN_FARE = 2.5
MAX_FARE = 250
MIN_DISTANCE_KM = 0.1
MAX_DISTANCE_KM = 100
MAX_PASSENGERS = 6


def clean_data(df, bounds=NYC_BOUNDS):
    """Aplica las reglas de limpieza en orden.

    Devuelve el DataFrame limpio y una bitácora con los registros eliminados por cada regla.
    """
    log = []

    def apply(rule, mask):
        nonlocal df
        before = len(df)
        df = df[mask]
        log.append({"regla": rule, "eliminados": before - len(df), "restantes": len(df)})

    log.append({"regla": "Registros originales", "eliminados": 0, "restantes": len(df)})
    apply("Valores nulos", df.notna().all(axis=1))
    apply("Claves duplicadas", ~df["key"].duplicated())
    apply(
        f"Tarifa fuera de [{MIN_FARE}, {MAX_FARE}] USD",
        df["fare_amount"].between(MIN_FARE, MAX_FARE),
    )
    apply(
        f"Pasajeros fuera de [1, {MAX_PASSENGERS}]",
        df["passenger_count"].between(1, MAX_PASSENGERS),
    )
    in_bounds = (
        df["pickup_longitude"].between(bounds["lon_min"], bounds["lon_max"])
        & df["pickup_latitude"].between(bounds["lat_min"], bounds["lat_max"])
        & df["dropoff_longitude"].between(bounds["lon_min"], bounds["lon_max"])
        & df["dropoff_latitude"].between(bounds["lat_min"], bounds["lat_max"])
    )
    apply("Coordenadas fuera de NYC", in_bounds)
    distance = haversine_km(
        df["pickup_latitude"], df["pickup_longitude"],
        df["dropoff_latitude"], df["dropoff_longitude"],
    )
    apply(
        f"Distancia fuera de [{MIN_DISTANCE_KM}, {MAX_DISTANCE_KM}] km",
        distance.between(MIN_DISTANCE_KM, MAX_DISTANCE_KM),
    )

    df = df.reset_index(drop=True)
    df["passenger_count"] = df["passenger_count"].astype(int)
    log = pd.DataFrame(log)
    log["pct_eliminado"] = (log["eliminados"] / log.loc[0, "restantes"] * 100).round(2)
    return df, log
