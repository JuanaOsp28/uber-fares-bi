# Fase 1 — Comprensión del problema

## Contexto del dataset

El **Uber Fares Dataset** contiene aproximadamente 200.000 viajes realizados en la ciudad de Nueva York
entre 2009 y 2015. Cada registro describe un viaje con su tarifa en dólares, la fecha y hora de recogida,
las coordenadas geográficas de origen y destino, y el número de pasajeros.

Nueva York es uno de los mercados de transporte urbano más competidos del mundo: taxis amarillos, taxis verdes
y plataformas de movilidad compiten por los mismos usuarios. En este entorno, entender **qué determina el precio
de un viaje** es clave tanto para la empresa (estrategia de precios, asignación de conductores) como para los
usuarios (planificación de gastos de transporte).

El dataset no incluye la distancia del viaje de forma explícita, por lo que debe calcularse a partir de las
coordenadas (distancia de Haversine). Además, presenta problemas de calidad: tarifas negativas o nulas,
coordenadas en (0, 0) o fuera de la ciudad, y registros con cantidades de pasajeros imposibles.

## Problema de análisis / negocio

> **¿Qué factores explican el valor de la tarifa de un viaje de Uber en Nueva York y cómo se comporta la demanda
> a lo largo del tiempo, de forma que la empresa pueda tomar decisiones sobre precios y disponibilidad de conductores?**

Una política de precios que no considere la hora, el día o el tipo de trayecto puede generar pérdida de ingresos
en momentos de alta demanda o baja ocupación de conductores en momentos de baja demanda.

## Preguntas clave

1. **¿Qué tan fuerte es la relación entre la distancia del viaje y la tarifa?** ¿Existe una tarifa base
   y un costo por kilómetro identificable?
2. **¿Cambia la tarifa según la franja horaria (hora pico vs. hora valle) y el día de la semana?**
3. **¿Cómo ha evolucionado la tarifa promedio entre 2009 y 2015?** ¿Hay cambios estructurales en el precio?
4. **¿Influye el número de pasajeros en el valor de la tarifa?**
5. **¿En qué horas y días se concentra la demanda de viajes?**
6. **¿Qué peso tienen los viajes hacia/desde aeropuertos en los ingresos totales?**

## Variables relevantes

| Variable | Rol en el análisis |
|----------|--------------------|
| `fare_amount` | Variable objetivo (métrica principal) |
| `pickup_datetime` | Se deriva año, mes, día de la semana, hora y franja horaria |
| Coordenadas de origen y destino | Se deriva la distancia del viaje y la identificación de aeropuertos |
| `passenger_count` | Variable explicativa de ocupación |

## Hallazgos iniciales del EDA

Ver `notebooks/01_comprension_problema.ipynb`. Resumen de los problemas de calidad detectados que se tratan en la Fase 3:

- Tarifas menores o iguales a cero y valores extremos.
- Coordenadas en cero o fuera del área de Nueva York.
- Registros con 0 pasajeros o con cantidades atípicas.
- Viajes con origen igual a destino (distancia cero).
- Un registro con coordenadas de destino nulas.
