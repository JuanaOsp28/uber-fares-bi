# Fase 2 — Formulación de hipótesis

Nivel de significancia: **α = 0,05**. Las pruebas se ejecutan en `notebooks/03_pruebas_hipotesis.ipynb`
con las funciones de `src/stats_tests.py`.

## Elección de las pruebas

La tarifa y la distancia tienen una distribución fuertemente asimétrica a la derecha (no normal, se verifica con la
prueba de D'Agostino-Pearson). Por eso se usan **pruebas no paramétricas**, que comparan rangos/medianas y no
suponen normalidad. Además, con ~190.000 viajes casi cualquier diferencia resulta significativa, por lo que
cada prueba se acompaña de un **tamaño del efecto** para juzgar su relevancia práctica.

---

## H1 — Distancia y tarifa

- **H0:** No existe correlación positiva entre la distancia del viaje y la tarifa (ρ ≤ 0).
- **H1:** A mayor distancia del viaje, mayor tarifa (ρ > 0).
- **Variables:** `distancia_km`, `fare_amount`.
- **Prueba:** Correlación de Spearman (unilateral) + regresión lineal simple para estimar tarifa base y costo por km.
- **Importancia:** Valida que la distancia es el principal motor del precio y permite estimar la estructura
  tarifaria (bajada de bandera + costo por km), base de cualquier estrategia de precios.

## H2 — Hora pico

- **H0:** La tarifa por km es igual en hora pico y fuera de hora pico.
- **H1:** La tarifa por km difiere entre hora pico y fuera de hora pico.
- **Variables:** `es_hora_pico`, `tarifa_por_km` (y `fare_amount` como complemento).
- **Prueba:** Mann-Whitney U (bilateral).
- **Importancia:** Si la congestión encarece los viajes por km, la empresa puede justificar tarifas dinámicas y
  asignar más conductores en esas horas.

## H3 — Fin de semana

- **H0:** La tarifa es igual entre semana y fin de semana.
- **H1:** La tarifa difiere entre semana y fin de semana.
- **Variables:** `es_fin_de_semana`, `fare_amount`.
- **Prueba:** Mann-Whitney U (bilateral).
- **Importancia:** Permite diseñar promociones o tarifas diferenciadas según el tipo de día.

## H4 — Evolución anual de la tarifa

- **H0:** La tarifa por km es igual en todos los años (2009–2015).
- **H1:** Al menos un año tiene una tarifa por km diferente.
- **Variables:** `anio`, `tarifa_por_km`.
- **Prueba:** Kruskal-Wallis y, como complemento, Mann-Whitney antes vs. después del ajuste tarifario de NYC de
  septiembre de 2012.
- **Importancia:** Identifica cambios estructurales de precio (inflación, regulación) que deben considerarse al
  comparar periodos en el dashboard.

## H5 — Número de pasajeros

- **H0:** La tarifa no difiere según el número de pasajeros.
- **H1:** La tarifa difiere según el número de pasajeros.
- **Variables:** `passenger_count`, `fare_amount`.
- **Prueba:** Kruskal-Wallis.
- **Importancia:** Determina si tiene sentido un esquema de precios por ocupación (por ejemplo, viajes compartidos).

## H6 — Franja horaria y tipo de trayecto

- **H0:** La franja horaria y la categoría de distancia son independientes.
- **H1:** La categoría de distancia depende de la franja horaria.
- **Variables:** `franja_horaria`, `categoria_distancia`.
- **Prueba:** Chi-cuadrado de independencia + V de Cramér.
- **Importancia:** Si en ciertas franjas predominan los viajes largos (por ejemplo, aeropuertos en la madrugada),
  la empresa puede ubicar conductores estratégicamente.

## Relación con las preguntas clave

| Pregunta (Fase 1) | Hipótesis |
|-------------------|-----------|
| 1. Relación distancia–tarifa | H1 |
| 2. Tarifa según franja y día | H2, H3, H6 |
| 3. Evolución de la tarifa 2009–2015 | H4 |
| 4. Influencia de los pasajeros | H5 |
