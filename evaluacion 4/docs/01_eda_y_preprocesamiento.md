# EDA, preprocesamiento y relevancia de variables — decisiones técnicas

Documento complementario de `notebooks/01_eda.ipynb` y `src/preprocessing.py`.
Todas las cifras se calculan sobre el conjunto de **entrenamiento** (36.168 clientes, 15 variables sin `duration`).
Las figuras están en `reports/figures/eda_*.png`.

## Hallazgos del EDA

| Tema | Hallazgo | Decisión |
|---|---|---|
| Calidad | Sin nulos explícitos; 10 filas duplicadas (0,03 %) sin identificador de cliente | Se conservan (pueden ser clientes distintos con el mismo perfil) |
| Desbalance | 11,7 % de "yes" (4.231 frente a 31.937); predecir siempre "no" da un 88,3 % de *accuracy* | Partición estratificada, pesos de clase; métricas F1, Recall, Precision, ROC-AUC y PR-AUC |
| `unknown` | `poutcome` 81,8 %, `contact` 28,7 %, `education` 4,1 %, `job` 0,6 % | Se conserva como categoría propia (es informativo: `contact = unknown` acepta solo un 4,1 %) |
| `pdays = -1` | El 81,8 % nunca fue contactado; los contactados antes aceptan un 22,8 % frente a un 9,2 % | Bandera `previously_contacted` + `pdays` → NaN imputado con la mediana |
| Colas largas | Asimetría: `balance` 8,3, `campaign` 4,9, `previous` 45 | Log con signo (conserva saldos negativos) |
| Atípicos | 18,2 % en `pdays`/`previous` (efecto del -1/0), 10,4 % en `balance`, 6,8 % en `campaign` | No se eliminan: son valores reales; se suavizan con el log |
| Edad | Relación en U: 24,4 % (≤ 25 años) y 42,1 % (> 60) frente a ~9-10 % entre 30 y 60 | Se mantiene numérica; los modelos no lineales captan la U |
| Correlaciones | Bajas; la mayor es `pdays`–`previous` (0,44) | No se elimina ninguna numérica; `StandardScaler` por las escalas distintas |
| Categóricas | Más aceptación: student (28,9 %), retired (23,0 %), sin hipoteca (16,7 %), single (15,0 %), tertiary (14,9 %). Menos: con préstamo (6,8 %), en mora (5,9 %), blue-collar (7,3 %) | One-Hot con `handle_unknown="ignore"` |
| Campaña | `poutcome = success` acepta un 64,6 %; la tasa cae de 14,6 % (1 llamada) a 4,1 % (> 10 llamadas) | Log en `campaign`; insistir no mejora la conversión |
| Variables temporales | Mayo concentra el 30,6 % de las llamadas con la menor tasa (6,7 %); marzo, septiembre, octubre y diciembre superan el 40 % con poco volumen | Codificación cíclica del mes (seno/coseno) |
| `duration` | Media de 537 s ("yes") frente a 221 s ("no"); solo se conoce después de la llamada | Excluida (fuga de información) |

## Cómo se evita la fuga de información
1. La partición train/test se hace **antes** de cualquier análisis (`src/data_loader.py`, semilla 42, estratificada 80/20).
2. El EDA usa solo el conjunto de entrenamiento.
3. Imputación, escalado y One-Hot viven dentro de un `Pipeline` que se ajusta únicamente con entrenamiento (resultado: 41 columnas sin NaN).
4. `duration` se elimina porque no existe al momento de decidir a quién llamar.

## Relevancia de variables y dimensionalidad
- **Información mutua** entre cada variable preprocesada y `y` (solo entrenamiento). Las más informativas son `poutcome_success` (0,028), `pdays` (0,025), el mes (`month_cos` 0,022, `month_sin` 0,017), `balance` (0,020), `contact` (0,015), `housing` (0,014), `previous` (0,013), `previously_contacted` (0,012) y `age` (0,012). Los valores son bajos: ninguna variable sola explica la aceptación.
- **Variables casi irrelevantes** (información mutua < 0,001; 10 de 41): `job_management`, `job_services`, `job_technician`, `job_unemployed`, `job_entrepreneur`, `job_unknown`, `marital_divorced`, `poutcome_other`, `education_primary` y `default_yes`. Son candidatas a descartar, pero la medida es univariada: `job` en conjunto sí aporta (student, retired), por lo que conviene que la selección la valide un modelo.
- **PCA** sobre la matriz preprocesada: **14 componentes explican el 90 %** y **19 el 95 %** de la varianza (de 41 columnas). La redundancia viene de dummies complementarias (`housing_yes`/`housing_no`, `loan_yes`/`loan_no`, `poutcome_unknown` ≈ `previously_contacted`) y de `pdays`–`previous`. Los dos primeros componentes solo explican el 31,1 %, así que una proyección 2D pierde mucha información.
- **Estrategia propuesta para el componente supervisado:** comparar con validación cruzada (PR-AUC y F1) (a) todas las variables, (b) `SelectKBest` por información mutua con k = 20 y (c) PCA al 95 %. Esperamos que la selección por información mutua mantenga el rendimiento con la mitad de las variables y siga siendo interpretable, mientras que PCA reduce dimensiones sin una ganancia clara y pierde interpretabilidad.

## Alternativas consideradas
- **Agrupar categorías de `job`** con tasas parecidas (housemaid, entrepreneur y services, entre 8 y 9 %) para reducir dummies poco informativas. No se aplicó en la versión base para no perder detalle antes de ver qué selecciona el modelo.
- **Otro tratamiento de `unknown`:** imputarlo con la moda o eliminar filas. Se descartó porque en `poutcome` significa "no aplica" y en `contact` está asociado a una tasa muy baja. Riesgo de mantenerlo: en `contact` es un artefacto de registro (58 % de las llamadas de mayo y 85 % de las de junio, casi 0 % en el resto), así que el modelo podría aprender la época de la campaña en lugar del canal.
- **Otra codificación:** `OneHotEncoder(drop="if_binary")` para no duplicar binarias, tramos de edad o un término cuadrático para la relación en U, y codificación ordinal para `education`. Quedan como mejoras posibles si la selección de variables no basta.
