# Modelos supervisados — justificación

Documento complementario de `notebooks/02_supervisado.ipynb` y `src/supervised.py`.

**Problema:** clasificación binaria desbalanceada (¿suscribe el depósito a plazo?).

## Algoritmos

### Regresión logística (línea base)
- **Por qué:** modelo simple e interpretable para tener una referencia.
- **Supuestos:** relación lineal entre las variables y el log-odds; poca multicolinealidad.
- **Ventajas:** coeficientes interpretables, entrena rápido, buena calibración.
- **Limitaciones:** no captura interacciones ni no linealidades sin ingeniería adicional.

### Random Forest
- **Por qué:** captura no linealidades e interacciones con variables mixtas.
- **Supuestos:** ninguno fuerte sobre la distribución.
- **Ventajas:** robusto a atípicos, da importancia de variables.
- **Limitaciones:** menos interpretable, más costoso, probabilidades menos calibradas.

### Gradient Boosting (HistGradientBoosting)
- **Por qué:** suele ser el mejor en datos tabulares.
- **Supuestos:** ninguno fuerte.
- **Ventajas:** alta capacidad predictiva, maneja nulos de forma nativa.
- **Limitaciones:** más hiperparámetros, riesgo de sobreajuste.

## Tratamiento del desbalance
`class_weight="balanced"` en los tres modelos. No probamos SMOTE: con los pesos de clase los modelos ya llegan a un recall de 0,62-0,66 en validación cruzada, y
generar clientes sintéticos con tantas variables categóricas (One-Hot) puede crear perfiles que no existen. Además el
desbalance lo manejamos también con la métrica (PR-AUC) y con el ajuste del umbral. Si se quisiera probar, el
remuestreo tendría que ir dentro del pipeline para aplicarse solo a los folds de entrenamiento.

## Selección de variables y reducción de dimensionalidad
Se comparan, con validación cruzada y dentro del pipeline: sin selección, información mutua (k = 20),
L1 y PCA (95 %). 

| Selector | Columnas | PR-AUC logística | PR-AUC Gradient Boosting |
|---|---|---|---|
| Sin selección | 41 | 0,372 | **0,449** |
| Información mutua (k = 20) | 20 | 0,358 | 0,434 |
| L1 | 29 | 0,372 | 0,444 |
| PCA 95 % | 19 | 0,296 | 0,372 |

**Decisión: no usar selección.** Ningún selector mejora el PR-AUC y PCA lo empeora bastante. Esto cuadra con el EDA:
la información mutua de cada variable es baja y las "casi irrelevantes" eran dummies sueltas que juntas sí aportan
(por ejemplo `job`). Como el modelo entrena rápido con 41 columnas, reducir no nos da ventaja y PCA además nos quitaría
la posibilidad de interpretar las variables originales.

## Optimización de hiperparámetros
`RandomizedSearchCV` (15 combinaciones, CV de 3 folds) optimizando PR-AUC; espacios de búsqueda en
`get_param_distributions()`. 

| Modelo | PR-AUC CV (base → optimizado) | PR-AUC prueba (base → optimizado) | Mejores parámetros | Tiempo |
|---|---|---|---|---|
| Regresión logística | 0,372 → 0,372 | 0,373 → 0,373 | `C` ≈ 0,075 | 6 s |
| Random Forest | 0,442 → 0,443 | 0,457 → 0,461 | `max_depth=None`, `min_samples_leaf=5`, `max_features=0,3` | 179 s |
| Gradient Boosting | 0,449 → 0,450 | 0,463 → 0,467 | `learning_rate` ≈ 0,10, `max_leaf_nodes=63`, `min_samples_leaf=100`, `l2_regularization` ≈ 0,54 | 23 s |

La mejora es muy pequeña. Lo leemos como que el límite está en la información disponible y no en los parámetros:
sin `duration` el PR-AUC se estanca alrededor de 0,46-0,47, aunque eso es casi cuatro veces el 0,117 del azar.

