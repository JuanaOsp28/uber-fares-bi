# Fase 4 — Definición de KPIs

Cálculo en Python: `src/kpis.py` y `notebooks/04_kpis.ipynb`. Implementación en Power BI: `dashboard/medidas_dax.md`.

| # | KPI | Fórmula | Justificación de negocio | Hipótesis relacionada |
|---|-----|---------|--------------------------|-----------------------|
| 1 | **Ingreso total** | Σ `fare_amount` | Mide el volumen económico generado; es el indicador principal para la dirección. | Todas |
| 2 | **Tarifa promedio por viaje** (ticket promedio) | Σ tarifa / N° viajes | Indica cuánto paga en promedio un usuario por viaje; sirve para comparar periodos y segmentos. | H3, H4, H5 |
| 3 | **Tarifa por km** | Σ tarifa / Σ distancia | Mide la rentabilidad por unidad de distancia, independiente de la longitud del viaje. | H1, H2, H4 |
| 4 | **Distancia promedio por viaje** | Σ distancia / N° viajes | Describe el tipo de uso del servicio (trayectos cortos urbanos vs. largos). | H1, H6 |
| 5 | **% de viajes en hora pico** | Viajes en hora pico / total | Mide la concentración de la demanda; guía la asignación de conductores. | H2 |
| 6 | **Ocupación promedio** | Σ pasajeros / N° viajes | Mide el aprovechamiento de la capacidad del vehículo; evalúa viajes compartidos. | H5 |
| 7 | **% de ingresos de aeropuertos** | Ingreso aeropuertos / ingreso total | Mide la dependencia de un segmento de alto valor. | H1, H6 |
| 8 | **Variación interanual de la tarifa promedio** | (Tarifa año t / tarifa año t−1) − 1 | Detecta cambios estructurales de precio (regulación, inflación). | H4 |

## Interpretación de cada indicador

Valores calculados sobre 191.776 viajes (`reports/kpis_globales.csv` y `reports/kpis_por_anio.csv`):

| KPI | Valor |
|-----|-------|
| Ingreso total | 2.166.790,70 USD |
| Total de viajes | 191.776 |
| Tarifa promedio por viaje | 11,30 USD |
| Tarifa por km | 3,36 USD/km |
| Distancia promedio por viaje | 3,37 km |
| % de viajes en hora pico | 26,5 % |
| Ocupación promedio | 1,69 pasajeros/viaje |
| % de ingresos de aeropuertos | 18,4 % |

1. **Ingreso total:** el periodo analizado (enero 2009 – junio 2015) generó **2.166.791 USD** en 191.776 viajes.
   2015 solo tiene seis meses, por lo que su ingreso (172.479 USD) no es comparable con los años completos.
2. **Tarifa promedio:** un viaje cuesta en promedio **11,30 USD**. Pasó de 9,94 USD en 2009 a 12,90 USD en 2015
   (+30 %), mientras la distancia promedio solo creció de 3,20 a 3,44 km: el aumento se debe sobre todo al precio.
3. **Tarifa por km:** cada km recorrido genera **3,36 USD**. Se mantuvo estable en ~3,10 USD entre 2009 y 2011 y
   subió a 3,76 USD en 2015. Por franja, la tarde es la más rentable (3,58 USD/km) y la madrugada la menos (2,95 USD/km).
4. **Distancia promedio:** **3,37 km** por viaje; predominan los trayectos cortos urbanos (la mediana es de 2,2 km).
   La madrugada tiene los viajes más largos (4,07 km).
5. **% hora pico:** el **26,5 %** de los viajes ocurre en hora pico (días hábiles 7-9 h y 16-19 h). En la franja
   de la mañana llega al 45,5 %, lo que exige más conductores en ese horario.
6. **Ocupación promedio:** **1,69 pasajeros por viaje**; el 69 % de los viajes lleva un solo pasajero, lo que
   sugiere potencial para viajes compartidos.
7. **% ingresos de aeropuertos:** los aeropuertos aportan el **18,4 %** de los ingresos con solo el **5,5 %** de los
   viajes (ticket de 30,80 USD en LGA, 46,50 USD en JFK y 71,18 USD en EWR, frente a 9,76 USD del resto). Su
   participación crece cada año: 15,9 % en 2009 → 21,1 % en 2015.
8. **Variación interanual:** la mayor variación de la tarifa promedio se presenta en **2013 (+13,2 %)**, seguida de
   2012 (+8,0 %), coincidiendo con el ajuste tarifario de NYC de septiembre de 2012. En 2015 la variación es nula (−0,02 %).

## Metas sugeridas para el dashboard ejecutivo

| KPI | Semáforo | Estado actual |
|-----|----------|---------------|
| Tarifa por km | Verde si ≥ valor del año anterior | Verde (3,76 USD en 2015 vs. 3,73 USD en 2014) |
| % hora pico | Alerta si supera el 30 % (posible déficit de conductores) | Verde (26,5 %) |
| Ocupación promedio | Verde si ≥ 1,5 pasajeros por viaje | Verde (1,69) |
