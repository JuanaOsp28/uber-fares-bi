# Análisis comparativo — supervisado vs. no supervisado

Documento de cierre que integra los resultados de `notebooks/01_eda.ipynb`, `notebooks/02_supervisado.ipynb` y
`notebooks/03_no_supervisado.ipynb`. Todas las cifras son sobre el conjunto de prueba (supervisado) o de
entrenamiento (no supervisado) de la partición estratificada 80/20 con semilla 42.

## 1. Qué responde cada enfoque

| | Supervisado | No supervisado |
|---|---|---|
| Pregunta | ¿Este cliente aceptará el depósito? | ¿Qué tipos de clientes hay? |
| Usa `y` | Sí, para entrenar | No; solo después, para interpretar |
| Resultado | Una probabilidad por cliente | Un segmento por cliente |
| Modelo final | Gradient Boosting (HistGB) optimizado | K-Means con k = 4 sobre PCA (90 % de varianza) |
| Métrica principal | PR-AUC (por el desbalance de 11,7 % "yes") | Silhouette y Davies-Bouldin, más interpretabilidad |

## 2. Resultados de cada componente

**Supervisado (prueba, modelos optimizados):**

| Modelo | Precision | Recall | F1 | ROC-AUC | PR-AUC |
|---|---|---|---|---|---|
| Regresión logística | 0,235 | 0,680 | 0,349 | 0,756 | 0,373 |
| Random Forest | 0,486 | 0,493 | 0,490 | 0,806 | 0,461 |
| **Gradient Boosting (elegido)** | 0,353 | 0,646 | 0,457 | 0,806 | **0,467** |

Gradient Boosting se eligió por tener el mayor PR-AUC y un recall mucho más alto que Random Forest (64,6 % frente a
49,3 %), con un costo de búsqueda ocho veces menor. La diferencia de PR-AUC con Random Forest (0,006) es pequeña;
lo que sí es claro es que los modelos de árboles superan a la regresión logística.

**No supervisado:**

| Algoritmo | k | Silhouette | Davies-Bouldin |
|---|---|---|---|
| **K-Means (elegido)** | 4 | 0,164 | 1,906 |
| Mezcla gaussiana | 4 | 0,090 | 3,702 |
| Jerárquico Ward (muestra) | 4 | 0,164 | 1,861 |

| Segmento | Tamaño | Aceptación |
|---|---|---|
| Nuevos sin canal registrado | 45,6 % | 9,0 % |
| Nuevos de verano contactados por celular | 36,2 % | 9,5 % |
| Recontactados antiguos con campaña fallida | 7,7 % | 13,4 % |
| Recontactados recientes con historial positivo | 10,5 % | **29,8 %** |

## 3. Dónde coinciden

Los dos enfoques llegan, por caminos distintos, a la misma conclusión: **lo que más explica la aceptación es la
campaña y el historial de contacto, no el perfil demográfico del cliente.**

- En el modelo supervisado, las variables más importantes por permutación son el **mes** (0,087), el **tipo de
  contacto** (0,063) y el **resultado de la campaña anterior** (0,029); edad, trabajo o estado civil pesan poco.
- El clustering, **sin ver `y`**, separó a los clientes justamente por esas variables: historial de contacto
  (`pdays`, `poutcome`), canal (`contact`) y mes. Y los segmentos resultantes tienen aceptaciones muy distintas
  (9,0 % a 29,8 %; χ² = 1.392, p ≈ 1,6·10⁻³⁰¹).
- Ambos confirman lo observado en el EDA: mayo concentra muchas llamadas con baja aceptación, `contact = unknown`
  casi no acepta y `poutcome = success` es la señal más fuerte de éxito.

## 4. Dónde se complementan

- **El supervisado ordena, el no supervisado explica.** El modelo dice *a quién* llamar primero, pero es una caja
  negra para el área comercial. Los segmentos dicen *qué tipo de cliente es* y permiten diseñar un mensaje, un canal y
  un momento distinto para cada grupo.
- **Granularidad.** Dentro de los segmentos de clientes nuevos (82 % de la base, ~9 % de aceptación) hay clientes con
  probabilidad alta que el promedio del segmento esconde; el modelo supervisado los encuentra.
- **Valor de negocio.** Con los costos supuestos en el notebook 02, llamar solo a los clientes con probabilidad ≥ 0,5
  da una ganancia de 4.897 frente a 1.537 si se llama a todos, con 1.933 llamadas en lugar de 9.043 (79 % menos),
  conservando el 64,6 % de las suscripciones.

## 5. Estrategia recomendada (uso conjunto)

1. **Segmentar** la base con K-Means para definir la estrategia de cada grupo:
   - *Recontactados con historial positivo:* prioridad máxima, recontacto temprano y pocas llamadas.
   - *Recontactados con campaña fallida:* cambiar la oferta en lugar de repetirla.
   - *Clientes nuevos:* contactar por celular, registrar el canal de quienes hoy aparecen como `unknown` y evitar
     concentrar la campaña en mayo.
2. **Dentro de cada segmento**, ordenar a los clientes por la probabilidad del modelo de Gradient Boosting y llamar
   primero a los de arriba, con un umbral cercano a 0,5.
3. **Medir** la tasa de aceptación por segmento en la siguiente campaña para validar ambos modelos con datos nuevos.

## 6. Limitaciones del análisis

- **Supervisado:** el PR-AUC de 0,467 indica que aún hay muchos falsos positivos; el ROC-AUC (0,806) es optimista con
  clases desbalanceadas; los costos del análisis de ganancia son supuestos; y la evaluación usa un solo split de prueba.
- **No supervisado:** el Silhouette es bajo (0,16), así que los segmentos resumen un continuo más que grupos
  naturales; el PCA pierde ~9 % de la varianza; la estabilidad de K-Means es buena pero no perfecta (ARI medio 0,79);
  y k = 4 se eligió por interpretabilidad (el BIC de la mezcla gaussiana sugiere 7 componentes).
- **Datos:** se excluyó `duration` para evitar fuga de información, lo que reduce el desempeño pero hace el modelo
  utilizable antes de la llamada; los datos son de campañas de 2008–2010 en Portugal, por lo que habría que
  revalidarlos antes de aplicarlos hoy.

## 7. Conclusión

El modelo supervisado permite **priorizar** a quién llamar y reduce las llamadas en un 79 % conservando dos tercios de
las ventas; el clustering permite **entender y personalizar** la campaña con cuatro perfiles accionables. Usados juntos,
el banco puede decidir a quién llamar, cuándo, por qué canal y con qué oferta.
