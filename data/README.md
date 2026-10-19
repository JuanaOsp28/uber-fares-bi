# Datos

## Fuente

**Uber Fares Dataset** — Kaggle: <https://www.kaggle.com/datasets/yasserh/uber-fares-dataset>

## Descarga

1. Iniciar sesión en Kaggle y descargar el dataset (botón *Download*).
2. Descomprimir el archivo y copiar `uber.csv` en `data/raw/uber.csv`.

Alternativa con la CLI de Kaggle:

```bash
kaggle datasets download -d yasserh/uber-fares-dataset -p data/raw --unzip
```

## Diccionario de datos

| Columna | Tipo | Descripción |
|---------|------|-------------|
| `key` | texto | Identificador único del viaje |
| `fare_amount` | decimal | Tarifa del viaje en dólares (USD) |
| `pickup_datetime` | fecha-hora | Fecha y hora de inicio del viaje (dice "UTC" pero está en hora local de NYC, ver notebook 01) |
| `pickup_longitude` | decimal | Longitud del punto de recogida |
| `pickup_latitude` | decimal | Latitud del punto de recogida |
| `dropoff_longitude` | decimal | Longitud del punto de destino |
| `dropoff_latitude` | decimal | Latitud del punto de destino |
| `passenger_count` | entero | Número de pasajeros |

## Carpetas

- `raw/`: dataset original sin modificar (no se versiona por tamaño).
- `processed/`: datos limpios y tablas del modelo dimensional generadas por `notebooks/02_preparacion_modelado.ipynb`.
