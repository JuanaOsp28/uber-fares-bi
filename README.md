# Análisis de Tarifas de Uber — Proyecto de Business Intelligence

Proyecto integral de BI del curso **Análisis de Datos** (Ingeniería de Sistemas, ITM — 2026-2).
**Equipo 4 — Transporte (Uber).**

## Objetivo

Transformar los datos históricos de viajes de Uber en Nueva York en información útil para la toma de decisiones,
identificando los factores que determinan la tarifa de un viaje (distancia, hora, día, año, número de pasajeros),
validando hipótesis con pruebas estadísticas y comunicando los hallazgos mediante KPIs y un dashboard interactivo.

## Dataset

- **Fuente:** [Uber Fares Dataset — Kaggle](https://www.kaggle.com/datasets/yasserh/uber-fares-dataset)
- **Registros:** ~200.000 viajes (2009–2015), ciudad de Nueva York.
- **Variables:** `key`, `fare_amount`, `pickup_datetime`, `pickup_longitude`, `pickup_latitude`,
  `dropoff_longitude`, `dropoff_latitude`, `passenger_count`.

Instrucciones de descarga en [`data/README.md`](data/README.md).

## Estructura del repositorio

```
uber-fares-bi/
├── data/
│   ├── raw/            # Dataset original (uber.csv) — no se versiona
│   └── processed/      # Datos limpios y tablas del modelo dimensional
├── notebooks/          # Notebooks de cada fase del proyecto
├── src/                # Código reutilizable (carga, limpieza, pruebas, KPIs)
├── docs/               # Documentación de cada fase
├── dashboard/          # Archivo de Power BI y guía de construcción
├── reports/            # Resultados exportados y figuras
├── requirements.txt
└── README.md
```

## Cómo ejecutar

```bash
python -m venv .venv
.venv\Scripts\activate        # Windows  (Linux/Mac: source .venv/bin/activate)
pip install -r requirements.txt
jupyter notebook
```

Ejecutar los notebooks en orden numérico (`01` → `04`).

## Metodología

| Fase | Contenido | Entregable |
|------|-----------|------------|
| 1. Comprensión del problema | Contexto, problema de negocio, preguntas clave, EDA inicial | `docs/01_comprension_problema.md`, `notebooks/01_comprension_problema.ipynb` |
| 2. Formulación de hipótesis | Hipótesis H0/H1, justificación y variables | `docs/02_hipotesis.md` |
| 3. Preparación y modelado | Limpieza, transformación, dimensiones y métricas | `notebooks/02_preparacion_modelado.ipynb` |
| 4. Definición de KPIs | KPIs de negocio y su interpretación | `docs/04_kpis.md`, `notebooks/04_kpis.ipynb` |
| 5. Dashboard | Dashboard en Power BI con dashboard ejecutivo | `dashboard/` |
| 6. Validación y storytelling | Pruebas estadísticas, valor p, narrativa y decisiones | `notebooks/03_pruebas_hipotesis.ipynb`, `docs/05_storytelling.md` |

## Resultados

_Se completará al finalizar las fases de análisis._

## Conclusiones

_Se completará al finalizar las fases de análisis._
