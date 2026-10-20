# Medidas DAX

Crear una tabla vacía `_Medidas` (Inicio → Especificar datos → Cargar) y agregar en ella las siguientes medidas.

```dax
Total Viajes = COUNTROWS ( fact_viajes )

Ingreso Total = SUM ( fact_viajes[fare_amount] )

Tarifa Promedio = DIVIDE ( [Ingreso Total], [Total Viajes] )

Distancia Total = SUM ( fact_viajes[distancia_km] )

Tarifa por Km = DIVIDE ( [Ingreso Total], [Distancia Total] )

Distancia Promedio = DIVIDE ( [Distancia Total], [Total Viajes] )

Viajes Hora Pico =
CALCULATE ( [Total Viajes], fact_viajes[es_hora_pico] = TRUE () )

% Viajes Hora Pico = DIVIDE ( [Viajes Hora Pico], [Total Viajes] )

Ocupacion Promedio = AVERAGE ( fact_viajes[passenger_count] )

Ingreso Aeropuertos =
CALCULATE ( [Ingreso Total], fact_viajes[es_aeropuerto] = TRUE () )

% Ingreso Aeropuertos = DIVIDE ( [Ingreso Aeropuertos], [Ingreso Total] )

Tarifa Promedio Año Anterior =
VAR AnioActual = MAX ( dim_fecha[anio] )
RETURN
    CALCULATE ( [Tarifa Promedio], REMOVEFILTERS ( dim_fecha ), dim_fecha[anio] = AnioActual - 1 )

Variacion Interanual Tarifa =
DIVIDE ( [Tarifa Promedio] - [Tarifa Promedio Año Anterior], [Tarifa Promedio Año Anterior] )

Tarifa por Km Año Anterior =
VAR AnioActual = MAX ( dim_fecha[anio] )
RETURN
    CALCULATE ( [Tarifa por Km], REMOVEFILTERS ( dim_fecha ), dim_fecha[anio] = AnioActual - 1 )

Semaforo Tarifa Km =
IF ( [Tarifa por Km] >= [Tarifa por Km Año Anterior], "#2E8B57", "#C0392B" )
```

## Formatos

| Medida | Formato |
|--------|---------|
| Ingreso Total, Tarifa Promedio, Tarifa por Km | Moneda (USD), 2 decimales |
| Distancia Promedio | Decimal, 2 decimales |
| % Viajes Hora Pico, % Ingreso Aeropuertos, Variacion Interanual Tarifa | Porcentaje, 1 decimal |
| Total Viajes | Número entero con separador de miles |

`Semaforo Tarifa Km` se usa en *Formato condicional → Color de fuente → Valor del campo* de la tarjeta de Tarifa por Km.

## Validación

Los valores de las tarjetas, sin filtros, deben coincidir con `reports/kpis_globales.csv` generado por `notebooks/04_kpis.ipynb`.
