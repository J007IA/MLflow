# GitHub Actions ML Pipeline Setup

Este documento explica cómo configurar y usar el pipeline de ML automatizado con GitHub Actions.

## Descripción del Pipeline

El pipeline automatizado ejecuta las siguientes etapas:

1. **Preprocesamiento de Datos**: Ejecuta `src/train-pre-process.py` para generar características de clientes
2. **Entrenamiento del Modelo**: Ejecuta `src/model_training.py` para entrenar un modelo Random Forest con SMOTE
3. **Registro en MLflow**: Guarda experimentos y artefactos en MLflow con almacenamiento S3
4. **Reportes y Artefactos**: Genera reportes de rendimiento y guarda artefactos

## Configuración Requerida

### 1. GitHub Secrets

Para que el pipeline funcione, necesitas configurar los siguientes secrets en tu repositorio de GitHub:

```
AWS_ACCESS_KEY_ID: Tu AWS Access Key ID
AWS_SECRET_ACCESS_KEY: Tu AWS Secret Access Key  
AWS_DEFAULT_REGION: us-west-1 (o tu región preferida)
```

**Cómo agregar secrets:**
1. Ve a tu repositorio en GitHub
2. Haz clic en "Settings"
3. En el menú lateral, haz clic en "Secrets and variables" → "Actions"
4. Haz clic en "New repository secret"
5. Agrega cada secret con su nombre y valor correspondiente

### 2. Estructura de Archivos

Asegúrate de que tu repositorio tenga la siguiente estructura:

```
MLflow/
├── .github/
│   └── workflows/
│       └── ml-pipeline.yml
├── src/
│   ├── train-pre-process.py
│   └── model_training.py
├── exploration-part/
│   └── data/
│       ├── raw/
│       │   ├── train_clientes_sample.csv
│       │   └── train_requerimientos_sample.csv
│       └── pre-processed/
└── requirements.txt
```

### 3. Configuración de MLflow

El pipeline está configurado para usar:
- **Servidor de Tracking**: SageMaker MLflow Server
- **Almacenamiento de Artefactos**: S3 (bucket: `myawsbucket.3.2025`)
- **Experimento**: `Customer_Churn_Production`

## Ejecución del Pipeline

### Ejecución Automática

El pipeline se ejecuta automáticamente cuando:
- Se hace push a las ramas `main` o `feature/add-actions`
- Se crea un pull request hacia `main`

### Ejecución Manual

También puedes ejecutar el pipeline manualmente:
1. Ve a la pestaña "Actions" en tu repositorio
2. Selecciona "ML Pipeline - Data Processing and Model Training"
3. Haz clic en "Run workflow"
4. Selecciona la rama y haz clic en "Run workflow"

## Resultado del Pipeline

### Artefactos Generados

- **Datos Preprocesados**: `exploration-part/data/pre-processed/train_clientes_features.csv`
- **Métricas del Modelo**: Registradas en MLflow
- **Reportes**: Matriz de confusión, importancia de características
- **Artefactos S3**: Almacenados en el bucket configurado

### Métricas Reportadas

El pipeline registra las siguientes métricas:
- **AUC Score**: Área bajo la curva ROC
- **F1 Score**: Puntuación F1
- **Recall**: Sensibilidad
- **Precision**: Precisión

### Visualización de Resultados

1. **GitHub Actions**: Ve el resumen de ejecución en la pestaña Actions
2. **MLflow UI**: Accede al servidor MLflow para ver experimentos detallados
3. **S3 Bucket**: Revisa los artefactos almacenados

## Solución de Problemas

### Errores Comunes

1. **"AWS credentials not configured"**
   - Verifica que los secrets de AWS estén configurados correctamente
   - Asegúrate de que las credenciales tengan permisos para S3

2. **"Input data files not found"**
   - Verifica que los archivos CSV estén en `exploration-part/data/raw/`
   - Confirma que los nombres de archivo coincidan exactamente

3. **"MLflow tracking server connection failed"**
   - Verifica la configuración del servidor MLflow
   - Confirma que el bucket S3 exista y sea accesible

### Logs y Debugging

- Revisa los logs detallados en la pestaña "Actions" de GitHub
- Cada paso del pipeline tiene logs específicos para debugging
- Los artefactos se guardan incluso si el pipeline falla

## Personalización

### Modificar Parámetros del Modelo

Edita `src/model_training.py` para cambiar:
- Hiperparámetros del Random Forest
- Configuración de SMOTE
- Métricas de evaluación

### Cambiar Configuración de AWS

Modifica las variables de entorno en `src/model_training.py`:
- Servidor MLflow
- Bucket S3
- Región AWS

### Agregar Nuevas Etapas

Modifica `.github/workflows/ml-pipeline.yml` para:
- Agregar nuevos pasos de preprocesamiento
- Incluir validación de datos
- Agregar notificaciones

## Monitoreo y Mantenimiento

### Revisión Regular

- Revisa los logs de ejecución mensualmente
- Verifica que las credenciales AWS no hayan expirado
- Monitorea el uso del bucket S3

### Actualizaciones

- Actualiza las dependencias en `requirements.txt` regularmente
- Revisa y actualiza los parámetros del modelo según sea necesario
- Mantén actualizada la configuración de MLflow

## Contacto y Soporte

Para problemas o preguntas sobre el pipeline:
1. Revisa este documento y los logs de GitHub Actions
2. Verifica la configuración de AWS y MLflow
3. Consulta la documentación de MLflow y scikit-learn 