import torch
from transformers import AutoModelForCausalLM, Trainer, TrainingArguments
from utils.logger import log_info, log_error
from pathlib import Path

def initialize_trainer(model_name: str, train_dataset, eval_dataset, output_dir: str = "models/fine_tuned"):
    """
    Inicializa el Trainer de Hugging Face para entrenamiento supervisado.
    """
    try:
        model = AutoModelForCausalLM.from_pretrained(model_name)

        args = TrainingArguments(
            output_dir=output_dir,
            evaluation_strategy="epoch",
            save_strategy="epoch",
            learning_rate=5e-5,
            per_device_train_batch_size=4,
            per_device_eval_batch_size=4,
            num_train_epochs=3,
            weight_decay=0.01,
            logging_dir=f"{output_dir}/logs",
            logging_steps=10,
            push_to_hub=False
        )

        trainer = Trainer(
            model=model,
            args=args,
            train_dataset=train_dataset,
            eval_dataset=eval_dataset
        )

        log_info(f"Trainer inicializado correctamente con modelo: {model_name}")
        return trainer
    except Exception as e:
        log_error(f"Error al inicializar Trainer: {e}")
        raise

def train(trainer, epochs: int = 3):
    """
    Ejecuta el proceso de entrenamiento.
    """
    try:
        trainer.args.num_train_epochs = epochs
        log_info(f"Iniciando entrenamiento por {epochs} épocas...")
        trainer.train()
        log_info("Entrenamiento finalizado exitosamente.")
    except Exception as e:
        log_error(f"Error durante el entrenamiento: {e}")
        raise

def track_progress(trainer):
    """
    Retorna las métricas de progreso registradas durante el entrenamiento.
    """
    try:
        logs = trainer.state.log_history
        log_info(f"Progreso del entrenamiento capturado: {len(logs)} entradas.")
        return logs
    except Exception as e:
        log_error(f"Error al obtener progreso del entrenamiento: {e}")
        raise

def log_results(logs, output_file: str = "reports/training/training_log.json"):
    """
    Guarda los logs del entrenamiento en un archivo JSON.
    """
    import json
    try:
        Path(output_file).parent.mkdir(parents=True, exist_ok=True)
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(logs, f, indent=4)
        log_info(f"Resultados del entrenamiento guardados en {output_file}")
    except Exception as e:
        log_error(f"Error al guardar logs de entrenamiento: {e}")
        raise
