"""Descarga y carga del Bank Marketing Dataset, y partición train/test compartida."""
import io
import urllib.request
import zipfile

import pandas as pd
from sklearn.model_selection import train_test_split

from src import config


def download_dataset():
    """Descarga el dataset desde UCI y deja bank-full.csv en data/raw/."""
    config.RAW_DIR.mkdir(parents=True, exist_ok=True)
    print(f"Descargando {config.UCI_URL} ...")
    with urllib.request.urlopen(config.UCI_URL) as response:
        outer = zipfile.ZipFile(io.BytesIO(response.read()))
    # El zip de UCI contiene zips anidados (bank.zip y bank-additional.zip).
    # Se omiten las carpetas __MACOSX (metadatos de macOS, no son datos).
    for name in outer.namelist():
        if name.startswith("__MACOSX"):
            continue
        if name.endswith(".zip"):
            inner = zipfile.ZipFile(io.BytesIO(outer.read(name)))
            members = [m for m in inner.namelist() if not m.startswith("__MACOSX")]
            inner.extractall(config.RAW_DIR, members=members)
        else:
            outer.extract(name, config.RAW_DIR)
    print("Listo. Archivos en", config.RAW_DIR)


def load_data():
    """Carga el CSV completo (separador ';'). Si no existe, intenta descargarlo."""
    if not config.DATA_FILE.exists():
        download_dataset()
    return pd.read_csv(config.DATA_FILE, sep=";")


def split_xy(df):
    """Separa X (sin la objetivo ni columnas con fuga) e y binaria (1 = yes)."""
    y = (df[config.TARGET] == "yes").astype(int)
    X = df.drop(columns=[config.TARGET] + config.LEAKAGE_COLUMNS, errors="ignore")
    return X, y


def get_train_test():
    """Partición estratificada 80/20 igual para todo el equipo (semilla fija)."""
    X, y = split_xy(load_data())
    return train_test_split(
        X, y, test_size=config.TEST_SIZE, stratify=y, random_state=config.RANDOM_STATE
    )
