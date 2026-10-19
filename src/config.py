"""Rutas y parámetros globales del proyecto."""
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT_DIR / "data"
RAW_DATA_PATH = DATA_DIR / "raw" / "uber.csv"
PROCESSED_DIR = DATA_DIR / "processed"
REPORTS_DIR = ROOT_DIR / "reports"
FIGURES_DIR = REPORTS_DIR / "figures"

# Límites geográficos aproximados del área metropolitana de Nueva York
NYC_BOUNDS = {
    "lon_min": -74.30,
    "lon_max": -73.65,
    "lat_min": 40.45,
    "lat_max": 40.95,
}

# Nivel de significancia para las pruebas de hipótesis
ALPHA = 0.05

# Zona horaria local: pickup_datetime viene en UTC
LOCAL_TZ = "America/New_York"

RANDOM_STATE = 42
