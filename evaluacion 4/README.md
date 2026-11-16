# Evaluación 4 — Predicción de contratación de productos financieros y segmentación de clientes

**Asignatura:** Análisis de Datos · **Docente:** Daniel Alexis Nieto Mora
**Carrera:** Ingeniería en Ciencia de Datos · **Grupo:** 190304018-1 · **Periodo:** 2026-2
**Equipo 4** · Entrega: viernes 13 de noviembre de 2026
**Repositorio:** https://github.com/JuanaOsp28/uber-fares-bi (esta evaluación vive en la carpeta `evaluacion 4`;
el resto del repositorio corresponde a la actividad anterior sobre tarifas de Uber).

## Integrantes

| Integrante 
|---
| Víctor Manuel David Rodríguez 
| David Viloria 
| Samuel Metaute Restrepo 
| Juana Ospina 

## 1. Descripción del problema

Una institución financiera realiza campañas telefónicas para ofrecer un **depósito a plazo**.
El proyecto aborda dos preguntas complementarias con el *Bank Marketing Dataset* (UCI):

- **Supervisado:** ¿se puede predecir si un cliente aceptará la oferta (`y`)? ¿Qué características
  demográficas, financieras y de campaña influyen más?
- **No supervisado:** ¿existen perfiles de clientes con comportamientos similares? ¿Cómo se
  relacionan esos segmentos con la aceptación del producto?

## 2. Estructura del proyecto

```
evaluacion 4/
├── README.md                     # Este archivo
├── requirements.txt              # Dependencias
├── data/
│   ├── README.md                 # Fuente y diccionario de datos
│   └── raw/                      # CSV (no se sube a Git)
├── src/
│   ├── config.py                 # Rutas, semilla, objetivo, columnas con fuga
│   ├── data_loader.py            # Descarga, carga y partición train/test
│   ├── preprocessing.py          # Pipeline de preprocesamiento
│   ├── supervised.py             # Modelos, selección de variables, optimización y métricas
│   └── unsupervised.py           # Clustering, optimización, estabilidad y perfiles
├── notebooks/
│   ├── 01_eda.ipynb              # Exploración, preprocesamiento y relevancia de variables
│   ├── 02_supervisado.ipynb      # Clasificación
│   └── 03_no_supervisado.ipynb   # Segmentación
├── docs/
│   ├── 01_eda_y_preprocesamiento.md
│   ├── 02_modelos_supervisados.md
│   ├── 03_modelos_no_supervisados.md
│   └── 04_analisis_comparativo.md
├── reports/
│   ├── figures/                  # Gráficas generadas
│   └── results/                  # Tablas de métricas (CSV)
└── video/
    └── presentacion_equipo4.mp4  # Video de presentación del equipo
```

## 3. Instrucciones de ejecución

```bash
cd "evaluacion 4"
python -m venv .venv
.venv\Scripts\activate            # En Linux/Mac: source .venv/bin/activate
pip install -r requirements.txt
python -c "from src.data_loader import download_dataset; download_dataset()"
jupyter notebook
```

Ejecutar los notebooks en orden: `01_eda` → `02_supervisado` → `03_no_supervisado`.
Los notebooks se ejecutan **desde la carpeta `notebooks/`** (ya incluyen el ajuste de ruta).
El notebook supervisado incluye una búsqueda de hiperparámetros que puede tardar varios minutos.

## 4. Fuentes de datos

- Moro, S., Rita, P. & Cortez, P. (2014). *Bank Marketing*. UCI Machine Learning Repository.
  https://archive.ics.uci.edu/dataset/222/bank+marketing

## 5. Decisiones técnicas clave

- **Sin fuga de información:** se excluye `duration` (solo se conoce tras la llamada) y todos los
  ajustes (imputación, escalado, codificación, selección de variables, PCA) se aprenden únicamente con el
  conjunto de entrenamiento, dentro de `Pipeline`.
- **Partición única** estratificada 80/20 con semilla 42 (`src/data_loader.py`), compartida por todos.
- **Desbalance (~11,7 % "yes"):** pesos de clase; se evalúa con F1, Recall, Precision, ROC-AUC y PR-AUC.
- **Selección de variables y reducción de dimensionalidad:** información mutua, L1 y PCA, comparadas con CV.
- **Optimización:** búsqueda aleatoria de hiperparámetros (supervisado); BIC, enlaces y estabilidad (no supervisado).
- En el componente no supervisado **no se usa `y`** como entrada; solo se usa después para interpretar.

## 6. Principales resultados

**Componente supervisado** (conjunto de prueba, modelos optimizados; detalle en `notebooks/02_supervisado.ipynb`):

| Modelo supervisado | Precision | Recall | F1 | ROC-AUC | PR-AUC |
|---|---|---|---|---|---|
| Regresión logística | 0,235 | 0,680 | 0,349 | 0,756 | 0,373 |
| Random Forest | 0,486 | 0,493 | 0,490 | 0,806 | 0,461 |
| **Gradient Boosting (elegido)** | 0,353 | 0,646 | 0,457 | 0,806 | **0,467** |

Se eligió **Gradient Boosting** por el mayor PR-AUC y un recall mucho más alto que Random Forest (encuentra el 64,6 %
de los clientes que aceptan). Llamando solo a los clientes con probabilidad ≥ 0,5 se hacen 79 % menos llamadas y la
ganancia estimada pasa de 1.537 a 4.897. Las variables más influyentes son el mes, el tipo de contacto y el resultado
de la campaña anterior.

**Componente no supervisado** (detalle en `notebooks/03_no_supervisado.ipynb`):

| Algoritmo de clustering | k | Silhouette | Davies-Bouldin |
|---|---|---|---|
| **K-Means (elegido)** | 4 | 0,164 | 1,906 |
| Mezcla gaussiana | 4 | 0,090 | 3,702 |
| Jerárquico Ward (muestra) | 4 | 0,164 | 1,861 |

K-Means encontró cuatro segmentos con aceptaciones muy distintas: clientes nuevos sin canal registrado (9,0 %), nuevos
de verano contactados por celular (9,5 %), recontactados con campaña fallida (13,4 %) y **recontactados recientes con
historial positivo (29,8 %)**, frente a una tasa global de 11,7 %.

**Conclusión conjunta:** los dos enfoques coinciden en que la aceptación depende sobre todo de la campaña y del
historial de contacto, no del perfil demográfico. El modelo supervisado sirve para **priorizar a quién llamar** y la
segmentación para **personalizar canal, momento y oferta**. Análisis completo en `docs/04_analisis_comparativo.md`.

## 7. Video de presentación

Video del equipo (11 min 53 s): [`video/presentacion_equipo4.mp4`](video/presentacion_equipo4.mp4)
