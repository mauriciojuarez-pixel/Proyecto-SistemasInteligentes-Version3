# scripts/train_finetune.py
"""
Módulo: train_finetune.py
Descripción:
    Ejecuta el proceso de fine-tuning del modelo Gemma 2B IT utilizando los
    datasets limpios ubicados en data/datasets/processed/.

Flujo:
    1. Cargar el modelo base (Gemma 2B IT).
    2. Cargar datasets limpios.
    3. Preparar datos para entrenamiento (tokenización, batching).
    4. Ejecutar el fine-tuning con parámetros controlados.
    5. Guardar el modelo reentrenado en data/models/gemma_2b_it_finetuned/.
"""

# scripts/train_finetune.py

import sys
from pathlib import Path
from datetime import datetime
import logging
import shutil
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, Trainer, TrainingArguments, TextDataset, DataCollatorForLanguageModeling

# --- Configuración de rutas ---
BASE_DIR = Path(__file__).resolve().parent.parent
PROCESSED_DATA_DIR = BASE_DIR / "data" / "datasets" / "processed"
MODEL_DIR = BASE_DIR / "data" / "models" / "gemma_2b_it_base"
FINETUNED_DIR = BASE_DIR / "data" / "models" / "gemma_2b_it_finetuned"
CHECKPOINTS_DIR = BASE_DIR / "data" / "models" / "checkpoints"
LOG_FILE = BASE_DIR / "data" / "outputs" / "logs" / "train_finetune.log"

# --- Logger ---
logging.basicConfig(filename=LOG_FILE, level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger()

def log(message):
    print(message)
    logger.info(message)

# --- Funciones ---
def load_dataset(file_path: Path):
    if not file_path.exists():
        log(f"[ERROR] Archivo de dataset no encontrado: {file_path}")
        sys.exit(1)
    return str(file_path)

def train_finetuned_model(train_file: Path, epochs=3, batch_size=2, save_checkpoint=True):
    log("[INFO] Iniciando fine-tuning del modelo Gemma 2B IT...")

    tokenizer = AutoTokenizer.from_pretrained(MODEL_DIR)
    model = AutoModelForCausalLM.from_pretrained(MODEL_DIR)

    # Dataset para fine-tuning
    dataset = TextDataset(
        tokenizer=tokenizer,
        file_path=load_dataset(train_file),
        block_size=128
    )
    data_collator = DataCollatorForLanguageModeling(
        tokenizer=tokenizer, mlm=False
    )

    # Configuración del entrenamiento
    training_args = TrainingArguments(
        output_dir=str(FINETUNED_DIR),
        overwrite_output_dir=True,
        num_train_epochs=epochs,
        per_device_train_batch_size=batch_size,
        save_steps=500,
        save_total_limit=2,
        logging_dir=str(BASE_DIR / "data" / "outputs" / "logs"),
        logging_steps=100
    )

    trainer = Trainer(
        model=model,
        args=training_args,
        data_collator=data_collator,
        train_dataset=dataset
    )

    # Entrenamiento
    trainer.train()

    # Guardar modelo final
    trainer.save_model(FINETUNED_DIR)
    log(f"[INFO] Modelo fine-tuned guardado en {FINETUNED_DIR}")

    # Opcional: guardar checkpoint intermedio
    if save_checkpoint:
        checkpoint_path = CHECKPOINTS_DIR / f"checkpoint_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        shutil.copytree(FINETUNED_DIR, checkpoint_path)
        log(f"[INFO] Checkpoint guardado en {checkpoint_path}")

# --- Ejecución ---
if __name__ == "__main__":
    # Se asume que hay un solo archivo procesado, si hay más se puede iterar
    processed_files = list(PROCESSED_DATA_DIR.glob("*.txt"))
    if not processed_files:
        log("[ERROR] No se encontraron archivos procesados para entrenamiento.")
        sys.exit(1)

    train_finetuned_model(train_file=processed_files[0])
