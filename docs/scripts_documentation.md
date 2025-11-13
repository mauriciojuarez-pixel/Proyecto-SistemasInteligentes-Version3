# Documentación Técnica — Capa SCRIPTS

**Versión:** 1.0  
**Última actualización:** 12/11/2025  
**Autor:** Mauricio Juárez Zeballos  

---

## Descripción general

La carpeta `scripts/` contiene **módulos auxiliares y automatizados** que permiten inicializar, mantener, entrenar y desplegar el sistema de forma controlada.  
A diferencia de la capa `core/`, aquí se ubican scripts **independientes** que pueden ejecutarse directamente desde la terminal o desde la interfaz principal (`main.py`) para realizar tareas específicas como:

- Preparación del entorno.
- Verificación de dependencias.
- Limpieza y preprocesamiento de datos.
- Reentrenamiento del modelo Gemma 2B IT (fine-tuning).
- Generación automática de reportes.
- Construcción del ejecutable (.exe).

---

## Estructura de la carpeta

scripts/
├── init.py
├── setup_env.py
├── verify_requirements.py
├── update_model.py
├── train_finetune.py
├── auto_clean_data.py
├── generate_report_auto.py
├── generate_sample_data.py
└── build_exe.py


---

## 1. setup_env.py

Script encargado de **configurar el entorno de ejecución** inicial.

### Funciones principales

| Función | Descripción |
|----------|--------------|
| `check_environment()` | Verifica la versión de Python y librerías críticas. |
| `init_directories()` | Crea las carpetas base en `data/`, `models/` y `outputs/` si no existen. |
| `load_env_variables()` | Carga y valida las variables del archivo `.env`. |
| `verify_gpu()` | Comprueba si hay GPU disponible para entrenamiento. |
| `summary()` | Muestra un resumen general del entorno configurado. |

---

## 2. verify_requirements.py

Verifica la **instalación de librerías** requeridas y versiones compatibles.

### Funciones principales

| Función | Descripción |
|----------|--------------|
| `read_requirements()` | Lee el archivo `requirements.txt`. |
| `check_libraries()` | Comprueba si las librerías están instaladas correctamente. |
| `install_missing()` | Instala automáticamente los paquetes faltantes. |
| `report_results()` | Muestra el resultado de la verificación en consola. |

---

## 3. update_model.py

Administra la **descarga, actualización o restauración** del modelo Gemma 2B IT.

### Funciones principales

| Función | Descripción |
|----------|--------------|
| `download_base_model()` | Descarga la versión base del modelo (`gemma_2b_it_base`). |
| `update_finetuned_model()` | Sustituye el modelo fine-tuned actual por una nueva versión entrenada. |
| `rollback_model()` | Permite restaurar un checkpoint anterior si el nuevo modelo falla. |
| `verify_model_integrity()` | Valida pesos, estructura y metadatos del modelo. |
| `log_update()` | Registra los cambios en el historial de versiones. |

---

## 4. train_finetune.py

Ejecuta el **proceso de reentrenamiento (fine-tuning)** del modelo Gemma 2B IT  
usando los datos procesados ubicados en `data/datasets/processed/`.

### Funciones principales

| Función | Descripción |
|----------|--------------|
| `load_processed_data()` | Carga los datos limpios generados por el sistema. |
| `prepare_training_data()` | Tokeniza, balancea y normaliza los datos. |
| `train_model(epochs=3, batch_size=32)` | Inicia el entrenamiento supervisado. |
| `evaluate_model()` | Calcula métricas personalizadas sobre el modelo entrenado. |
| `save_finetuned_model()` | Guarda la versión ajustada en `data/models/gemma_2b_it_finetuned/`. |
| `generate_training_report()` | Genera un reporte con resultados de métricas y desempeño. |

---

## 5. auto_clean_data.py

Realiza la **limpieza automática** de los datasets originales (ubicados en `data/datasets/raw/`),  
preparándolos para la fase de análisis y entrenamiento.

### Funciones principales

| Función | Descripción |
|----------|--------------|
| `scan_raw_folder()` | Busca archivos `.csv` y `.xlsx` nuevos. |
| `clean_dataset(file_path)` | Elimina nulos, duplicados y ruido. |
| `normalize_data(df)` | Estandariza columnas y tipos de datos. |
| `save_processed(df)` | Guarda los resultados limpios en `data/datasets/processed/`. |
| `log_cleaning_results()` | Crea un registro del proceso en `data/outputs/logs/`. |

---

## 6. generate_report_auto.py

Script encargado de la **generación automática de reportes** en PDF y Excel  
sin necesidad de intervención del usuario.

### Funciones principales

| Función | Descripción |
|----------|--------------|
| `load_clean_data()` | Carga los datos ya procesados. |
| `analyze_data()` | Aplica análisis estadístico y genera correlaciones. |
| `generate_ai_insights()` | Llama al modelo Gemma 2B IT para producir conclusiones automáticas. |
| `create_visualizations()` | Construye gráficos para incluir en el reporte. |
| `export_final_report()` | Genera el reporte en PDF (y opcionalmente en Excel). |
| `archive_report()` | Guarda el reporte en `data/outputs/reports/`. |

---

## 7. generate_sample_data.py

Crea **datasets sintéticos o de prueba** para validar el pipeline de análisis.

### Funciones principales

| Función | Descripción |
|----------|--------------|
| `generate_csv(rows=1000)` | Genera un dataset aleatorio en formato CSV. |
| `generate_excel(rows=1000)` | Crea un archivo Excel con valores aleatorios. |
| `add_noise()` | Introduce ruido controlado para pruebas de limpieza. |
| `save_samples()` | Almacena los datos en `data/datasets/samples/`. |

---

## 8. build_exe.py

Empaqueta todo el proyecto en un **ejecutable (.exe)** listo para distribución con PyInstaller.

### Funciones principales

| Función | Descripción |
|----------|--------------|
| `prepare_build()` | Limpia la carpeta temporal y prepara dependencias. |
| `compile_with_pyinstaller()` | Llama a PyInstaller con las opciones configuradas. |
| `move_executable()` | Mueve el ejecutable a `build_executable/dist/`. |
| `verify_build()` | Comprueba la integridad del ejecutable generado. |
| `cleanup()` | Elimina archivos temporales post compilación. |

---

## 9. Conclusión

Los scripts del sistema permiten **automatizar completamente el ciclo de vida del proyecto**, desde la limpieza de datos y reentrenamiento del modelo, hasta la generación de reportes y la construcción del ejecutable final.  
Cada script puede ejecutarse individualmente o ser invocado por el agente principal dentro del flujo orquestado por la capa `core/controller/`.

---

