# Fase 3 — Preparación y modelado de datos

Implementación: `src/cleaning.py`, `src/features.py`, `src/modeling.py` y `notebooks/02_preparacion_modelado.ipynb`.

## 1. Limpieza

| # | Regla | Justificación |
|---|-------|---------------|
| 1 | Eliminar registros con nulos | No es posible calcular la distancia sin coordenadas. |
| 2 | Eliminar `key` duplicadas | Cada clave identifica un viaje único. |
| 3 | `fare_amount` entre 2,5 y 250 USD | 2,5 USD es la tarifa mínima en NYC; negativos y extremos son errores. |
| 4 | `passenger_count` entre 1 y 6 | Viajes con 0 o más de 6 pasajeros no son posibles en un vehículo estándar. |
| 5 | Coordenadas dentro del área de NYC | Lon −74,30 a −73,65 y lat 40,45 a 40,95. Elimina puntos en (0, 0) y fuera de la ciudad. |
| 6 | Distancia entre 0,1 y 100 km | Elimina viajes con origen = destino y errores de GPS. |

La cantidad de registros eliminados por cada regla queda en `reports/bitacora_limpieza.csv`.

## 2. Transformación

| Variable nueva | Cálculo |
|----------------|---------|
| `distancia_km` | Fórmula de Haversine entre origen y destino |
| `tarifa_por_km` | `fare_amount / distancia_km` |
| `fecha_local` | `pickup_datetime` sin zona horaria: ya está en hora local de NYC aunque diga "UTC" (ver notebook 01) |
| `anio`, `mes`, `trimestre`, `dia_semana`, `hora` | Extraídos de la fecha local |
| `franja_horaria` | Madrugada (0-5), Mañana (6-11), Tarde (12-17), Noche (18-23) |
| `es_fin_de_semana` | Sábado o domingo |
| `es_hora_pico` | Lunes a viernes, 7-9 h y 16-19 h |
| `categoria_distancia` | 0-2, 2-5, 5-10, 10-20, > 20 km |
| `aeropuerto` / `es_aeropuerto` | Origen o destino a menos de 2 km de JFK, LGA o EWR |

## 3. Selección de variables

- **Se descartan:** `key` (se reemplaza por `id_viaje`) y `pickup_datetime` (se reemplaza por `fecha_local`).
- **Se conservan:** tarifa, pasajeros, coordenadas (para el mapa) y todas las variables derivadas.

## 4. Dimensiones y métricas

**Métricas:** tarifa, distancia, tarifa por km, pasajeros, número de viajes.

**Dimensiones:** tiempo (fecha y hora), tipo de trayecto (categoría de distancia, aeropuerto) y ocupación (pasajeros).

## 5. Modelo estrella (Power BI)

| Tabla | Llave | Contenido |
|-------|-------|-----------|
| `fact_viajes` | `id_viaje` | Un registro por viaje con métricas y atributos de trayecto |
| `dim_fecha` | `id_fecha` (AAAAMMDD) | Año, trimestre, mes, día de la semana, fin de semana |
| `dim_hora` | `hora` (0-23) | Franja horaria, rango pico |

Relaciones: `dim_fecha[id_fecha] 1 → * fact_viajes[id_fecha]` y `dim_hora[hora] 1 → * fact_viajes[hora]`.

Archivos generados en `data/processed/`: `uber_clean.csv`, `fact_viajes.csv`, `dim_fecha.csv`, `dim_hora.csv`.
