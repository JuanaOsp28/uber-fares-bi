# Dashboard — Power BI

Archivo del dashboard: `uber_fares_dashboard.pbix` (en esta carpeta).

## 1. Carga de datos

1. Obtener `fact_viajes.csv`, `dim_fecha.csv` y `dim_hora.csv`, generados por
   `notebooks/02_preparacion_modelado.ipynb` en `data/processed/` (no se versionan por tamaño).
2. Power BI Desktop → **Obtener datos → Texto/CSV** y cargar los tres archivos.
3. En Power Query verificar tipos: `fecha` y `fecha_local` como fecha, columnas `es_*` como verdadero/falso,
   coordenadas como número decimal (configuración regional **Inglés (Estados Unidos)** para que el punto decimal se lea bien).

## 2. Modelo

En la vista **Modelo** crear las relaciones (uno a varios, dirección de filtro única):

- `dim_fecha[id_fecha]` → `fact_viajes[id_fecha]`
- `dim_hora[hora]` → `fact_viajes[hora]`

Marcar `dim_fecha` como tabla de fechas (columna `fecha`). Ordenar `dim_fecha[nombre_mes]` por `mes` y
`dim_fecha[dia_semana]` por `dia_semana_num`.

## 3. Medidas

Crear las medidas de [`medidas_dax.md`](medidas_dax.md).

## 4. Páginas del reporte

### Página 1 — Dashboard ejecutivo
| Visual | Contenido |
|--------|-----------|
| 5 tarjetas (KPI) | Ingreso Total, Total Viajes, Tarifa Promedio, Tarifa por Km (con semáforo), % Viajes Hora Pico |
| Gráfico de líneas | Tarifa Promedio y Tarifa por Km por `dim_fecha[anio_mes]` |
| Gráfico de columnas | Total Viajes por `dim_hora[hora]` |
| Gráfico de anillo | Ingreso Total por `fact_viajes[aeropuerto]` |
| Segmentadores | `dim_fecha[anio]`, `dim_hora[franja_horaria]` |

### Página 2 — Análisis temporal
| Visual | Contenido |
|--------|-----------|
| Matriz / mapa de calor | Filas `dia_semana`, columnas `hora`, valor Total Viajes (formato condicional de color de fondo) |
| Gráfico de barras agrupadas | Tarifa por Km por `franja_horaria`, leyenda `es_hora_pico` |
| Gráfico de columnas | Variacion Interanual Tarifa por `anio` |
| Segmentadores | `anio`, `es_fin_de_semana` |

### Página 3 — Análisis de trayectos
| Visual | Contenido |
|--------|-----------|
| Mapa (Azure Maps o Mapa) | Latitud `pickup_latitude`, longitud `pickup_longitude`, tamaño Total Viajes |
| Gráfico de dispersión | Eje X Distancia Promedio, eje Y Tarifa Promedio, detalle `categoria_distancia` |
| Gráfico de columnas apiladas | Total Viajes por `categoria_distancia`, leyenda `franja_horaria` |
| Gráfico de barras | Tarifa Promedio por `passenger_count` |
| Segmentadores | `aeropuerto`, `anio` |

### Página 4 — Hipótesis
Tarjetas de texto con la decisión de cada hipótesis (`reports/resultados_hipotesis.csv`) y un visual de apoyo por
hipótesis.

## 5. Buenas prácticas de diseño

- Paleta reducida (2–3 colores) y un único color de acento para resaltar.
- KPI más importantes arriba a la izquierda; lectura en "Z".
- Títulos descriptivos que cuenten el hallazgo (ej. "La tarifa por km sube en hora pico").
- Ejes con unidades, sin decimales innecesarios y sin efectos 3D.
- Sincronizar segmentadores entre páginas (Ver → Sincronizar segmentaciones).
- Botones de navegación entre páginas e información sobre herramientas con KPIs adicionales.
