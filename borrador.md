data/
├── datasets/
│   ├── raw/                               # Datos originales subidos por el usuario
│   ├── processed/                         # Datos limpios listos para análisis
│   ├── versions/                          # Versiones asociadas a cada fine-tuning
│   │   ├── v1/
│   │   ├── v2/
│   │   └── v3/
│   └── samples/                           # Pequeños ejemplos de prueba
│
├── models/
│   ├── base/                              # Modelo base preentrenado (Gemma 2B IT)
│   ├── fine_tuned/                        # Modelos reentrenados por versión
│   │   ├── v1/
│   │   ├── v2/
│   │   └── latest/                        # Última versión activa del modelo
│   └── checkpoints/                       # Pesos intermedios (por cada entrenamiento)
│
├── outputs/
│   ├── reports/                           # Reportes PDF generados
│   │   ├── v1/
│   │   ├── v2/
│   │   └── comparisons/                   # Comparativas entre versiones
│   ├── logs/                              # Logs de ejecución y entrenamiento
│   └── metrics/                           # Métricas globales y por versión
│       ├── v1/
│       ├── v2/
│       └── summary_latest.json
