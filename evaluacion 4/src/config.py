"""Configuración central del proyecto (rutas, semilla y columnas especiales).

Todos los notebooks y módulos importan de aquí para que el equipo trabaje
con exactamente la misma partición de datos y las mismas rutas.
"""
import os
from pathlib import Path

RANDOM_STATE = 42
TEST_SIZE = 0.2

# Rutas
ROOT = Path(__file__).resolve().parents[1]
RAW_DIR = ROOT / "data" / "raw"
FIGURES_DIR = ROOT / "reports" / "figures"
RESULTS_DIR = ROOT / "reports" / "results"

# Archivo principal del Bank Marketing Dataset (UCI, id 222).
# Se puede sobreescribir con la variable de entorno BANK_DATA_PATH.
DATA_FILE = Path(os.environ.get("BANK_DATA_PATH", RAW_DIR / "bank-full.csv"))
UCI_URL = "https://archive.ics.uci.edu/static/public/222/bank+marketing.zip"

# Variable objetivo: ¿el cliente suscribió el depósito a plazo? (yes/no)
TARGET = "y"

# 'duration' (duración de la llamada) solo se conoce DESPUÉS de la llamada,
# por lo que usarla para predecir sería fuga de información (data leakage).
# La documentación del dataset recomienda excluirla en un modelo realista.
LEAKAGE_COLUMNS = ["duration"]
