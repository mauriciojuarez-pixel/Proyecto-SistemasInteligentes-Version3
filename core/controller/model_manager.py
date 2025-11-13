# core/controller/model_manager.py

import os
import json
import pandas as pd
from datetime import datetime
from core.utils.logger import log_info, log_error
from core.heavy_modules.fine_tuning.data_preparation import (
    clean_training_data,
    tokenize_texts,
    balance_classes,
    split_train_test
)
from core.heavy_modules.fine_tuning.train_model import Trainer
from core.heavy_modules.fine_tuning.evaluate_model import (
    compute_metrics,
    compare_with_baseline,
    generate_evaluation_report
)
from core.heavy_modules.fine_tuning.model_saver import (
    save_checkpoint,
    load_checkpoint,
    list_model_versions,
    delete_old_models
)
from core.heavy_modules.analytics.statistical_summary import compute_descriptive_stats
from core.heavy_modules.analytics.correlation_analysis import compute_correlations, detect_multicollinearity
from core.heavy_modules.analytics.anomaly_detection import detect_outliers, remove_anomalies

MODEL_DIR = "models/"
REGISTRY_PATH = os.path.join(MODEL_DIR, "registry.json")


class ModelManager:
    """
    Controla el ciclo de vida del modelo Gemma 2B IT:
    carga, fine-tuning, evaluación y versionado.
    """

    def __init__(self):
        self.model = None
        self.current_version = None
        self._ensure_registry()

    def _ensure_registry(self):
        if not os.path.exists(MODEL_DIR):
            os.makedirs(MODEL_DIR)
        if not os.path.exists(REGISTRY_PATH):
            with open(REGISTRY_PATH, "w") as f:
                json.dump({"versions": []}, f)

    # ---------------------------------------------------------------
    # 1. Cargar modelo
    # ---------------------------------------------------------------
    def load_model(self, version="latest"):
        try:
            versions = list_model_versions()
            if not versions:
                raise FileNotFoundError("No hay versiones registradas del modelo.")
            
            if version == "latest":
                version = versions[-1]

            self.model = load_checkpoint(version)
            self.current_version = version
            log_info(f"Modelo '{version}' cargado correctamente.")
            return self.model
        except Exception as e:
            log_error(f"Error al cargar el modelo: {e}")
            raise

    # ---------------------------------------------------------------
    # 2. Preparar datos para fine-tuning
    # ---------------------------------------------------------------
    def prepare_data_for_finetuning(self, df: pd.DataFrame):
        try:
            df_clean = clean_training_data(df)
            tokenized = tokenize_texts(df_clean)
            balanced = balance_classes(tokenized)
            train_data, val_data = split_train_test(balanced)
            log_info("Datos preparados correctamente para fine-tuning.")
            return train_data, val_data
        except Exception as e:
            log_error(f"Error en la preparación de datos: {e}")
            raise

    # ---------------------------------------------------------------
    # 3. Fine-tuning
    # ---------------------------------------------------------------
    def fine_tune(self, df: pd.DataFrame, epochs=3, batch_size=32):
        try:
            train_data, val_data = self.prepare_data_for_finetuning(df)
            trainer = Trainer(self.model)
            trainer.train(train_data, val_data, epochs=epochs, batch_size=batch_size)
            
            version_name = f"fine_tuned_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            save_checkpoint(self.model, version_name)
            self.current_version = version_name
            log_info(f"Fine-tuning completado. Versión '{version_name}' guardada.")
        except Exception as e:
            log_error(f"Error en el fine-tuning: {e}")
            raise

    # ---------------------------------------------------------------
    # 4. Evaluación
    # ---------------------------------------------------------------
    def evaluate_model(self, metrics: list):
        try:
            results = compute_metrics(self.model, metrics)
            comparison = compare_with_baseline(results)
            generate_evaluation_report(results, comparison)
            log_info("Evaluación completada correctamente.")
            return results
        except Exception as e:
            log_error(f"Error al evaluar el modelo: {e}")
            raise

    # ---------------------------------------------------------------
    # 5. Rollback a versión anterior
    # ---------------------------------------------------------------
    def rollback_to_previous_version(self):
        try:
            versions = list_model_versions()
            if len(versions) < 2:
                raise RuntimeError("No hay versión anterior disponible.")
            
            previous_version = versions[-2]
            self.model = load_checkpoint(previous_version)
            self.current_version = previous_version
            log_info(f"Rollback realizado a la versión: {previous_version}")
        except Exception as e:
            log_error(f"Error en rollback: {e}")
            raise
