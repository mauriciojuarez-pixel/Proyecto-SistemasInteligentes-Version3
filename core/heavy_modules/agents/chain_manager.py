# core/heavy_modules/agents/chain_manager.py

import os
from llama_cpp import Llama

from core.utils.logger import init_logger, log_info, log_error
from core.utils.prompt_builder import BuilderPrompt

logger = init_logger("ChainManager")


class ChainManager:
    """
    Maneja generación de prompts y ejecución del modelo GGUF con llama.cpp
    """

    def __init__(self):
        try:
            # --------------------------
            # RUTA CORRECTA DEL MODELO
            # --------------------------
            self.model_path = (
                "data/models/gemma_2b_it_base/"
                "models--google--gemma-2b-it/"
                "snapshots/96988410cbdaeb8d5093d1ebdc5a8fb563e02bad/"
                "gemma-2b-it.gguf"
            )

            if not os.path.exists(self.model_path):
                raise FileNotFoundError(
                    f"Modelo GGUF no encontrado en:\n{self.model_path}"
                )

            # --------------------------
            # CARGA DEL MODELO LLAMA.CPP
            # --------------------------
            self.llm = Llama(
                model_path=self.model_path,
                n_ctx=4096,
                n_threads=6,
                n_gpu_layers=20,
                verbose=False
            )

            self.memory_context = {}
            self.trace = []

            log_info(
                logger,
                f"ChainManager inicializado correctamente.\nModelo cargado: {self.model_path}"
            )

        except Exception as e:
            log_error(logger, f"Error inicializando ChainManager: {e}")
            raise

    # ---------------------------------------------------------------------

    def build_prompt(self, df=None, metadata=None, instruction=""):
        """Construye un prompt profesional usando BuilderPrompt."""
        try:
            builder = BuilderPrompt()
            prompt_text = builder.build_prompt_chain(
                df=df,
                metadata=metadata,
                instruction=instruction or "Analiza y resume los datos."
            )

            self.trace.append("Prompt construido correctamente.")
            log_info(logger, "Prompt generado con BuilderPrompt.")
            return prompt_text

        except Exception as e:
            log_error(logger, f"Error al construir prompt: {e}")
            raise

    # ---------------------------------------------------------------------

    def execute_prompt(self, prompt: str, max_tokens: int = 512):
        """Ejecuta el modelo GGUF usando llama_cpp."""

        try:
            response = self.llm(
                prompt=prompt,            # <-- corregido (antes era sin keyword)
                max_tokens=max_tokens,
                temperature=0.7,
                top_p=0.9,
                stop=["#HASH:"]
            )

            text = response["choices"][0]["text"].strip()

            self.trace.append("Prompt ejecutado correctamente.")
            log_info(logger, "Modelo GGUF ejecutado sobre el prompt.")

            print("\n========== PROMPT ENVIADO AL MODELO ==========\n")
            print(prompt)
            print("\n==============================================\n")

            return text

        except Exception as e:
            log_error(logger, f"Error ejecutando el modelo GGUF: {e}")
            raise

    # ---------------------------------------------------------------------

    def execute_chain(self, df=None, metadata=None, instruction=""):
        """Genera prompt y lo ejecuta."""
        try:
            prompt = self.build_prompt(df=df, metadata=metadata, instruction=instruction)
            result = self.execute_prompt(prompt)

            self.trace.append("Cadena ejecutada correctamente.")
            log_info(logger, "Cadena ejecutada exitosamente.")
            return result

        except Exception as e:
            log_error(logger, f"Error ejecutando la cadena: {e}")
            raise

    # ---------------------------------------------------------------------

    def inject_context(self, memory: dict):
        try:
            self.memory_context.update(memory)
            self.trace.append("Contexto inyectado.")
            log_info(logger, "Contexto inyectado correctamente.")
        except Exception as e:
            log_error(logger, f"Error al inyectar contexto: {e}")
            raise

    # ---------------------------------------------------------------------

    def trace_chain(self):
        return self.trace
