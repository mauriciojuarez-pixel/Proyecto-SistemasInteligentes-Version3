"""
AGENT CONTROLLER
================
Orquesta el flujo principal del sistema inteligente basado en LangChain.
Gestiona la inicialización del agente, la ejecución del pipeline,
la delegación de tareas y el control de estados del sistema.
"""

from __future__ import annotations
import threading
import traceback
from enum import Enum
from typing import Optional, Dict, Any
import pandas as pd


from core.controller.data_manager import DataManager
from core.controller.model_manager import ModelManager
from core.controller.report_manager import ReportManager
from core.heavy_modules.agents.autonomous_agent import AutonomousAgent

from core.utils.logger import init_logger, log_info, log_error
logger = init_logger("AgentController")


class AgentState(Enum):
    """Estados posibles del agente."""
    IDLE = "idle"
    RUNNING = "running"
    TRAINING = "training"
    ERROR = "error"


class AgentController:
    """Controlador principal del sistema autónomo."""

    def __init__(self):
        self.state = AgentState.IDLE
        self.agent: Optional[AutonomousAgent] = None
        self.data_manager = DataManager()
        self.model_manager = ModelManager()
        self.report_manager = ReportManager()
        self.current_thread: Optional[threading.Thread] = None

    # -------------------------------------------------------------------------
    # Inicialización
    # -------------------------------------------------------------------------
    def initialize_agent(self) -> None:
        """Configura e inicializa el agente LangChain."""
        try:
            log_info(logger,"Inicializando agente LangChain...")
            self.agent = AutonomousAgent()
            self.state = AgentState.IDLE
            log_info(logger,"Agente inicializado correctamente.")
        except Exception as e:
            log_error(logger,f"Error al inicializar el agente: {e}")
            self.state = AgentState.ERROR
            traceback.print_exc()

    # -------------------------------------------------------------------------
    # Ejecución del pipeline principal
    # -------------------------------------------------------------------------
    def run_pipeline(self, file_path: str) -> None:
        """
        Ejecuta el flujo completo:
        1. Carga y validación del dataset
        2. Limpieza y análisis
        3. Fine-tuning y evaluación
        4. Generación de reporte
        """
        def _pipeline():
            try:
                self.state = AgentState.RUNNING
                log_info(logger,f"Inicio del pipeline con archivo: {file_path}")

                # 1. Cargar y limpiar datos
                df = self.data_manager.load_data(file_path)
                df = self.data_manager.clean_data(df)
                self.data_manager.validate_structure(df)

                # 2. Análisis inteligente (LangChain)
                insights = self.agent.analyze_data(df)

                # 3. Fine-tuning (si aplica)
                self.state = AgentState.TRAINING
                self.model_manager.fine_tune("data/datasets/processed/", epochs=3)

                # 4. Generar reporte final
                self.state = AgentState.RUNNING
                report_path = self.report_manager.generate_report(df, insights)
                log_info(logger,f"Reporte generado: {report_path}")

                self.state = AgentState.IDLE
                log_info(logger,"Pipeline completado correctamente.")

            except Exception as e:
                log_error(logger,f"Error en el pipeline: {e}")
                self.state = AgentState.ERROR
                traceback.print_exc()

        # Ejecutar el pipeline en hilo separado
        self.current_thread = threading.Thread(target=_pipeline, daemon=True)

        self.current_thread.start()

    # -------------------------------------------------------------------------
    # Delegación de tareas
    # -------------------------------------------------------------------------
    def delegate_task(self, task_name: str, params: Dict[str, Any]) -> Any:
        """Delegar tareas específicas a los módulos correspondientes."""
        log_info(logger,f"Delegando tarea: {task_name}")
        try:
            if task_name == "clean_data":
                return self.data_manager.clean_data(params["data"])
            elif task_name == "fine_tune":
                return self.model_manager.fine_tune(params["data_path"])
            elif task_name == "generate_report":
                return self.report_manager.generate_report(params["data"], params["insights"])
            else:
                raise ValueError(f"Tarea no reconocida: {task_name}")
        except Exception as e:
            log_error(logger,f"Error al delegar tarea '{task_name}': {e}")
            traceback.print_exc()
            self.state = AgentState.ERROR

    # -------------------------------------------------------------------------
    # Monitoreo y estado
    # -------------------------------------------------------------------------
    def monitor_progress(self) -> str:
        """Devuelve el estado actual del agente."""
        return f"Estado actual del agente: {self.state.value}"

    def get_agent_state(self) -> AgentState:
        """Obtiene el estado actual del agente."""
        return self.state

    # -------------------------------------------------------------------------
    # Reinicio y limpieza
    # -------------------------------------------------------------------------
    def reset_agent(self) -> None:
        """Reinicia el agente y limpia sus memorias previas."""
        try:
            log_info(logger,"Reiniciando agente y limpiando memoria...")
            if self.agent:
                self.agent.reset_memory()
            self.state = AgentState.IDLE
            log_info(logger,"Agente reiniciado correctamente.")
        except Exception as e:
            log_error(logger,f"Error al reiniciar agente: {e}")
            self.state = AgentState.ERROR
            traceback.print_exc()
