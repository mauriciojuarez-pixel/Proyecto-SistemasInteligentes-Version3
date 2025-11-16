# core/utils/prompt_builder.py

import hashlib
import pandas as pd
from typing import Dict, Optional
from core.utils.column_inspector import infer_column_roles

# Módulos de analytics
from core.heavy_modules.analytics.statistical_summary import compute_descriptive_stats
from core.heavy_modules.analytics.anomaly_detection import detect_outliers
from core.heavy_modules.analytics.correlation_analysis import compute_correlations

from transformers import pipeline
import json


class BuilderPrompt:

    def __init__(self):
        self.model_path = (
            "data/models/gemma_2b_it_base/"
            "models--google--gemma-2b-it/"
            "snapshots/96988410cbdaeb8d5093d1ebdc5a8fb563e02bad/"
        )
        self.generator = pipeline(
            "text-generation",
            model=self.model_path,
            device="cpu"
        )

    @staticmethod
    def _generate_hash(text: str) -> str:
        h = hashlib.sha1()
        h.update(text.encode("utf-8"))
        return h.hexdigest()

    @staticmethod
    def _format_metadata(metadata: Dict) -> str:
        if not metadata:
            return "No hay metadata adicional"
        return "\n".join([f"{k}: {v}" for k, v in metadata.items()])

    @staticmethod
    def _format_column_roles(df: pd.DataFrame) -> str:
        roles = infer_column_roles(df)
        lines = [f"- {col}: {role}" for col, role in roles.items()]
        return "\n".join(lines)

    @staticmethod
    def _format_statistics(df: pd.DataFrame) -> str:
        numeric_cols = df.select_dtypes(include='number').columns
        if len(numeric_cols) == 0:
            return "No hay columnas numéricas para calcular estadísticas."

        stats_df = compute_descriptive_stats(df[numeric_cols])

        stats_text = []
        for col in stats_df.index:  # <-- usar index en vez de columns
            mean = stats_df.loc[col].get('mean', 'N/A')
            median = stats_df.loc[col].get('50%', 'N/A')  # mediana en describe() es '50%'
            mode = df[col].mode().iloc[0] if not df[col].mode().empty else 'N/A'
            std = stats_df.loc[col].get('std', 'N/A')
            outliers_count = len(detect_outliers(df[[col]]))

            stats_text.append(
                f"**{col}:** Media={mean}, Mediana={median}, Moda={mode}, "
                f"Desviación estándar={std}, Outliers={outliers_count}"
            )

        return "\n".join(stats_text)


    @staticmethod
    def _format_correlations(df: pd.DataFrame) -> str:
        numeric_df = df.select_dtypes(include='number')
        if numeric_df.empty:
            return "No hay columnas numéricas para calcular correlaciones."

        corr_matrix = compute_correlations(numeric_df)
        top_corrs = []
        for col in corr_matrix.columns:
            high_corr = corr_matrix[col][(corr_matrix[col].abs() > 0.8) & (corr_matrix[col].abs() < 1.0)]
            for related_col, value in high_corr.items():
                top_corrs.append(f"{col} ↔ {related_col}: {value:.2f}")
        return "\n".join(top_corrs) if top_corrs else "No hay correlaciones altas."


    def build_report_prompt(self, df: pd.DataFrame, metadata: Optional[Dict] = None) -> str:
        """
        Construye un prompt para generar SOLO un resumen final.
        Evita cualquier instrucción que pueda causar un re-análisis.
        """

        metadata_text = self._format_metadata(metadata or {})
        columns_text = self._format_column_roles(df)
        stats_text = self._format_statistics(df)
        correlations_text = self._format_correlations(df)

        prompt = (
            "Eres Gemma 2B IT, experta en análisis de datos.\n\n"
            "Tu objetivo es generar un **resumen ejecutivo final**, basado en:\n"
            "- El análisis previo (incluido como metadata).\n"
            "- Estadísticas y estructura del dataset.\n\n"
            "IMPORTANTE:\n"
            "- NO repitas el análisis previo.\n"
            "- NO reconstruyas estadísticas.\n"
            "- NO vuelvas a describir distribución, patrones o anomalías.\n"
            "- SOLO sintetiza y extrae conclusiones finales.\n\n"

            f"### Análisis previo (metadata):\n{metadata_text}\n\n"

            "### Información técnica del dataset (para contexto, NO analizar):\n"
            f"- Columnas y roles:\n{columns_text}\n\n"
            f"- Estadísticas clave:\n{stats_text}\n\n"
            f"- Correlaciones relevantes:\n{correlations_text}\n\n"

            "Genera un **resumen ejecutivo conciso** que incluya únicamente:\n"
            "- Hallazgos finales.\n"
            "- Conclusiones de negocio.\n"
            "- Recomendaciones.\n"
            "- Riesgos o anomalías importantes.\n"
            "- Visualizaciones útiles.\n\n"
        )

        integrity_hash = self._generate_hash(prompt)
        prompt += f"#HASH:{integrity_hash}"

        return prompt



    @staticmethod
    def build_prompt_chain(df: pd.DataFrame, metadata: Optional[Dict] = None, instruction: str = "") -> str:
        metadata = metadata or {}
        column_roles = infer_column_roles(df)
        columns_info = [f"- {col}: {role}" for col, role in column_roles.items()]
        columns_text = "\n".join(columns_info)
        metadata_text = "\n".join([f"{k}: {v}" for k, v in metadata.items()]) if metadata else "No hay metadata adicional"

        stats_text = BuilderPrompt._format_statistics(df)
        correlations_text = BuilderPrompt._format_correlations(df)

        prompt = (
            f"{instruction}\n\n"
            f"### Metadata:\n{metadata_text}\n\n"
            f"### Columnas y roles:\n{columns_text}\n\n"
            f"### Estadísticas y outliers:\n{stats_text}\n\n"
            f"### Correlaciones relevantes:\n{correlations_text}\n\n"
            "Describe distribución, patrones, posibles anomalías, recomendaciones y visualizaciones sugeridas.\n"
            "Finalmente, presenta un resumen consolidado con conclusiones y recomendaciones de negocio."
        )

        return prompt

    def build_column_prompt(self, df: pd.DataFrame, sample_size: int = 5) -> str:
        """
        Genera un prompt para que Gemma infiera el rol de cada columna basado
        en su tipo de dato y valores de ejemplo.

        :param df: DataFrame a analizar
        :param sample_size: Número de valores de ejemplo por columna
        :return: String con el prompt listo
        """
        column_info_list = []

        for col in df.columns:
            dtype = str(df[col].dtype)
            sample_values = df[col].dropna().head(sample_size).tolist()
            # Convertir a string y escapar caracteres especiales
            sample_values = [str(v) for v in sample_values]
            column_info_list.append({
                "column_name": col,
                "dtype": dtype,
                "sample_values": sample_values
            })

        # Convertir la lista a JSON legible
        column_info_json = json.dumps(column_info_list, indent=2, ensure_ascii=False)

        # Construir el prompt
        prompt = (
            "Eres Gemma 2B IT, experta en análisis de datos.\n"
            "Tienes un conjunto de columnas de un dataset, cada una con tipo de dato y ejemplos de valores.\n"
            "Tu tarea es inferir el rol principal de cada columna (por ejemplo: numérico, categórico, fecha, identificador, etc.) "
            "y proporcionar una breve descripción de su propósito.\n"
            "Usa los valores de ejemplo para guiar tu inferencia.\n\n"
            f"Columnas y ejemplos:\n{column_info_json}\n\n"
            "Responde únicamente en formato JSON como:\n"
            "{\n"
            "  \"column_name_1\": \"inferred_role\",\n"
            "  \"column_name_2\": \"inferred_role\",\n"
            "  ...\n"
            "}"
        )

        return prompt



    def execute_model(self, prompt: str, max_length: int = 600) -> str:
        output = self.generator(
            prompt,
            max_length=max_length,
            num_return_sequences=1
        )
        return output[0]["generated_text"]
