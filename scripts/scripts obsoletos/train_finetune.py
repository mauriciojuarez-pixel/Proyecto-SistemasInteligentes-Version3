# scripts/train_finetune.py
"""
Módulo: train_finetune.py
Descripción:
    Reentrena (fine-tuning) el modelo Gemma 2B IT utilizando los datasets
    procesados gestionados por core.controller.data_manager.
    Ahora delega toda la gestión de modelos a core.controller.model_manager.
"""

from pathlib import Path
from core.controller.data_manager import DataManager
from core.controller.model_manager import ModelManager
from core.utils.logger.logger import init_logger
from transformers import AutoTokenizer, Trainer, TrainingArguments, TextDataset, DataCollatorForLanguageModeling

# --- Paths y configuración ---
BASE_DIR = Path(__file__).resolve().parent.parent
PROCESSED_DIR = BASE_DIR / "data" / "datasets" / "processed"
LOG_FILE = BASE_DIR / "data" / "outputs" / "logs" / "train_finetune.log"

logger = init_logger("train_finetune", LOG_FILE)

def log(message: str, level="info"):
    if level == "info":
        logger.info(message)
    elif level == "warning":
        logger.warning(message)
    elif level == "error":
        logger.error(message)
    print(message)

def prepare_dataset(file_path: Path, block_size=128):
    """Carga y tokeniza un dataset usando funciones del core."""
    df = load_data(str(file_path))  # core.controller.data_manager
    temp_file = PROCESSED_DIR / f"{file_path.stem}_token.txt"
    df.to_csv(temp_file, index=False, header=False)  # convertir a texto plano para transformers

    tokenizer = AutoTokenizer.from_pretrained(load_base_model())  # model_manager
    dataset = TextDataset(
        tokenizer=tokenizer,
        file_path=str(temp_file),
        block_size=block_size
    )
    return dataset, tokenizer

def train_model(dataset, tokenizer, epochs=3, batch_size=2):
    """Entrena el modelo y guarda checkpoint usando model_manager."""
    model = load_base_model()  # model_manager
    data_collator = DataCollatorForLanguageModeling(tokenizer=tokenizer, mlm=False)

    training_args = TrainingArguments(
        output_dir=str(BASE_DIR / "data" / "models" / "tmp_training"),
        overwrite_output_dir=True,
        num_train_epochs=epochs,
        per_device_train_batch_size=batch_size,
        logging_dir=str(LOG_FILE.parent),
        logging_steps=100,
    )

    trainer = Trainer(
        model=model,
        args=training_args,
        data_collator=data_collator,
        train_dataset=dataset
    )

    log("[INFO] Iniciando entrenamiento...")
    trainer.train()

    # Guardar modelo fine-tuned
    save_finetuned_model(trainer.model)  # model_manager
    log("[INFO] Modelo fine-tuned guardado con model_manager.")

    # Guardar checkpoint
    create_checkpoint(trainer.model)
    log("[INFO] Checkpoint registrado con model_manager.")

def run_finetuning(epochs=3, batch_size=2):
    """Ejecuta fine-tuning para todos los datasets procesados."""
    processed_files = list(PROCESSED_DIR.glob("*.*"))
    if not processed_files:
        log("[ERROR] No se encontraron archivos procesados para entrenamiento.", level="error")
        return

    for file_path in processed_files:
        log(f"[INFO] Procesando dataset: {file_path.name}")
        dataset, tokenizer = prepare_dataset(file_path)
        train_model(dataset, tokenizer, epochs=epochs, batch_size=batch_size)

# --- Ejecución ---
if __name__ == "__main__":
    run_finetuning(epochs=3, batch_size=2)
