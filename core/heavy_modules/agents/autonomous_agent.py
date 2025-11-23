# core/heavy_modules/agents/autonomous_agent.py

from core.utils.logger import init_logger, log_info, log_warning, log_error
from core.heavy_modules.agents.chain_manager import ChainManager
from core.heavy_modules.agents.memory_manager import MemoryManager
from core.utils.prompt_builder import BuilderPrompt
import pandas as pd

logger = init_logger("AutonomousAgent")


class AutonomousAgent:
    def __init__(self, session_id: str = "default_session"):
        try:
            self.session_id = session_id
            self.memory = MemoryManager()

            # ChainManager ya contiene el modelo GGUF cargado con llama_cpp
            self.chain_manager = ChainManager()

            # Variables internas
            self.last_analysis = None
            self.last_analysis_df = None

            log_info(logger, f"AutonomousAgent iniciado para sesión {session_id}.")

        except Exception as e:
            log_error(logger, f"Error al inicializar AutonomousAgent: {e}")
            raise

    def analyze_data(self, df: pd.DataFrame):
        """
        Analiza un DataFrame completo y genera hallazgos usando ChainManager.
        Maneja DataFrames vacíos y asegura siempre una respuesta no vacía.
        """
        try:
            if df is None or df.empty:
                log_warning(logger, "DataFrame vacío. Se generará un análisis por defecto.")
                self.last_analysis_df = pd.DataFrame()
                response = "No se pudieron generar hallazgos debido a datos vacíos."
                self.last_analysis = response
                self.memory.store_context(self.session_id, {"analysis": response})
                return response

            # Guardamos el DataFrame
            self.last_analysis_df = df.copy()

            # Llamamos al análisis completo
            response = self.chain_manager.execute_chain(df=df)
            response = response or "No se generaron hallazgos del análisis."

            # Guardamos en memoria
            self.last_analysis = response
            self.memory.store_context(self.session_id, {"analysis": response})

            log_info(logger, "Análisis de datos completado correctamente.")
            return response

        except Exception as e:
            log_error(logger, f"Error durante el análisis de datos: {e}")
            # Retornar mensaje por defecto si falla el análisis
            response = "Error durante el análisis de datos; no se generaron hallazgos."
            self.last_analysis = response
            return response

    def generate_summary(self, analysis_results: dict, instruction: str = "") -> str:
        """
        Genera un resumen final del análisis usando el contenido del prompt.
        Si el modelo falla, retorna un fallback seguro.
        """
        try:
            if self.last_analysis_df is None:
                raise ValueError("No hay análisis previo. Ejecuta analyze_data() primero.")

            # Genera prompt completo con todos los datos, estadísticas y roles
            prompt_builder = BuilderPrompt()
            prompt_text = prompt_builder.build_prompt_chain(
                df=self.last_analysis_df,
                metadata=analysis_results,
                instruction=instruction
            )

            # Aquí guardas el prompt si quieres depuración
            self.last_prompt = prompt_text
            with open("ultimo_prompt.txt", "w", encoding="utf-8") as f:
                f.write(prompt_text)

            # Ejecuta el modelo usando el prompt generado
            try:
                response = self.chain_manager.execute_prompt(prompt_text)
            except Exception as e:
                log_error(logger, f"Error ejecutando modelo: {e}")
                response = ""

            # Fallback si no hay contenido útil
            if not response or response.strip() == "" or "no generó contenido" in response.lower():
                log_info(logger, "El modelo no generó contenido, usando fallback basado en análisis existente.")

                # Construir fallback con RECOMENDACIONES y SUMMARY si existen, si no, usar todo analysis_results
                if 'RECOMENDACIONES' in analysis_results or 'SUMMARY' in analysis_results:
                    fallback_summary = (
                        "=== Fallback: Resumen basado en análisis disponible ===\n\n"
                        f"RECOMENDACIONES: {analysis_results.get('RECOMENDACIONES', '')}\n\n"
                        f"SUMMARY: {analysis_results.get('SUMMARY', '')}\n"
                    )
                else:
                    # Imprime todo lo que se generó
                    fallback_summary = "=== Fallback: Contenido disponible en analysis_results ===\n\n"
                    for key, value in analysis_results.items():
                        fallback_summary += f"{key}: {value}\n\n"

                response = fallback_summary

            log_info(logger, "Resumen generado correctamente.")
            return response

        except Exception as e:
            log_error(logger, f"Error al generar resumen: {e}")
            return "Error al generar el resumen; se recomienda revisar los datos y la configuración del modelo."
