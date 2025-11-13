# core/utils/prompt_builder.py
"""
Módulo: prompt_builder.py
Descripción:
    Construye automáticamente el prompt para Gemma 2B IT usando un dataset
    (CSV o Excel) y metadata opcional.
    Incluye inferencia automática de roles de columna.
"""

import pandas as pd
from typing import Dict, Optional
from core.utils.column_inspector import infer_column_roles

class BuilderPrompt:

    def build_report_prompt(df: pd.DataFrame, metadata: Optional[Dict] = None) -> str:
        """
        Genera un prompt completo para el modelo Gemma 2B IT.

        :param df: DataFrame con los datos procesados.
        :param metadata: Diccionario con información adicional (autor, fecha, notas, etc.)
        :return: String con el prompt listo para enviar al modelo.
        """
        metadata = metadata or {}
        column_roles = infer_column_roles(df)

        # Construcción de la sección de columnas
        columns_info = []
        for col, role in column_roles.items():
            columns_info.append(f"- {col}: {role}")
        columns_text = "\n".join(columns_info)

        # Metadata opcional
        metadata_text = ""
        if metadata:
            metadata_lines = [f"{k}: {v}" for k, v in metadata.items()]
            metadata_text = "\n".join(metadata_lines)

        # Prompt final
        prompt = (
            "Eres Gemma 2B IT, un agente experto en análisis de datos y generación de reportes.\n\n"
            "A continuación se proporciona información sobre los datos que debes analizar:\n\n"
            f"### Metadata:\n{metadata_text if metadata_text else 'No hay metadata adicional'}\n\n"
            f"### Columnas y roles:\n{columns_text}\n\n"
            "Tu tarea es analizar estos datos y generar un reporte completo en PDF, "
            "incluyendo conclusiones interpretativas, métricas relevantes y visualizaciones sugeridas. "
            "Describe patrones, anomalías y resalta información clave para la toma de decisiones.\n\n"
            "Redacta la información de manera clara y profesional."
        )

        return prompt
