test/
├── __init__.py
├── test_data_manager.py          # Unit tests para core.controller.data_manager
├── test_model_manager.py         # Unit tests para core.controller.model_manager
├── test_report_manager.py        # Unit tests para core.controller.report_manager
├── test_prompt_builder.py        # Unit tests para core.utils.prompt_builder
├── test_scripts_integration.py   # Tests de integración para scripts/ (auto_clean_data, generate_report_auto, etc.)
├── sample_data/                  # Datasets de prueba (CSV/XLSX)
│   ├── sample1.csv
│   └── sample2.xlsx
└── logs/                         # Logs de pruebas


a) test_data_manager.py

    Prueba la limpieza, validación y guardado de datasets.

    Verifica que los DataFrames se carguen correctamente desde CSV y Excel.

    Comprueba que los datos procesados estén consistentes.

b) test_model_manager.py

    Prueba carga del modelo base y fine-tuned.

    Verifica generate_from_prompt con un DataFrame de prueba.

    Testea fine-tuning y rollback.

    Comprueba evaluación y versionado del modelo.

c) test_report_manager.py

    Prueba que ReportManager genere reportes completos.

    Verifica inserción de métricas, gráficos y secciones de texto.

    Comprueba exportación a PDF y Excel.

d) test_prompt_builder.py

    Prueba que BuilderPrompt genere prompts correctos a partir de DataFrames de distintos tipos de columnas.

    Verifica que detecte nombres y tipos de columnas automáticamente.

e) test_scripts_integration.py

    Simula la ejecución de tus scripts principales (auto_clean_data.py, generate_report_auto.py, manage_training.py, etc.) usando datasets de sample_data/.

    Verifica que cada script funcione sin errores y que el flujo completo de limpieza → análisis → reporte → entrenamiento funcione.