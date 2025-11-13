# Documentación Técnica — Capa CORE

## Descripción general

La capa `core/` es el núcleo lógico del sistema, responsable de la coordinación, análisis inteligente, automatización, limpieza, fine-tuning y generación de reportes.  
Está compuesta por tres submódulos principales:

core/
│
├── controller/
├── heavy_modules/
└── utils/


---

## 1. controller/

Orquesta el flujo general del sistema. Cada módulo dentro de `controller/` actúa como coordinador de alto nivel, conectando la interfaz de usuario con los módulos de inteligencia artificial y de procesamiento de datos.

### 1.1 agent_controller.py

Controla el comportamiento general del agente LangChain, desde la carga de datos hasta la generación del reporte final.

| Función                                       | Descripción |
|----------|--------------|
| `initialize_agent()`                          | Configura el entorno y carga el agente autónomo. |
| `run_pipeline(file_path: str)`                | Ejecuta el flujo completo: carga → limpieza → análisis → reporte. |
| `delegate_task(task_name: str, params: dict)` | Asigna una tarea específica al módulo correspondiente. |
| `monitor_progress()`                          | Supervisa el estado de ejecución y comunica avances a la UI. |
| `get_agent_state()`                           | Devuelve el estado actual del agente (idle, running, training, error). |
| `reset_agent()`                               | Reinicia el agente y limpia memorias previas. |

---

### 1.2 data_manager.py

Gestiona los archivos cargados por el usuario (Excel/CSV), asegurando su validez, limpieza y compatibilidad con los análisis.

| Función                                   | Descripción |
|----------|--------------|
| `load_data(file_path: str)`               | Carga el dataset desde un archivo .csv o .xlsx. |
| `detect_file_type(file_path: str)`        | Determina el tipo de archivo (CSV o Excel). |
| `validate_structure(df: DataFrame)`       | Verifica que las columnas y tipos cumplan el `data_schema.json`. |
| `clean_data(df: DataFrame)`               | Llama al módulo `data_cleaner.py` para limpiar los datos. |
| `split_data(df: DataFrame)`               | Divide los datos en subconjuntos para entrenamiento y validación. |
| `save_processed(df: DataFrame)`           | Guarda los datos procesados en `data/datasets/processed/`. |
| `summarize_dataset(df: DataFrame)`        | Genera un resumen estadístico previo al análisis. |

---

### 1.3 model_manager.py

Controla el ciclo de vida del modelo Gemma 2B IT: carga, fine-tuning, evaluación y versionado.

| Función                                       | Descripción |
|----------|--------------|
| `load_model(version='latest')`                        | Carga el modelo base o el último modelo fine-tuned. |
| `prepare_data_for_finetuning(df: DataFrame)`          | Preprocesa los datos para entrenamiento (normalización, tokenización). |
| `fine_tune(data_path: str, epochs=3)`                 | Ejecuta el proceso de reentrenamiento supervisado. |
| `evaluate_model(metrics: list)`                       | Evalúa el desempeño del modelo usando métricas ad hoc. |
| `compare_versions(old_model, new_model)`              | Compara resultados entre versiones para decidir cuál conservar. |
| `save_model_checkpoint(name='fine_tuned_latest')`     | Guarda los pesos entrenados y genera un registro en `models/checkpoints/`. |
| `load_fine_tuned_model()`                             | Carga el modelo más reciente ya ajustado. |
| `rollback_to_previous_version()`                      | Restaura la versión anterior del modelo si el nuevo falla. |

---

### 1.4 report_manager.py

Supervisa la generación completa del reporte (texto, gráficos, métricas y conclusiones).

| Función                                                   | Descripción |
|----------|--------------|
| `generate_report(data: DataFrame, insights: dict)`        | Crea un reporte a partir de los resultados del análisis. |
| `add_visualizations(data: DataFrame)`                     | Genera gráficos y visualizaciones con matplotlib o plotly. |
| `compile_sections(analysis, graphs, summary)`             | Une los distintos componentes (texto, métricas, figuras). |
| `export_to_pdf(output_path: str)`                         | Llama a `export_pdf.py` para crear el archivo final. |
| `export_to_excel(output_path: str)`                       | Llama a `export_excel.py` para exportar resultados tabulares. |
| `append_metadata(info: dict)`                             | Añade metadatos del modelo, dataset y ejecución al reporte. |
| `auto_name_report()`                                      | Genera automáticamente el nombre del archivo de salida (`report_YYYYMMDD.pdf`). |

---

## 2. heavy_modules/

