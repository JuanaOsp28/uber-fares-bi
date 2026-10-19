"""Carga del dataset original y resumen de calidad de datos."""
import pandas as pd

from src.config import RAW_DATA_PATH

RAW_COLUMNS = [
    "key",
    "fare_amount",
    "pickup_datetime",
    "pickup_longitude",
    "pickup_latitude",
    "dropoff_longitude",
    "dropoff_latitude",
    "passenger_count",
]


def load_raw_data(path=RAW_DATA_PATH):
    """Lee uber.csv, descarta la columna índice sin nombre y convierte la fecha.

    Aunque pickup_datetime trae el sufijo "UTC", la distribución horaria corresponde a la hora
    local de Nueva York (mínimo a las 5 h, pico a las 19 h, caída a las 16 h por el cambio de turno
    de los taxis), por lo que se conserva la hora registrada sin conversión de zona horaria.
    """
    if not path.exists():
        raise FileNotFoundError(
            f"No se encontró {path}. Descarga el dataset siguiendo data/README.md"
        )
    df = pd.read_csv(path)
    df = df.drop(columns=[c for c in df.columns if c.startswith("Unnamed")])
    df["pickup_datetime"] = pd.to_datetime(
        df["pickup_datetime"], utc=True, errors="coerce"
    ).dt.tz_localize(None)
    return df[RAW_COLUMNS]


def quality_report(df):
    """Tabla por columna con tipo, nulos, valores únicos, mínimo y máximo."""
    numeric = df.select_dtypes("number")
    report = pd.DataFrame(
        {
            "tipo": df.dtypes.astype(str),
            "nulos": df.isna().sum(),
            "pct_nulos": (df.isna().mean() * 100).round(3),
            "unicos": df.nunique(),
        }
    )
    report["minimo"] = numeric.min()
    report["maximo"] = numeric.max()
    return report


def anomaly_summary(df, bounds):
    """Cuenta los registros con valores fuera de rango lógico."""
    coords_out = ~(
        df["pickup_longitude"].between(bounds["lon_min"], bounds["lon_max"])
        & df["pickup_latitude"].between(bounds["lat_min"], bounds["lat_max"])
        & df["dropoff_longitude"].between(bounds["lon_min"], bounds["lon_max"])
        & df["dropoff_latitude"].between(bounds["lat_min"], bounds["lat_max"])
    )
    checks = {
        "Tarifa <= 0": (df["fare_amount"] <= 0).sum(),
        "Tarifa > 250 USD": (df["fare_amount"] > 250).sum(),
        "Pasajeros = 0": (df["passenger_count"] == 0).sum(),
        "Pasajeros > 6": (df["passenger_count"] > 6).sum(),
        "Coordenadas fuera de NYC": coords_out.sum(),
        "Origen igual a destino": (
            (df["pickup_longitude"] == df["dropoff_longitude"])
            & (df["pickup_latitude"] == df["dropoff_latitude"])
        ).sum(),
        "Registros duplicados (key)": df["key"].duplicated().sum(),
    }
    summary = pd.Series(checks, name="registros").to_frame()
    summary["pct"] = (summary["registros"] / len(df) * 100).round(2)
    return summary
