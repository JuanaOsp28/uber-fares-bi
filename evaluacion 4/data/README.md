# Datos

**Dataset:** Bank Marketing (UCI Machine Learning Repository, id 222)
**Enlace:** https://archive.ics.uci.edu/dataset/222/bank+marketing

Campañas de marketing directo (llamadas telefónicas) de un banco portugués para
ofrecer un depósito a plazo. Objetivo: predecir si el cliente suscribe (`y`).

## Cómo obtenerlo

Opción automática (desde la carpeta `evaluacion 4`):

```bash
python -c "from src.data_loader import download_dataset; download_dataset()"
```

Opción manual: descargar el zip de UCI, extraer `bank.zip` y copiar `bank-full.csv`
en `data/raw/`. Los datos **no se suben al repositorio** (ver `.gitignore`).

## Variables de `bank-full.csv` (45.211 filas, 16 variables + objetivo)

| Variable | Tipo | Descripción |
|---|---|---|
| age | numérica | Edad del cliente |
| job | categórica | Tipo de empleo |
| marital | categórica | Estado civil |
| education | categórica | Nivel educativo |
| default | categórica | ¿Tiene crédito en mora? |
| balance | numérica | Saldo medio anual (euros) |
| housing | categórica | ¿Tiene crédito de vivienda? |
| loan | categórica | ¿Tiene préstamo personal? |
| contact | categórica | Canal de contacto (cellular, telephone, unknown) |
| day | numérica | Día del mes del último contacto |
| month | categórica | Mes del último contacto |
| duration | numérica | Duración de la última llamada (segundos) — **se excluye (fuga de información)** |
| campaign | numérica | Nº de contactos en esta campaña |
| pdays | numérica | Días desde el contacto en una campaña anterior (-1 = no contactado antes) |
| previous | numérica | Nº de contactos antes de esta campaña |
| poutcome | categórica | Resultado de la campaña anterior |
| **y** | objetivo | ¿Suscribió el depósito a plazo? (yes/no) |

> Nota: el objetivo está desbalanceado (~11,7 % de "yes").