## Criterios de comparación y selección del modelo
1. PR-AUC y F1 en prueba. 2. Recall. 3. Estabilidad (brecha CV vs prueba). 4. Interpretabilidad y costo computacional.


**Modelo elegido: Gradient Boosting.** Empata con Random Forest en el ranking (gana en PR-AUC 0,467 frente a 0,461;
pierde en F1 0,457 frente a 0,490) y desempatamos por PR-AUC porque no depende del umbral. Además tiene mucho mejor
recall (0,646 frente a 0,493), la misma estabilidad (brecha CV-prueba de −0,018 en ambos) y su búsqueda tardó 23 s
frente a 179 s. La diferencia con Random Forest es pequeña y puede estar dentro del ruido; lo que sí es claro es que
los dos modelos de árboles superan a la regresión logística (PR-AUC 0,373). Sacrificamos interpretabilidad directa,
que compensamos con la importancia por permutación.

## Métricas y su lectura crítica
Precision, Recall, F1, ROC-AUC (exigidas) y PR-AUC (más informativa con desbalance). La matriz de confusión
permite analizar el costo de falsos positivos (llamadas inútiles) frente a falsos negativos (clientes interesados
que no se contactan). 

Limitaciones que tenemos presentes:
- **Un solo split de prueba** (9.043 clientes, 1.058 "yes"): diferencias de centésimas entre modelos pueden ser azar.
- **ROC-AUC optimista con desbalance:** 0,806 se ve bien, pero el PR-AUC (0,467) muestra que todavía hay muchos falsos positivos.
- **Dependencia del umbral:** con 0,5 el recall es 0,646 y la precisión 0,353; con el umbral que maximiza F1 (0,62,
  elegido con validación cruzada) pasan a 0,557 y 0,442.
- **Costos supuestos:** con llamada = 1 y suscripción = 10, el umbral de F1 deja menos ganancia que 0,5 y el que
  maximiza la ganancia en validación sale alrededor de 0,47. Esos números cambian si los costos reales son otros.

## Resultados y conclusiones


Métricas en prueba de los modelos optimizados (umbral 0,5), de `reports/results/supervisado_ranking_modelos.csv`:

| Modelo | Precision | Recall | F1 | ROC-AUC | PR-AUC |
|---|---|---|---|---|---|
| **Gradient Boosting** | 0,353 | **0,646** | 0,457 | **0,806** | **0,467** |
| Random Forest | **0,486** | 0,493 | **0,490** | **0,806** | 0,461 |
| Regresión logística | 0,235 | 0,680 | 0,349 | 0,756 | 0,373 |

Gradient Boosting con umbral 0,62: Precision 0,442, Recall 0,557, F1 0,493. El análisis de costos está en
`supervisado_costos_umbral.csv`.

**Importancia de variables (permutación, ROC-AUC):** dominan las variables de campaña y de momento de la llamada:
`month` (0,087), `contact` (0,063), `poutcome` (0,029) y `day` (0,027). Después vienen `balance`, `age` y `housing`
(≈ 0,010). `job`, `loan` y `default` casi no influyen. Esto es coherente con el EDA (mayo con baja aceptación,
`poutcome = success` con 64,6 %, `contact = unknown` con 4,1 %). Como `contact` y el mes están relacionados, y también
`pdays` y `previous`, la permutación puede repartir o subestimar su importancia; y la importancia no implica causalidad.

**Conclusión:** el modelo no es perfecto, pero sirve para priorizar. Con umbral 0,5 encuentra el 65 % de los clientes
que aceptan y de cada 100 llamadas aceptan unos 35, frente a 12 llamando al azar. Recomendamos usarlo para ordenar la
lista de clientes, validar los costos reales con el banco antes de fijar el umbral y reentrenarlo con cada campaña,
porque depende mucho del mes y del canal.
