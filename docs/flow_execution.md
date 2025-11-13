Flujo General del Sistema — Proyecto_Maquiña
1. Inicio del Sistema

    El usuario ejecuta el archivo Proyecto_Maquiña.exe (o corre python app/main.py en modo desarrollo).

    El sistema inicia la interfaz de usuario (app/ui/window_main.py).

    El agente se inicializa internamente: se carga la configuración de entorno desde config/environments/ y el modelo Gemma 2B IT (base o fine-tuned) desde data/models/.

2. Selección del Archivo

    El usuario selecciona un archivo Excel o CSV mediante la interfaz.
    El sistema verifica el formato con utils/file_manager.py.

    Si el archivo no es válido, se muestra un mensaje de error.

    Si es válido, se copia automáticamente a data/datasets/raw/ y se notifica al agente que hay una nueva fuente de datos disponible.

3. Activación del Agente Autónomo (LangChain)

    El agente principal (core/heavy_modules/agents/autonomous_agent.py) recibe el evento de nuevo dataset.

    El agente planifica las tareas necesarias sin intervención del usuario.
    Ejemplo de planificación interna:

    Tarea 1: Validar formato del dataset
    Tarea 2: Limpiar datos y eliminar ruido
    Tarea 3: Generar análisis estadístico y correlacional
    Tarea 4: Detectar anomalías
    Tarea 5: Crear visualizaciones y métricas
    Tarea 6: Redactar reporte en lenguaje natural (con Gemma)
    Tarea 7: Exportar a PDF


    El agente inicia la ejecución secuencial de estas tareas usando LangChain Chains y Tools (definidas en chain_manager.py).

4. Limpieza y Validación de Datos

    Se ejecuta el módulo core/utils/data_cleaner.py:

    Elimina duplicados, nulos y valores inconsistentes.

    Corrige tipos de datos (fechas, numéricos, categóricos).

    Detecta valores atípicos con analytics/anomaly_detection.py.

    El resultado limpio se guarda en data/datasets/processed/.

5. Análisis y Generación de Métricas

    El agente invoca el módulo analytics/statistical_summary.py y correlation_analysis.py:

    Calcula promedios, medianas, desviaciones estándar, correlaciones y tendencias.

    Extrae insights clave para el reporte.

    Las métricas ad hoc se calculan con reporting/metrics.py.
    Ejemplo:

        Eficiencia de limpieza de datos.

        Nivel de ruido eliminado (%).

        Precisión del modelo en predicciones internas.

        Todos los resultados se registran en data/outputs/metrics/.

6. Generación de Gráficos y Visualizaciones

    El módulo reporting/report_builder.py genera gráficos automáticos:

    Histogramas, boxplots, correlaciones y distribuciones.

    Se usa matplotlib o plotly para renderizar visualmente los resultados.

    Las imágenes se almacenan temporalmente en data/outputs/reports/temp/ antes de incrustarse en el PDF.

7. Redacción Inteligente del Reporte (Gemma 2B IT)

    El agente pasa los resultados procesados al modelo Gemma 2B IT (vía model_manager.py).

    El modelo redacta secciones del reporte con lenguaje natural:

    Introducción (tipo de dataset, variables, contexto).

    Análisis descriptivo y observaciones clave.

    Conclusiones automáticas basadas en correlaciones o patrones detectados.

    Esta parte puede mejorar progresivamente mediante fine-tuning manual con nuevos datasets.

8. Fine-Tuning (Reentrenamiento del Modelo)

    (Acción opcional y controlada manualmente por el desarrollador dentro del código)

    Desde heavy_modules/fine_tuning/train_model.py, el programador puede ejecutar:

    python core/heavy_modules/fine_tuning/train_model.py


    El script usa los datos limpios de data/datasets/processed/ para reentrenar Gemma 2B IT.

    El modelo actualizado se guarda en data/models/gemma_2b_it_finetuned/.

    El agente puede detectar automáticamente nuevas versiones del modelo y utilizarlas para mejorar la redacción de futuros reportes.

9. Generación del Reporte Final

    El módulo reporting/export_pdf.py compila toda la información:

    Datos limpios.

    Gráficos.

    Métricas.

    Texto interpretativo generado por el modelo.

    Se crea un PDF completo y estructurado, con portada, secciones y conclusiones.

    El archivo final se guarda en data/outputs/reports/.

10. Registro y Evaluación

    Todos los procesos (tiempos, decisiones del agente, métricas) se guardan en data/outputs/logs/.

    El módulo logger.py crea un registro de auditoría que permite evaluar:

    Rendimiento del agente.

    Tiempo total del análisis.

    Precisión del modelo.

    Nivel de intervención humana (debe tender a cero).

11. Finalización del Proceso

    El agente notifica a la interfaz que el reporte ha sido generado exitosamente.

    El usuario puede abrir el archivo PDF desde la UI o directamente desde la carpeta de salida.

    El sistema queda en espera para procesar un nuevo archivo, sin necesidad de reiniciarse.

Resumen del Flujo Automático
Etapa	                                         Descripción	                        Módulos Clave
1. Inicio	                                    Carga entorno y modelo	                main.py, model_manager.py
2. Input	                                    Usuario selecciona archivo	            ui/window_main.py, file_manager.py
3. Planificación	                            Agente define tareas	                autonomous_agent.py, chain_manager.py
4. Limpieza	                                    Datos limpios y validados	            data_cleaner.py, anomaly_detection.py
5. Análisis	                                    Cálculo de métricas y patrones	        statistical_summary.py, metrics.py
6. Visualización	                            Generación de gráficos	                report_builder.py
7. Redacción	                                Reporte en lenguaje natural	            Gemma 2B IT, report_manager.py
8. Fine-Tuning	                                Reentrenamiento del modelo	            fine_tuning/train_model.py
9. Exportación	                                Genera PDF final	                    export_pdf.py
10. Logs	                                    Auditoría del proceso	                logger.py