Agrupa los módulos de inteligencia: agentes, análisis, fine-tuning y reporting.  
Aquí se encuentra toda la lógica autónoma, analítica y de aprendizaje.

---

### 2.1 agents/

Define la inteligencia autónoma del sistema mediante LangChain.

#### chain_manager.py

| Función                                   | Descripción |
|----------|--------------|
| `build_chain()`                           | Define la secuencia de pasos (input → análisis → resumen → reporte). |
| `execute_chain(data: DataFrame)`          | Ejecuta la cadena sobre los datos cargados. |
| `inject_context(memory: dict)`            | Inyecta contexto previo del agente (memoria). |
| `trace_chain()`                           | Devuelve un registro paso a paso de la ejecución. |

#### autonomous_agent.py

| Función                                       | Descripción |
|----------|--------------|
| `plan_actions(goal: str)`                     | Define un plan de acciones para alcanzar un objetivo dado. |
| `analyze_data(df: DataFrame)`                 | Interpreta los datos y genera hallazgos clave. |
| `decide_next_step()`                          | Decide automáticamente el siguiente paso de la cadena. |
| `generate_summary(analysis: dict)`            | Genera un resumen textual con el modelo Gemma. |
| `self_optimize()`                             | Ajusta los parámetros internos según resultados previos. |

#### memory_manager.py

| Función                                       | Descripción |
|----------|--------------|
| `store_context(session_id, info)`             | Guarda información relevante entre ejecuciones. |
| `recall_context(session_id)`                  | Recupera contexto previo de ejecución. |
| `clear_memory(session_id)`                    | Limpia la memoria de sesión. |

---

### 2.2 fine_tuning/

Entrenamiento y mejora del modelo Gemma con nuevos datos.

| Módulo                                | Funciones principales |
|---------|------------------------|
| `data_preparation.py`                 | `clean_training_data()`, `tokenize_texts()`, `balance_classes()`, `split_train_test()` |
| `train_model.py`                      | `initialize_trainer()`, `train(epochs, batch_size)`, `track_progress()`, `log_results()` |
| `evaluate_model.py`                   | `compute_metrics()`, `compare_with_baseline()`, `generate_evaluation_report()` |
| `model_saver.py`                      | `save_checkpoint()`, `list_model_versions()`, `load_checkpoint(version)`, `delete_old_models()` |

---

### 2.3 analytics/

Módulos de análisis estadístico, correlaciones y detección de anomalías.

| Módulo                                        | Funciones principales |
|---------|------------------------|
| `statistical_summary.py`                      | `compute_descriptive_stats()`, `generate_histograms()`, `summary_to_json()` |
| `correlation_analysis.py`                     | `compute_correlations()`, `detect_multicollinearity()`, `visualize_correlation_matrix()` |
| `anomaly_detection.py`                        | `detect_outliers()`, `remove_anomalies()`, `flag_noisy_data()`, `score_data_quality()` |

---

### 2.4 reporting/

Construcción y exportación del reporte final enriquecido con IA.

| Módulo                            | Funciones principales |
|---------|------------------------|
| `report_builder.py`               | `build_structure()`, `add_text_sections()`, `embed_charts()`, `insert_metrics()`, `finalize_report()` |
| `export_pdf.py`                   | `create_pdf()`, `add_images()`, `add_table()`, `save_pdf()` |
| `export_excel.py`                 | `create_excel_summary()`, `export_sheets()`, `save_excel()` |
| `metrics.py`                      | `calculate_custom_metrics()`, `evaluate_model_performance()`, `summarize_results()` |

---

## 3. utils/

Módulos de soporte general, usados por todos los demás componentes.

| Módulo                        | Funciones principales |
|---------|------------------------|
| `file_manager.py`             | `validate_path()`, `load_csv()`, `load_excel()`, `save_file()`, `get_filename()` |
| `data_cleaner.py`             | `remove_nulls()`, `remove_duplicates()`, `normalize_columns()`, `detect_noise()`, `save_clean_data()` |
| `logger.py`                   | `init_logger()`, `log_info()`, `log_warning()`, `log_error()`, `save_log()` |
| `time_utils.py`               | `start_timer()`, `stop_timer()`, `elapsed_time()`, `log_execution_time()` |
| `helpers.py`                  | `format_number()`, `format_date()`, `generate_id()`, `safe_division()`, `normalize_string()` |

---

## Conclusión

La capa `core/` proporciona la base lógica y funcional del sistema.  
Su diseño modular garantiza independencia entre componentes, escalabilidad del sistema y soporte para tareas autónomas, análisis inteligente y generación de reportes sin intervención manual.
