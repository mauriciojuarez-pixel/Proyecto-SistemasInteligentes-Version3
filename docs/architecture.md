
Proyecto_SistemasInteligentes_Version3/
│
├── app/                                   # Capa de Presentación (Interfaz de Usuario)
│   ├── main.py                            # Punto de entrada principal del sistema
│   ├── ui/                                # Interfaz gráfica (Tkinter / Streamlit)
│   │   ├── __init__.py
│   │   ├── window_main.py                 # Ventana principal (selección de archivos)
│   │   ├── dialog_settings.py             # Configuración avanzada (opcional)
│   │   └── progress_window.py             # Barra de progreso de ejecución
│   ├── styles/
│   │   ├── theme.json                     # Definición del tema visual (colores, fuentes)
│   │   └── icons/                         # Iconos e imágenes de la UI
│   └── assets/                            # Recursos visuales, plantillas y logos
│
├── core/                                  # Capa de Lógica y Control (Controlador)
│   ├── __init__.py
│   │
│   ├── controller/                        # Orquesta la interacción entre módulos
│   │   ├── __init__.py
│   │   ├── agent_controller.py            # Coordina el flujo de tareas del agente
│   │   ├── data_manager.py                # Gestiona carga, limpieza y validación de datos
│   │   ├── model_manager.py               # Maneja el fine-tuning del modelo Gemma
│   │   └── report_manager.py              # Supervisa la generación de reportes
│   │
│   ├── heavy_modules/                     # Módulos de IA, aprendizaje y análisis
│   │   ├── __init__.py
│   │   ├── agents/                        # Agente LangChain
│   │   │   ├── __init__.py
│   │   │   ├── chain_manager.py           # Orquestación de cadenas LangChain
│   │   │   ├── autonomous_agent.py        # Agente principal (razonamiento y planificación)
│   │   │   └── memory_manager.py          # Manejo de memoria y contexto
│   │   │
│   │   ├── fine_tuning/                   # Reentrenamiento del modelo Gemma 2B IT
│   │   │   ├── __init__.py
│   │   │   ├── data_preparation.py        # Limpieza y normalización previa al fine-tuning
│   │   │   ├── train_model.py             # Entrenamiento supervisado con nuevos datos
│   │   │   ├── evaluate_model.py          # Evaluación del modelo actualizado
│   │   │   └── model_saver.py             # Guardado y versionado del modelo fine-tuned
│   │   │
│   │   ├── analytics/                     # Análisis de datos y métricas
│   │   │   ├── __init__.py
│   │   │   ├── statistical_summary.py     # Estadísticos descriptivos
│   │   │   ├── correlation_analysis.py    # Correlaciones y outliers
│   │   │   └── anomaly_detection.py       # Limpieza avanzada y detección de ruido
│   │   │
│   │   └── reporting/                     # Generación automática de reportes
│   │       ├── __init__.py
│   │       ├── report_builder.py          # Estructura del reporte (texto, gráficos)
│   │       ├── export_pdf.py              # Generación de reporte final en PDF
│   │       ├── export_excel.py            # Exportación alternativa en Excel
│   │       └── metrics.py                 # Cálculo de métricas y KPIs personalizados
│   │
│   └── utils/                             # Herramientas auxiliares y funciones comunes
│       ├── __init__.py
│       ├── file_manager.py                # Validación de extensiones, lectura de CSV/Excel
│       ├── data_cleaner.py                # Eliminación de ruido, nulos y duplicados
│       ├── logger.py                      # Sistema de logs y seguimiento de ejecución
│       ├── time_utils.py                  # Control de tiempos de ejecución
│       └── helpers.py                     # Funciones generales (formatos, validaciones)
│
├── data/                                  # Capa de Datos (Modelo)
│   ├── datasets/
│   │   ├── raw/                           # Datos originales subidos por el usuario
│   │   ├── processed/                     # Datos limpios y listos para análisis
│   │   └── samples/                       # Ejemplos y datos de prueba
│   ├── models/
│   │   ├── gemma_2b_it_base/              # Modelo base preentrenado
│   │   ├── gemma_2b_it_finetuned/         # Versión fine-tuned personalizada
│   │   └── checkpoints/                   # Pesos intermedios del entrenamiento
│   ├── outputs/
│   │   ├── reports/                       # Reportes PDF generados
│   │   ├── logs/                          # Archivos de seguimiento del sistema
│   │   └── metrics/                       # Métricas en CSV o JSON
│
├── config/                                # Capa de Configuración
│   ├── __init__.py
│   ├── environments/
│   │   ├── development/
│   │   │   ├── settings.json              # Configuración local (modo dev)
│   │   │   ├── model_config.json          # Parámetros del modelo en desarrollo
│   │   │   └── ui_config.json             # Configuración visual para pruebas
│   │   ├── production/
│   │   │   ├── settings.json              # Configuración optimizada para producción
│   │   │   └── model_config.json
│   │   └── testing/
│   │       ├── settings.json              # Configuración para pruebas unitarias
│   │       └── model_config.json
│   ├── schemas/                           # Validaciones JSON
│   │   ├── data_schema.json
│   │   ├── report_schema.json
│   │   └── model_schema.json
│   └── defaults/
│       ├── default_paths.json             # Rutas predeterminadas del sistema
│       └── constants.json                 # Parámetros por defecto (limpieza, métricas)
│
├── scripts/                               # Scripts de automatización y soporte
│   ├── __init__.py
│   ├── setup_env.py                       # Verifica dependencias y entorno
│   ├── verify_requirements.py             # Comprueba librerías instaladas
│   ├── update_model.py                    # Descarga o actualiza el modelo Gemma
│   ├── generate_sample_data.py            # Crea datasets de prueba
│   ├── retrain_model.py                   # Reentrena Gemma 2B IT con datos procesados
│   └── build_exe.py                       # Genera ejecutable (.exe) con PyInstaller
│
├── tests/                                 # Capa de Pruebas
│   ├── __init__.py
│   ├── test_data_cleaning.py              # Pruebas del módulo de limpieza
│   ├── test_fine_tuning.py                # Pruebas del reentrenamiento Gemma
│   ├── test_reporting.py                  # Validación de reportes generados
│   └── test_agent_behavior.py             # Comportamiento del agente LangChain
│
├── docs/                                  # Documentación del Proyecto
│   ├── architecture.md                    # (Este documento)
│   ├── objectives.md                      # Objetivos principales y secundarios
│   ├── case_study.md                      # Descripción del caso de estudio
│   ├── flow_execution.md                  # Flujo de ejecución del sistema
│   ├── metrics_definition.md              # Definición de métricas y KPIs
│   ├── fine_tuning_notes.md               # Notas del entrenamiento del modelo
│   └── changelog.md                       # Historial de versiones
│
├── build_executable/                      # Capa de Empaquetado
│   ├── pyinstaller.spec                   # Configuración del ejecutable
│   ├── dist/                              # Binarios finales
│   └── temp/                              # Archivos temporales de compilación
│
├── requirements.txt                       # Dependencias del sistema
├── setup.py                               # Configuración de instalación
├── .env                                   # Variables de entorno (credenciales, paths)
├── .gitignore                             # Exclusión de archivos no versionables
└── README.md                              # Descripción general del proyecto



La arquitectura cumple con los **objetivos primarios y secundarios** del proyecto, garantizando:
- Automatización completa del flujo de análisis y reporte.  
- Aprendizaje continuo mediante fine-tuning del modelo Gemma 2B IT.  
- Generación de reportes enriquecidos con texto, gráficas y métricas.  
- Modularidad, escalabilidad y mantenibilidad.  
- Ejecución autónoma mediante un archivo ejecutable.  
- Configuración adaptable a entornos de desarrollo, pruebas y producción.

---