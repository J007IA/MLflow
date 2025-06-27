# 🧭 Objetivo del Proyecto

Construir un pipeline de Machine Learning que prediga la **fuga de clientes (churn o attrition)** en los próximos 6 meses y que sea **desplegado en AWS** con prácticas de **MLOps**: versionamiento, automatización, trazabilidad y escalabilidad.

---

## ✅ 1. Entendimiento del Negocio

- **Problema:** Alta tasa de fuga de clientes que afecta la rentabilidad del banco.  
- **Solución:** Modelo de predicción de fuga de clientes, para tomar acciones preventivas.  
- **Target:** Variable `attrition` (columna binaria: 1 si el cliente se fue, 0 si no).  
- **Horizonte de predicción:** 6 meses.  

---

## 🗃️ 2. Estructura de Datos

| Archivo                        | Contenido                                           |
|-------------------------------|-----------------------------------------------------|
| `train_clientes_sample.csv`   | Info estática de clientes         |
| `train_requerimientos_sample.csv` | Datos transaccionales                         |
| `oot_clientes_sample.csv`     | Clientes a predecir                   |
| `oot_requerimientos_sample.csv` | Datos transaccionales del mes actual            |
| `descripcion.xlsx`            | Diccionario de variables                           |

---

## 🧱 3. Arquitectura General del Pipeline

      +--------------------------+
      |    Recolección de datos  |
      +-----------+--------------+
                  |
    +-------------v-------------+
    |  Cruce de datos (cliente + transacciones)
    +-------------+-------------+
                  |
       +----------v----------+
       | Limpieza + Feature Engineering |
       +----------+----------+
                  |
       +----------v----------+
       | División Train/Test |
       +----------+----------+
                  |
       +----------v----------+
       | Entrenamiento de modelos |
       +----------+----------+
                  |
       +----------v----------+
       |  MLflow tracking + metrics  |
       +----------+----------+
                  |
       +----------v----------+
       |   Selección y registro del mejor modelo |
       +----------+----------+
                  |
       +----------v----------+
       |   Scoreo sobre datos OOT (inference)    |
       +----------+----------+
                  |
       +----------v----------+
       | Despliegue en AWS + CI/CD (GitHub Actions) |
       +-------------------+

---

## ⚙️ 4. Plan de Trabajo Técnico

### 🧪 Fase Offline

#### 🔄 Cruce y preparación del dataset
- Merge clientes con requerimientos (por ID o similar).
- Agregaciones temporales de variables transaccionales (ej: sumatorias mensuales, recencia, frecuencia).

#### 🧹 Preprocesamiento
- Imputación de nulos.
- Encoding de variables categóricas.
- Escalado de variables numéricas.


#### 🤖 Modelos
- Prueba con modelos base: Logistic Regression, Random Forest, XGBoost.
- Validación cruzada.
- Métricas: AUC, Recall, Precision, F1-score.

#### 📈 MLflow Tracking
- Log de hiperparámetros, métricas y artefactos.
- Versionamiento de modelos.

---

### 🚀 Fase Online (Despliegue)

#### 🏗️ Infraestructura
- **AWS Lambda o SageMaker:** para despliegue online.
- **GitHub Actions:** para CI/CD.

#### 📦 Pipelines
- **Entrenamiento:** activado por cambios en `develop` o por programación.
- **Inferencia batch:** lectura periódica de nuevos datos para scoring.
- **Inferencia online:** API para predicciones en tiempo real (opcional).


#### 🧠 Monitoreo (opcional avanzado)
- **Concept drift:** comparación entre distribución de features train vs OOT.
- **Data drift:** alertas por cambios fuertes en las variables.

---

## 🛠️ Herramientas y Librerías

| Etapa          | Tecnología sugerida                             |
|----------------|--------------------------------------------------|
| Datos          | `pandas`, `numpy`, `sqlalchemy`                  |
| Modelos        | `scikit-learn`, `xgboost`                        |
| Experimentos   | `MLflow`, `matplotlib`, `seaborn`                |
| Despliegue     | `AWS S3`, `Lambda`, `SageMaker`, `Docker`        |
| CI/CD          | `GitHub Actions`, `Git`, `Pytest`                |
| Infraestructura| `Terraform` o `AWS CLI` (opcional)               |
