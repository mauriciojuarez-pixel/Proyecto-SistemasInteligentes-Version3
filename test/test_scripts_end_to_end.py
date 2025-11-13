# test/test_scripts_end_to_end.py

import pytest
from pathlib import Path
import subprocess
import shutil

# --- Configuración paths ---
BASE_DIR = Path(__file__).resolve().parent
SCRIPTS_DIR = BASE_DIR.parent / "scripts"
SAMPLE_DATA_DIR = BASE_DIR / "sample_data"
RAW_DATA_DIR = BASE_DIR / "data/raw_test"
PROCESSED_DATA_DIR = BASE_DIR / "data/processed_test"
REPORTS_DIR = BASE_DIR / "data/reports_test"
LOGS_DIR = BASE_DIR / "data/logs_test"
MODELS_DIR = BASE_DIR / "data/models_test"

# --- Fixtures ---
@pytest.fixture(scope="module")
def setup_test_environment():
    """Crea carpetas temporales y copia datasets de prueba."""
    for folder in [RAW_DATA_DIR, PROCESSED_DATA_DIR, REPORTS_DIR, LOGS_DIR, MODELS_DIR]:
        folder.mkdir(parents=True, exist_ok=True)

    # Copiar datasets de prueba a raw_test
    for f in SAMPLE_DATA_DIR.glob("*.*"):
        shutil.copy(f, RAW_DATA_DIR / f.name)

    yield

    # Limpieza final después de tests
    shutil.rmtree(RAW_DATA_DIR)
    shutil.rmtree(PROCESSED_DATA_DIR)
    shutil.rmtree(REPORTS_DIR)
    shutil.rmtree(LOGS_DIR)
    shutil.rmtree(MODELS_DIR)


# --- Función de utilidad para ejecutar scripts ---
def run_script(script_name, args=None):
    cmd = ["python", str(SCRIPTS_DIR / script_name)]
    if args:
        cmd.extend(args)
    result = subprocess.run(cmd, capture_output=True, text=True)
    print(result.stdout)
    if result.returncode != 0:
        print(result.stderr)
        raise RuntimeError(f"Error ejecutando {script_name}")
    return result


# --- Tests de flujo completo ---
def test_auto_clean_data_script(setup_test_environment):
    """Ejecuta auto_clean_data.py sobre RAW_DATA_DIR"""
    run_script("auto_clean_data.py")
    # Verificar que archivos procesados existen
    processed_files = list(PROCESSED_DATA_DIR.glob("*.*"))
    assert len(processed_files) > 0
    print("Limpieza de datos completada correctamente.")


def test_generate_report_script(setup_test_environment):
    """Ejecuta generate_report_auto.py para generar reportes"""
    run_script("generate_report_auto.py")
    pdf_files = list(REPORTS_DIR.glob("*.pdf"))
    excel_files = list(REPORTS_DIR.glob("*.xlsx"))
    assert len(pdf_files) > 0
    assert len(excel_files) > 0
    print("Reportes generados correctamente.")


def test_manage_training_script(setup_test_environment):
    """Ejecuta manage_training.py para fine-tuning de modelo"""
    run_script("manage_training.py", args=["--epochs", "1", "--batch_size", "2"])
    # Verificar que existan modelos fine-tuned
    fine_tuned_models = list(MODELS_DIR.glob("gemma_2b_it_finetuned/*"))
    assert len(fine_tuned_models) > 0
    print("Fine-tuning completado correctamente.")
