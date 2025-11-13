# core/controller/model_manager.py

import os
import json
import pandas as pd
from datetime import datetime
from core.utils.logger import init_logger, log_info, log_error
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

# Inicializar logger central
logger = init_logger("ModelManager")

MODEL_DIR = "data/models/checkpoints"
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
        os.makedirs(MODEL_DIR, exist_ok=True)
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
            log_info(logger, f"Modelo '{version}' cargado correctamente.")
            return self.model
        except Exception as e:
            log_error(logger, f"Error al cargar el modelo: {e}")
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
            log_info(logger, "Datos preparados correctamente para fine-tuning.")
            return train_data, val_data
        except Exception as e:
            log_error(logger, f"Error en la preparación de datos: {e}")
            raise

    # ---------------------------------------------------------------
    # 3. Fine-tuning
    # ---------------------------------------------------------------
    def fine_tune(self, data_path: str, epochs=3, batch_size=32):
        try:
            df = pd.read_csv(data_path) if isinstance(data_path, str) else data_path
            train_data, val_data = self.prepare_data_for_finetuning(df)

            if not self.model:
                self.load_model("latest")

            trainer = Trainer(self.model)
            trainer.train(train_data, val_data, epochs=epochs, batch_size=batch_size)

            version_name = f"fine_tuned_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            save_checkpoint(self.model, version_name)
            self.current_version = version_name
            log_info(logger, f"Fine-tuning completado. Versión '{version_name}' guardada.")
        except Exception as e:
            log_error(logger, f"Error en el fine-tuning: {e}")
            raise

    # ---------------------------------------------------------------
    # 4. Evaluación
    # ---------------------------------------------------------------
    def evaluate_model(self, metrics: list):
        try:
            results = compute_metrics(self.model, metrics)
            comparison = compare_with_baseline(results)
            generate_evaluation_report(results, comparison)
            log_info(logger, "Evaluación completada correctamente.")
            return results
        except Exception as e:
            log_error(logger, f"Error al evaluar el modelo: {e}")
            raise

    # ---------------------------------------------------------------
    # 5. Comparar versiones
    # ---------------------------------------------------------------
    def compare_versions(self, old_model_version, new_model_version):
        try:
            old_model = load_checkpoint(old_model_version)
            new_model = load_checkpoint(new_model_version)
            comparison = compare_with_baseline([old_model, new_model])
            log_info(logger, f"Comparación entre versiones {old_model_version} y {new_model_version} realizada.")
            return comparison
        except Exception as e:
            log_error(logger, f"Error comparando versiones: {e}")
            raise

    # ---------------------------------------------------------------
    # 6. Guardar checkpoint
    # ---------------------------------------------------------------
    def save_model_checkpoint(self, name="fine_tuned_latest"):
        try:
            if not self.model:
                raise RuntimeError("No hay modelo cargado para guardar.")
            save_checkpoint(self.model, name)
            self.current_version = name
            log_info(logger, f"Checkpoint guardado: {name}")
        except Exception as e:
            log_error(logger, f"Error guardando checkpoint: {e}")
            raise

    # ---------------------------------------------------------------
    # 7. Cargar fine-tuned
    # ---------------------------------------------------------------
    def load_fine_tuned_model(self):
        try:
            versions = list_model_versions()
            if not versions:
                raise FileNotFoundError("No hay modelos fine-tuned disponibles.")
            latest = versions[-1]
            self.model = load_checkpoint(latest)
            self.current_version = latest
            log_info(logger, f"Modelo fine-tuned '{latest}' cargado correctamente.")
            return self.model
        except Exception as e:
            log_error(logger, f"Error cargando modelo fine-tuned: {e}")
            raise

    # ---------------------------------------------------------------
    # 8. Rollback
    # ---------------------------------------------------------------
    def rollback_to_previous_version(self):
        try:
            versions = list_model_versions()
            if len(versions) < 2:
                raise RuntimeError("No hay versión anterior disponible.")
            previous_version = versions[-2]
            self.model = load_checkpoint(previous_version)
            self.current_version = previous_version
            log_info(logger, f"Rollback realizado a la versión: {previous_version}")
        except Exception as e:
            log_error(logger, f"Error en rollback: {e}")
            raise

    # ---------------------------------------------------------------
    # 9. Generar texto a partir de un prompt
    # ---------------------------------------------------------------
    def generate_from_prompt(self, prompt: str, max_tokens: int = 512, temperature: float = 0.7) -> str:
        try:
            if not self.model:
                self.load_fine_tuned_model()

            if hasattr(self.model, "generate_text"):
                output = self.model.generate_text(prompt, max_tokens=max_tokens, temperature=temperature)
            else:
                from transformers import AutoTokenizer
                tokenizer = AutoTokenizer.from_pretrained("ruta_a_modelo_o_cache_local")
                inputs = tokenizer(prompt, return_tensors="pt")
                outputs = self.model.generate(**inputs, max_new_tokens=max_tokens)
                output = tokenizer.decode(outputs[0], skip_special_tokens=True)

            log_info(logger, "Texto generado correctamente a partir del prompt.")
            return output
        except Exception as e:
            log_error(logger, f"Error generando texto desde el prompt: {e}")
            raise
