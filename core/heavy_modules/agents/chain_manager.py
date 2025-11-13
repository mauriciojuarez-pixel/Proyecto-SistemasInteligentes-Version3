# chain_manager.py

from langchain_community.llms import huggingface_pipeline
from langchain_core.prompts import PromptTemplate
from langchain_classic.chains.llm import LLMChain
from langchain_classic.chains.sequential import SimpleSequentialChain
from utils.logger import log_info, log_error
from transformers import pipeline


class ChainManager:
    """
    Define y ejecuta cadenas de razonamiento con LangChain.
    """

    def __init__(self, model_path="data/models/gemma_2b_it_finetuned"):
        try:
            # Crear el pipeline de Hugging Face manualmente
            hf_pipeline = pipeline(
                task="text-generation",
                model=model_path,
                max_new_tokens=256,
                temperature=0.7
            )

            # Inicializar LLM compatible con LangChain
            self.llm = huggingface_pipeline(pipeline=hf_pipeline)

            self.memory_context = {}
            self.trace = []
            log_info("ChainManager inicializado correctamente con HuggingFacePipeline.")
        except Exception as e:
            log_error(f"Error inicializando ChainManager: {e}")
            raise

    def build_chain(self):
        """
        Define la secuencia de pasos (input → análisis → resumen → reporte).
        """
        try:
            # Prompt 1: análisis del contenido
            input_prompt = PromptTemplate(
                input_variables=["user_input"],
                template="Analiza el siguiente contenido y describe sus patrones clave:\n{user_input}"
            )

            # Prompt 2: resumen técnico
            analysis_prompt = PromptTemplate(
                input_variables=["analysis"],
                template=(
                    "Con base en este análisis:\n{analysis}\n"
                    "Resume los hallazgos principales en lenguaje técnico y conciso."
                ),
            )

            # Cadena 1: análisis
            input_chain = LLMChain(
                llm=self.llm,
                prompt=input_prompt,
                output_key="analysis",
            )

            # Cadena 2: resumen técnico
            summary_chain = LLMChain(
                llm=self.llm,
                prompt=analysis_prompt,
                output_key="summary",
            )

            # Cadena secuencial: input → análisis → resumen
            chain = SimpleSequentialChain(
                chains=[input_chain, summary_chain],
                verbose=True,
            )

            self.trace.append("Cadena construida exitosamente.")
            log_info("Cadena LangChain creada correctamente.")
            return chain

        except Exception as e:
            log_error(f"Error al construir la cadena: {e}")
            raise

    def execute_chain(self, data: str):
        """
        Ejecuta la cadena sobre los datos cargados.
        """
        try:
            chain = self.build_chain()
            result = chain.run(data)
            self.trace.append("Cadena ejecutada correctamente.")
            log_info("Cadena ejecutada con éxito.")
            return result
        except Exception as e:
            log_error(f"Error al ejecutar la cadena: {e}")
            raise

    def inject_context(self, memory: dict):
        """
        Inyecta contexto previo del agente (memoria).
        """
        try:
            self.memory_context.update(memory)
            self.trace.append("Contexto inyectado.")
            log_info("Contexto inyectado exitosamente.")
        except Exception as e:
            log_error(f"Error al inyectar contexto: {e}")
            raise

    def trace_chain(self):
        """
        Devuelve un registro paso a paso de la ejecución.
        """
        return self.trace
