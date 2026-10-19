# Fase 6 — Análisis, validación y storytelling

Fuentes: `reports/resultados_hipotesis.csv`, `reports/kpis_globales.csv`, `reports/kpis_por_anio.csv` y el dashboard.

## 1. Narrativa con los datos

La historia se cuenta en cuatro actos, siguiendo las páginas del dashboard:

1. **El contexto — ¿cuánto se mueve?** Entre enero de 2009 y junio de 2015, los **191.776 viajes** analizados
   generaron **2,17 millones de USD**, con un ticket promedio de **11,30 USD** y viajes cortos de **3,37 km** en
   promedio. La demanda crece durante el día, cae a las 16 h por el cambio de turno de los taxis y alcanza su
   máximo a las 19 h; el viernes es el día con más viajes.
2. **El motor del precio — la distancia.** La distancia explica el **81 %** de la variación de la tarifa
   (rho = 0,867, R² = 0,807). La tarifa base estimada es de **3,38 USD** y cada km adicional cuesta **2,35 USD**.
   Los aeropuertos son el caso extremo: con solo el 5,5 % de los viajes aportan el **18,4 % de los ingresos**.
3. **El tiempo importa — hora y año, pero no el tipo de día.** En hora pico cada km cuesta un **8 % más**
   (4,03 vs. 3,73 USD de mediana) por la congestión, aunque el viaje total cuesta lo mismo porque es más corto.
   El cambio más importante es el **ajuste tarifario de septiembre de 2012**: la tarifa por km subió un **19 %**
   (3,52 → 4,20 USD de mediana) y la tarifa promedio creció un 13,2 % en 2013. El fin de semana, en cambio,
   no cambia la tarifa (p = 0,149).
4. **Lo que no importa — los pasajeros.** La tarifa es la misma (mediana 8,50 USD) para 1 a 5 pasajeros:
   la diferencia es estadísticamente significativa pero de tamaño despreciable. Además, el **69 %** de los viajes
   lleva un solo pasajero (1,69 en promedio): hay capacidad ociosa.

## 2. Validación de hipótesis (valor p)

| Hipótesis | Prueba | Valor p | Tamaño del efecto | Decisión | Relevancia práctica |
|-----------|--------|---------|-------------------|----------|---------------------|
| H1 Distancia → tarifa | Spearman | < 0,001 | rho = 0,867 | Se rechaza H0 | Alta |
| H2 Tarifa/km en hora pico | Mann-Whitney U | < 0,001 | r = 0,111 | Se rechaza H0 | Moderada |
| H3 Fin de semana | Mann-Whitney U | 0,149 | r = 0,004 | No se rechaza H0 | Nula |
| H4 Tarifa/km entre años | Kruskal-Wallis | < 0,001 | ε² = 0,043 | Se rechaza H0 | Moderada |
| H4b Antes vs. después de sep-2012 | Mann-Whitney U | < 0,001 | r = 0,258 | Se rechaza H0 | Alta |
| H5 Pasajeros | Kruskal-Wallis | < 0,001 | ε² = 0,0009 | Se rechaza H0 | Nula |
| H6 Franja × distancia | Chi-cuadrado | < 0,001 | V = 0,076 | Se rechaza H0 | Baja |

Criterio: valor p < 0,05 → se rechaza H0. Se considera **relevante para el negocio** solo si además el tamaño
del efecto es al menos pequeño (|rho|, |r| o V ≥ 0,1; ε² ≥ 0,01). Con casi 192.000 registros, H5 y H6 son
significativas pero su efecto es despreciable: **significancia estadística no implica relevancia práctica**.

## 3. Decisiones propuestas basadas en evidencia

| Evidencia | Decisión |
|-----------|----------|
| La distancia explica el 81 % de la tarifa; base de 3,38 USD + 2,35 USD/km (H1) | Mostrar al usuario un precio estimado antes del viaje con este modelo base + km; aumenta la confianza y la conversión. |
| Tarifa por km +8 % en hora pico; 45,5 % de los viajes de la mañana son en hora pico (H2, KPI 5) | Incentivar a los conductores a conectarse en días hábiles de 7-9 h y 16-19 h; evaluar una tarifa dinámica moderada. |
| La tarifa no cambia en fin de semana (H3) | No aplicar recargos por tipo de día; usar los fines de semana para promociones que estimulen la demanda. |
| Ajuste de sep-2012: tarifa por km +19 % (H4) | Comparar periodos con la tarifa por km y no con ingresos totales; separar en el dashboard los periodos antes y después del ajuste. |
| Pasajeros sin efecto en la tarifa y 69 % de viajes con un solo pasajero (H5, KPI 6) | Lanzar viajes compartidos con descuento para aprovechar la capacidad ociosa. |
| Aeropuertos: 5,5 % de los viajes y 18,4 % de los ingresos, en crecimiento (KPI 7) | Ubicar conductores cerca de JFK y LGA, sobre todo en la madrugada, cuando los viajes son más largos (H6). |

## 4. Limitaciones

- **Distancia aproximada:** se usa la distancia en línea recta (Haversine), no la ruta real; subestima los trayectos.
- **Sin variables de contexto:** no hay duración del viaje, propinas, peajes, clima ni tipo de servicio, que
  explicarían parte del 19 % de variación que no explica la distancia.
- **Periodo histórico (2009–2015):** las tarifas actuales y la competencia son distintas; 2015 solo tiene seis meses.
- **Muestra:** los 200.000 registros son una muestra del total de viajes y pueden no representar todas las zonas.
- **Muestra grande:** casi todas las pruebas resultan significativas; por eso se interpreta el tamaño del efecto.
- **Reglas de limpieza:** se eliminó el 4,1 % de los registros; los umbrales (tarifa, distancia, coordenadas)
  son decisiones del equipo y afectan los resultados.
- **Zona horaria:** las fechas dicen "UTC", pero su patrón horario indica que ya están en hora local de NYC; se
  usan sin conversión. Si la etiqueta fuera correcta, los análisis por hora estarían desplazados 4-5 horas.
- **Identificación de aeropuertos:** se usa un radio de 2 km alrededor de cada aeropuerto, por lo que algunos
  viajes cercanos pueden quedar mal clasificados.
