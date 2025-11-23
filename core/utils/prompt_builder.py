# core/utils/prompt_builder.py

import hashlib
import pandas as pd
from typing import Dict, Optional
from core.utils.column_inspector import infer_column_roles

# Módulos de analytics
from core.heavy_modules.analytics.statistical_summary import compute_descriptive_stats
from core.heavy_modules.analytics.anomaly_detection import detect_outliers
from core.heavy_modules.analytics.correlation_analysis import compute_correlations
from typing import Optional, Dict
from llama_cpp import Llama
import json


class BuilderPrompt:

    def __init__(self):
        """
        Constructor: carga el modelo GGUF con llama.cpp.
        """
        self.model_path = (
            "data/models/gemma_2b_it_base/"
            "models--google--gemma-2b-it/"
            "snapshots/96988410cbdaeb8d5093d1ebdc5a8fb563e02bad/"
            "gemma-2b-it.gguf"
        )

        # Cargar modelo GGUF con llama.cpp
        self.model = Llama(
            model_path=self.model_path,
            n_ctx=8192,         # contexto largo
            n_gpu_layers=-1,    # usar GPU si existe
            n_threads=8,        # optimización CPU
            temperature=0.0,    # para RESÚMENES → salida estable
            verbose=False
        )

    # =========================================================
    #       MÉTODO PRINCIPAL DE INFERENCIA (produce texto)
    # =========================================================
    def generate(self, prompt: str, max_tokens=1024) -> str:
        response = self.model(
            prompt,
            max_tokens=max_tokens,
            stop=["</s>", "###"],
        )
        return response["choices"][0]["text"].strip()

    # =========================================================
    #                  FORMATTERS
    # =========================================================

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
        for col in stats_df.index:
            mean = stats_df.loc[col].get('mean', 'N/A')
            median = stats_df.loc[col].get('50%', 'N/A')
            mode = df[col].mode().iloc[0] if not df[col].mode().empty else 'N/A'
            std = stats_df.loc[col].get('std', 'N/A')
            outliers_count = len(detect_outliers(df[[col]]))

            stats_text.append(
                f"**{col}:** Media={mean}, Mediana={median}, "
                f"Moda={mode}, Desviación estándar={std}, Outliers={outliers_count}"
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
            high_corr = corr_matrix[col][
                (corr_matrix[col].abs() > 0.8) & (corr_matrix[col].abs() < 1.0)
            ]
            for related_col, value in high_corr.items():
                top_corrs.append(f"{col} ↔ {related_col}: {value:.2f}")

        return "\n".join(top_corrs) if top_corrs else "No hay correlaciones altas."

    # =========================================================
    #                   PROMPT PRINCIPAL
    # =========================================================

    def build_report_prompt(self, df: pd.DataFrame, metadata: Optional[Dict] = None) -> str:
        metadata_text = self._format_metadata(metadata or {})
        columns_text = self._format_column_roles(df)
        stats_text = self._format_statistics(df)
        correlations_text = self._format_correlations(df)

        prompt = (
            "Genera un resumen ejecutivo claro y conciso.\n\n"
            "INSTRUCCIONES:\n"
            "- No muestres datos internos.\n"
            "- No repitas estadísticas, columnas ni metadatos.\n"
            "- No vuelvas a analizar los datos.\n"
            "- Solo escribe el resumen final.\n\n"

            "[INFORMACIÓN INTERNA — NO MOSTRAR]\n"
            f"{metadata_text}\n"
            f"{columns_text}\n"
            f"{stats_text}\n"
            f"{correlations_text}\n"
        )

        return prompt


    # =========================================================
    #               PROMPT PARA CADENA COMPLETA
    # =========================================================


    @staticmethod
    def build_prompt_chain(df: pd.DataFrame, metadata: Optional[Dict] = None, instruction: str = "") -> str:
        """
        Construye un prompt compacto para el modelo, incluyendo:
        - Metadata resumida
        - Roles de columnas
        - Estadísticas clave (redondeadas)
        - Correlaciones relevantes
        - Instrucciones claras para generar un resumen ejecutivo
        """

        metadata = metadata or {}
        column_roles = infer_column_roles(df)

        # Formateo de metadata resumida
        metadata_text = "\n".join([f"{k}: {v}" for k, v in metadata.items()]) if metadata else "Sin metadata relevante"

        # Formateo de roles
        columns_text = "\n".join([f"- {col}: {role}" for col, role in column_roles.items()])

        # Estadísticas resumidas
        numeric_cols = df.select_dtypes(include='number').columns
        stats_text = []
        for col in numeric_cols:
            mean = round(df[col].mean(), 2)
            median = round(df[col].median(), 2)
            mode = round(df[col].mode().iloc[0], 2) if not df[col].mode().empty else 'N/A'
            std = round(df[col].std(), 2)
            outliers_count = len(detect_outliers(df[[col]]))
            stats_text.append(f"**{col}:** Media={mean}, Mediana={median}, Moda={mode}, Std={std}, Outliers={outliers_count}")
        stats_text = "\n".join(stats_text) if stats_text else "No hay columnas numéricas."

        # Correlaciones altas solo
        corr_text = []
        if not df[numeric_cols].empty:
            corr_matrix = compute_correlations(df[numeric_cols])
            for col in corr_matrix.columns:
                high_corr = corr_matrix[col][(corr_matrix[col].abs() > 0.8) & (corr_matrix[col].abs() < 1.0)]
                for related_col, val in high_corr.items():
                    corr_text.append(f"{col} ↔ {related_col}: {round(val, 2)}")
        corr_text = "\n".join(corr_text) if corr_text else "No hay correlaciones altas."

        # Instrucciones compactas
        instruction_text = instruction or (
            "Genera un resumen ejecutivo profesional basado únicamente en los datos proporcionados."
        )

        # Construcción del prompt final
        prompt = (
            f"{instruction_text}\n\n"
            "TUS TAREAS Y OBJETIVOS:\n"
            "- Genera **RECOMENDACIONES ACCIONABLES**: sugiere acciones concretas basadas en los hallazgos del análisis de datos, siendo específico y práctico.\n"
            "- Genera **SUGERIR VISUALIZACIONES**: propone gráficos, histogramas, boxplots u otras visualizaciones útiles para interpretar los datos y sus patrones.\n"
            "- Genera **SUMMARY**: un resumen ejecutivo consolidado de los hallazgos clave, incluyendo patrones de las columnas, distribuciones, anomalías, outliers y cualquier insight relevante.\n"
            "- Genera **RESUMEN EJECUTIVO**: sintetiza de forma clara y concisa lo generado en RECOMENDACIONES, VISUALIZACIONES y SUMMARY, destacando los hallazgos más importantes, conclusiones clave y la situación general de los datos.\n"

            "REGLAS:\n"
            "- Mantén Markdown profesional.\n"
            "- No inventes columnas ni datos.\n"
            "- Usa solo la información proporcionada.\n\n"
            "[INFORMACIÓN INTERNA — NO INCLUIR EN EL RESUMEN]\n"
            f"METADATA:\n{metadata_text}\n\n"
            f"ROLES DE COLUMNAS:\n{columns_text}\n\n"
            f"ESTADÍSTICAS:\n{stats_text}\n\n"
            f"CORRELACIONES:\n{corr_text}"
        )


        return prompt



    # =========================================================
    #              PROMPT PARA INFERIR ROLES DE COLUMNA
    # =========================================================
    def build_column_prompt(self, df: pd.DataFrame, sample_size: int = 5) -> str:
        """
        Prompt para que el modelo infiera roles columna por columna.
        La respuesta será SOLO un JSON válido.
        """

        column_info_list = []

        for col in df.columns:
            dtype = str(df[col].dtype)
            sample_values = df[col].dropna().head(sample_size).tolist()
            sample_values = [str(v) for v in sample_values]
            column_info_list.append({
                "column_name": col,
                "dtype": dtype,
                "sample_values": sample_values
            })

        column_info_json = json.dumps(column_info_list, indent=2, ensure_ascii=False)

        prompt = (
            "Eres Gemma 2B IT, especialista en estructuras de datos.\n"
            "Tu tarea es INFERIR el rol de cada columna basado en tipo de dato y ejemplos.\n\n"

            "INSTRUCCIONES:\n"
            "NO muestres el prompt ni los textos internos.\n"
            "Usa la información solo para razonar.\n"
            "DEBES responder únicamente con un JSON válido.\n"
            "Sin texto adicional, sin explicaciones.\n\n"

            f"[COLUMN_DATA]\n{column_info_json}\n\n"

            "RESPUESTA OBLIGATORIA (solo JSON):\n"
            "{\n"
            '  "column_name_1": "rol",\n'
            '  "column_name_2": "rol"\n'
            "}"
        )

        return prompt
