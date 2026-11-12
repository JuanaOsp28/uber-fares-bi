# EDA, preprocesamiento y relevancia de variables — decisiones técnicas

Documento complementario de `notebooks/01_eda.ipynb` y `src/preprocessing.py`.

## Hallazgos del EDA
_(Completar con los resultados reales después de ejecutar el notebook.)_

| Tema | Hallazgo | Decisión |
|---|---|---|
| Desbalance | ≈ 11,7 % de "yes" | Pesos de clase; métricas F1, Recall, Precision, ROC-AUC y PR-AUC |
| `unknown` | Presente en `job`, `education`, `contact`, `poutcome` | Se conserva como categoría propia |
| `pdays = -1` | La mayoría no fue contactada antes | Bandera `previously_contacted` + imputación de `pdays` |
| Colas largas | `balance`, `campaign`, `previous` | Log con signo |
| Variables temporales | `month` con fuerte estacionalidad | Codificación cíclica (seno/coseno) |
| `duration` | Solo se conoce después de la llamada | Excluida (data leakage) |

## Cómo se evita la fuga de información
1. La partición train/test se hace **antes** de cualquier análisis (`src/data_loader.py`, semilla 42).
2. El EDA usa solo el conjunto de entrenamiento.
3. Imputación, escalado y One-Hot viven dentro de un `Pipeline` que se ajusta únicamente con entrenamiento.
4. `duration` se elimina porque no existe al momento de decidir a quién llamar.

## Relevancia de variables y dimensionalidad
- **Información mutua** entre cada variable preprocesada y `y` (solo entrenamiento): ranking y variables casi irrelevantes.
- **PCA** sobre la matriz preprocesada: número de componentes para 90 % y 95 % de varianza (redundancia por el one-hot).
- _(Completar: qué variables se proponen descartar y qué estrategia se probará en el componente supervisado.)_

## Alternativas consideradas
_(Completar: ¿agrupar categorías raras de `job`? ¿otro tratamiento de `unknown`? ¿otra codificación?)_
