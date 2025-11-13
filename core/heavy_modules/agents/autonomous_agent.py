from utils.logger import log_info, log_error
from core.heavy_modules.agents.chain_manager import ChainManager
from core.heavy_modules.agents.memory_manager import MemoryManager
from transformers import pipeline
import pandas as pd
import numpy as np

class AutonomousAgent:
    """
    Agente autónomo responsable de planificar, analizar y sintetizar información.
    """

    def __init__(self, session_id: str = "default_session"):
        try:
            self.session_id = session_id
            self.memory = MemoryManager()
            self.chain_manager = ChainManager()
            self.model = pipeline("text-generation", model="data/models/gemma_2b_it_finetuned")
            self.last_analysis = None
            log_info(f"AutonomousAgent iniciado para sesión {session_id}.")
        except Exception as e:
            log_error(f"Error al inicializar AutonomousAgent: {e}")
            raise

    def plan_actions(self, goal: str):
        """
        Define una secuencia de acciones para alcanzar el objetivo indicado.
        """
        try:
            plan = [
                f"1. Analizar datos relacionados con: {goal}",
                "2. Identificar patrones relevantes.",
                "3. Generar un resumen técnico del análisis.",
                "4. Evaluar la coherencia de los hallazgos.",
                "5. Guardar resultados y optimizar parámetros."
            ]
            log_info(f"Plan generado para objetivo '{goal}'.")
            return plan
        except Exception as e:
            log_error(f"Error al planificar acciones: {e}")
            raise

    def analyze_data(self, df: pd.DataFrame):
        """
        Analiza un DataFrame y genera hallazgos clave.
        """
        try:
            description = df.describe(include="all").to_string()
            response = self.chain_manager.execute_chain(description)
            self.last_analysis = response
            self.memory.store_context(self.session_id, {"analysis": response})
            log_info("Análisis de datos completado correctamente.")
            return response
        except Exception as e:
            log_error(f"Error durante el análisis de datos: {e}")
            raise

    def decide_next_step(self):
        """
        Decide el siguiente paso basándose en el contexto y resultados previos.
        """
        try:
            context = self.memory.recall_context(self.session_id)
            if not context or "analysis" not in context:
                next_step = "Realizar nuevo análisis de datos."
            else:
                next_step = "Generar reporte o pasar a fase de optimización."
            log_info(f"Siguiente paso decidido: {next_step}")
            return next_step
        except Exception as e:
            log_error(f"Error al decidir siguiente paso: {e}")
            raise

    def generate_summary(self, analysis: dict):
        """
        Genera un resumen textual basado en los resultados del análisis.
        """
        try:
            text_input = str(analysis)
            summary = self.model(text_input, max_length=250, num_return_sequences=1)[0]["generated_text"]
            log_info("Resumen generado exitosamente.")
            return summary
        except Exception as e:
            log_error(f"Error al generar resumen: {e}")
            raise

    def self_optimize(self):
        """
        Ajusta internamente los parámetros según los resultados previos.
        """
        try:
            context = self.memory.recall_context(self.session_id)
            if not context:
                log_info("No hay contexto previo para optimización.")
                return "Sin contexto previo."

            adjustments = {
                "learning_rate": np.random.choice([3e-5, 5e-5, 7e-5]),
                "batch_size": np.random.choice([2, 4, 8])
            }

            self.memory.store_context(self.session_id, {"optim_params": adjustments})
            log_info(f"Parámetros ajustados: {adjustments}")
            return adjustments
        except Exception as e:
            log_error(f"Error al optimizar agente: {e}")
            raise
