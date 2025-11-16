# core/heavy_modules/agents/chain_manager.py

from langchain_community.llms.huggingface_pipeline import HuggingFacePipeline
from transformers import pipeline
import os

from core.utils.logger import init_logger, log_info, log_error
from core.utils.prompt_builder import BuilderPrompt

logger = init_logger("ChainManager")

class ChainManager:
    """
    Ejecuta análisis y resúmenes usando prompts generados dinámicamente.
    """

    def __init__(self, model_base_path="data/models/gemma_2b_it_base"):
        try:
            snapshot_dir = os.path.join(
                model_base_path,
                "models--google--gemma-2b-it",
                "snapshots",
                "96988410cbdaeb8d5093d1ebdc5a8fb563e02bad"
            )

            if not os.path.exists(snapshot_dir):
                raise FileNotFoundError(f"Ruta del modelo no encontrada: {snapshot_dir}")

            hf_pipe = pipeline(
                task="text-generation",
                model=snapshot_dir,
                tokenizer=snapshot_dir,
                max_new_tokens=512,
                temperature=0.7
            )

            self.llm = HuggingFacePipeline(pipeline=hf_pipe)
            self.memory_context = {}
            self.trace = []

            log_info(logger, f"ChainManager inicializado con modelo local en {snapshot_dir}")

        except Exception as e:
            log_error(logger, f"Error inicializando ChainManager: {e}")
            raise

    def build_prompt(self, df=None, metadata=None, instruction=""):
        """
        Genera un prompt completo usando BuilderPrompt.
        """
        try:
            prompt_builder = BuilderPrompt()
            prompt_text = prompt_builder.build_prompt_chain(
                df=df,
                metadata=metadata,
                instruction=instruction or "Analiza y resume los datos para generar hallazgos técnicos."
            )
            self.trace.append("Prompt construido correctamente.")
            log_info(logger, "Prompt generado con BuilderPrompt.")
            return prompt_text
        except Exception as e:
            log_error(logger, f"Error al construir el prompt: {e}")
            raise

    def execute_prompt(self, prompt: str, max_length: int = 600):
        """
        Ejecuta el modelo local con el prompt generado, usando texto plano.
        """
        try:
            # Ejecutar pipeline de HuggingFace directamente con string
            # siempre pasamos una lista de strings
            result = self.llm.generate([prompt])
            text = result.generations[0][0].text


            self.trace.append("Prompt ejecutado correctamente.")
            log_info(logger, "Modelo ejecutado sobre el prompt.")
            return text
        except Exception as e:
            log_error(logger, f"Error al ejecutar el prompt: {e}")
            raise



    def execute_chain(self, df=None, metadata=None, instruction=""):
        """
        Genera prompt y lo ejecuta, retornando el resultado.
        """
        try:
            prompt_text = self.build_prompt(df=df, metadata=metadata, instruction=instruction)
            result = self.execute_prompt(prompt_text)
            self.trace.append("Cadena ejecutada correctamente.")
            log_info(logger, "Cadena ejecutada.")
            return result
        except Exception as e:
            log_error(logger, f"Error al ejecutar la cadena: {e}")
            raise


    def inject_context(self, memory: dict):
        """
        Inyecta contexto adicional que pueda usar el agente.
        """
        try:
            self.memory_context.update(memory)
            self.trace.append("Contexto inyectado.")
            log_info(logger, "Contexto inyectado en ChainManager.")
        except Exception as e:
            log_error(logger, f"Error al inyectar contexto: {e}")
            raise

    def trace_chain(self):
        """
        Retorna el historial de acciones y trazas.
        """
        return self.trace
