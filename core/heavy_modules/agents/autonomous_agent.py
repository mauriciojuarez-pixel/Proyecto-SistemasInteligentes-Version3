# core/heavy_modules/agents/autonomous_agent.py

from core.utils.logger import init_logger, log_info, log_error
from core.heavy_modules.agents.chain_manager import ChainManager
from core.heavy_modules.agents.memory_manager import MemoryManager
from core.utils.prompt_builder import BuilderPrompt
from transformers import pipeline
import pandas as pd
import numpy as np

logger = init_logger("AutonomousAgent")


class AutonomousAgent:
    def __init__(self, session_id: str = "default_session"):
        try:
            self.session_id = session_id
            self.memory = MemoryManager()
            self.chain_manager = ChainManager()

            # Modelo de generación de texto (Gemma local)
            self.model = pipeline(
                "text-generation",
                model="data/models/gemma_2b_it_base/models--google--gemma-2b-it/snapshots/96988410cbdaeb8d5093d1ebdc5a8fb563e02bad"
            )

            # Variables internas para mantener estado
            self.last_analysis = None
            self.last_analysis_df = None

            log_info(logger, f"AutonomousAgent iniciado para sesión {session_id}.")
        except Exception as e:
            log_error(logger, f"Error al inicializar AutonomousAgent: {e}")
            raise

    def analyze_data(self, df: pd.DataFrame):
        """
        Analiza un DataFrame completo y genera hallazgos.
        """
        try:
            # Guardar copia del DataFrame usado durante el análisis
            self.last_analysis_df = df.copy()

            # Ejecutar cadena de análisis con todo el DataFrame
            response = self.chain_manager.execute_chain(df=df)

            # Guardar análisis en memoria temporal del agente
            self.last_analysis = response
            self.memory.store_context(self.session_id, {"analysis": response})

            log_info(logger, "Análisis de datos completado correctamente con todos los datos del DataFrame.")
            return response

        except Exception as e:
            log_error(logger, f"Error durante el análisis de datos: {e}")
            raise

    def generate_summary(self, analysis_results: dict):
        """
        Genera un reporte final basado en:
        - El DataFrame original usado en el análisis
        - Los resultados generados por la cadena LLM
        """
        try:
            prompt_builder = BuilderPrompt()

            # Construcción correcta del prompt
            prompt = prompt_builder.build_report_prompt(
                df=self.last_analysis_df,     # DataFrame original
                metadata=analysis_results     # Resultados del análisis
            )

            # Ejecutar prompt directamente en la chain
            response = self.chain_manager.execute_prompt(prompt)

            log_info(logger, "Resumen generado correctamente.")
            return response

        except Exception as e:
            log_error(logger, f"Error al generar resumen: {e}")
            raise
