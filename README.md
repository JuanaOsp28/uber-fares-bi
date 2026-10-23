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

### Calidad de datos
De 200.000 registros originales se conservaron **191.776 (95,9 %)** tras aplicar las reglas de limpieza
(detalle en `reports/bitacora_limpieza.csv`). Se identificó además que `pickup_datetime`, aunque dice "UTC",
ya está en hora local de Nueva York, por lo que no se convierte (ver `notebooks/01_comprension_problema.ipynb`).

### KPIs principales

| KPI | Valor |
|-----|-------|
| Ingreso total | 2.166.790,70 USD |
| Total de viajes | 191.776 |
| Tarifa promedio por viaje | 11,30 USD |
| Tarifa por km | 3,36 USD/km |
| Distancia promedio | 3,37 km |
| % de viajes en hora pico | 26,5 % |
| Ocupación promedio | 1,69 pasajeros/viaje |
| % de ingresos de aeropuertos | 18,4 % |

### Validación de hipótesis (α = 0,05)

| Hipótesis | Prueba | Valor p | Tamaño del efecto | Decisión |
|-----------|--------|---------|-------------------|----------|
| H1 — A mayor distancia, mayor tarifa | Spearman | < 0,001 | rho = 0,867 | Se rechaza H0 |
| H2 — La tarifa por km difiere en hora pico | Mann-Whitney U | < 0,001 | r = 0,111 | Se rechaza H0 |
| H3 — La tarifa difiere en fin de semana | Mann-Whitney U | 0,149 | r = 0,004 | No se rechaza H0 |
| H4 — La tarifa por km cambia entre años | Kruskal-Wallis | < 0,001 | ε² = 0,043 | Se rechaza H0 |
| H5 — La tarifa difiere según pasajeros | Kruskal-Wallis | < 0,001 | ε² = 0,0009 (despreciable) | Se rechaza H0 |
| H6 — La distancia depende de la franja horaria | Chi-cuadrado | < 0,001 | V = 0,076 (despreciable) | Se rechaza H0 |

### Dashboard
El dashboard de Power BI (`dashboard/uber_fares_dashboard.pbix`) incluye un dashboard ejecutivo con los KPIs
principales y tres páginas de análisis (temporal, trayectos e hipótesis) con segmentadores por año, franja horaria
y tipo de trayecto.

## Conclusiones

1. **Distancia:** es el principal determinante del precio. Explica el 81 % de la variación de la tarifa, con una
   tarifa base de 3,38 USD y 2,35 USD por km adicional.
2. **Hora pico:** cada km cuesta un 8 % más en hora pico (4,03 vs. 3,73 USD) por la congestión, aunque el valor
   total del viaje no cambia porque los trayectos son más cortos.
3. **Evolución anual:** el ajuste tarifario de septiembre de 2012 elevó la tarifa por km un 19 % (3,52 → 4,20 USD)
   y la tarifa promedio un 13,2 % en 2013. El fin de semana no afecta la tarifa.
4. **Pasajeros:** no influyen en la práctica en la tarifa, y el 69 % de los viajes lleva un solo pasajero, lo que
   abre la oportunidad de viajes compartidos.
5. **Aeropuertos:** con el 5,5 % de los viajes generan el 18,4 % de los ingresos, y su peso crece cada año.
6. **Decisiones recomendadas:** precio estimado antes del viaje, incentivos a conductores en hora pico, viajes
   compartidos y mayor presencia en aeropuertos. Detalle en `docs/05_storytelling.md`.
7. **Limitaciones:** distancia en línea recta, ausencia de variables de contexto (duración, clima, propinas) y periodo
   histórico 2009–2015 con 2015 incompleto.

## Video

Video explicativo del proyecto: [ver `Actividad 3.mp4`](./Actividad%203.mp4).
