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
- **k final = 4.** El Silhouette máximo (k = 2, 0,305) solo separa clientes contactados antes de los nuevos; entre k = 4
  y k = 6 las métricas casi no cambian (Silhouette 0,164–0,172) y k = 4 da segmentos interpretables con tamaños útiles
  (el menor tiene el 7,7 %).
- **Algoritmo final: K-Means.** Con k = 4 obtiene el mejor Davies-Bouldin (1,91) y Calinski-Harabasz (6.262) y un
  Silhouette igual al jerárquico (0,164); GMM queda por debajo (Silhouette 0,090). Es estable entre semillas
  (ARI medio 0,79).
- **GMM:** el BIC prefiere covarianza *full* con k = 7: describe mejor la densidad, pero con componentes difíciles de
  interpretar como segmentos.
- **Jerárquico:** *average* y *complete* dejan un cluster con más del 80 % de los clientes; *ward* es el único que
  produce grupos equilibrados. El acuerdo con K-Means es moderado (ARI = 0,35 en la muestra; 0,55 con GMM).
- El Silhouette bajo indica un continuo de clientes más que grupos muy separados: los segmentos se usan como resumen
  útil para la campaña.

## Perfiles y relación con la aceptación

| Cluster | Segmento | Tamaño | Aceptación |
|---|---|---|---|
| 0 | Nuevos sin canal registrado (mayo-junio, con hipoteca, *blue-collar*) | 45,6 % | 9,0 % |
| 1 | Nuevos de verano contactados por celular (sin hipoteca, *management*) | 36,2 % | 9,5 % |
| 2 | Recontactados antiguos con campaña fallida (`pdays` ≈ 337) | 7,7 % | 13,4 % |
| 3 | Recontactados recientes con historial positivo (mayor balance) | 10,5 % | **29,8 %** |

Tasa global de aceptación: 11,7 %. La relación entre segmento y aceptación es significativa (chi-cuadrado = 1.392,
p ≈ 1,6·10⁻³⁰¹).

**Recomendaciones de focalización:** priorizar el segmento 3 con recontacto temprano y pocas llamadas; contactar a los
clientes nuevos por celular (14,8 % de aceptación frente a 4,1 % con canal desconocido) y fuera de mayo (6,7 %);
registrar el canal de contacto del segmento 0; y cambiar la oferta para los
recontactados con campañas fallidas.
