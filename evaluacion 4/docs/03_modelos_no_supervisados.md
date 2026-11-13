# Modelos no supervisados — justificación

Documento complementario de `notebooks/03_no_supervisado.ipynb` y `src/unsupervised.py`.

**Problema:** segmentar clientes por sus características y su historial de contacto, **sin usar `y`**.

## Preparación
Preprocesamiento ajustado con entrenamiento + PCA (~90 % de varianza). Con variables mixtas
(numéricas + one-hot) la distancia euclídea pierde sentido en alta dimensión; PCA reduce ese problema
a costa de perder parte de la información (documentar cuánta).

## Algoritmos

### K-Means
- **Supuestos:** clusters esféricos, de tamaño y densidad similares.
- **Ventajas:** rápido, fácil de interpretar. **Limitaciones:** hay que fijar k; sensible a escala y atípicos.
- **Optimización:** codo + Silhouette + Davies-Bouldin; estabilidad con distintas semillas (ARI).

### Mezcla gaussiana (GMM)
- **Supuestos:** los datos provienen de una mezcla de gaussianas.
- **Ventajas:** clusters elípticos, asignación probabilística. **Limitaciones:** más costoso y sensible a inicialización.
- **Optimización:** BIC/AIC por k y tipo de covarianza (full, diag, spherical).

### Clustering jerárquico
- **Supuestos:** clusters compactos (ward). **Ventajas:** no depende de inicialización; sirve para validar estabilidad.
- **Limitaciones:** O(n²) en memoria → se usa una muestra (el efecto del muestreo debe discutirse).
- **Optimización:** comparación de enlaces (ward, average, complete).

## Métricas
Silhouette (calculado sobre muestra), Davies-Bouldin, Calinski-Harabasz y acuerdo entre algoritmos (ARI).

## Comparación y selección
_(Completar: criterios usados para elegir el algoritmo y k final — métricas, estabilidad, interpretabilidad y
tamaño de los grupos.)_

## Perfiles y relación con la aceptación
_(Completar: nombre y descripción de cada segmento, tasa de aceptación por segmento, prueba chi-cuadrado
y recomendaciones de focalización de campañas.)_
