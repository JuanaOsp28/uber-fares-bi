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
`class_weight="balanced"` en los tres modelos. _(Completar si el equipo prueba SMOTE u otra técnica:
cualquier remuestreo debe aplicarse solo dentro del entrenamiento/validación cruzada.)_

## Selección de variables y reducción de dimensionalidad
Se comparan, con validación cruzada y dentro del pipeline: sin selección, información mutua (k = 20),
L1 y PCA (95 %). _(Completar con la decisión y su justificación.)_

## Optimización de hiperparámetros
`RandomizedSearchCV` (15 combinaciones, CV de 3 folds) optimizando PR-AUC; espacios de búsqueda en
`get_param_distributions()`. _(Completar con los mejores parámetros y la mejora frente a la línea base.)_

## Criterios de comparación y selección del modelo
1. PR-AUC y F1 en prueba. 2. Recall. 3. Estabilidad (brecha CV vs prueba). 4. Interpretabilidad y costo computacional.
_(Completar con el modelo elegido y la argumentación.)_

## Métricas y su lectura crítica
Precision, Recall, F1, ROC-AUC (exigidas) y PR-AUC (más informativa con desbalance). La matriz de confusión
permite analizar el costo de falsos positivos (llamadas inútiles) frente a falsos negativos (clientes interesados
que no se contactan). _(Completar limitaciones: un solo split de prueba, umbral, costos supuestos.)_

## Resultados y conclusiones
_(Completar con la tabla final de `reports/results/` y la lectura de la importancia de variables.)_
