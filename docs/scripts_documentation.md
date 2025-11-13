# Documentación de Scripts

Este documento resume los scripts del proyecto, sus módulos y funciones principales.

---

## 1. `auto_clean_data.py`
**Descripción:** Limpieza automática de datasets en `data/datasets/raw/` y guardado en `data/datasets/processed/`.

| Función | Descripción | Uso |
|---------|------------|-----|
| `scan_raw_folder()` | Busca archivos CSV y Excel nuevos en raw/ | Usado internamente para detectar datasets nuevos |
| `clean_dataset(file_path: Path)` | Limpia un dataset usando `DataManager` y lo guarda | Ejecuta limpieza sobre un archivo específico |
| `clean_all_files()` | Aplica limpieza automática a todos los archivos en raw/ | Ejecutable principal |
| `log(message: str, level="info")` | Logger unificado (consola + archivo) | Uso interno para registro |

---

## 2. `generate_report_auto.py`
**Descripción:** Genera reportes completos en PDF y Excel usando datasets procesados y modelo Gemma 2B IT.

| Función | Descripción | Uso |
|---------|------------|-----|
| `ensure_directories()` | Verifica o crea la carpeta de reportes | Uso interno |
| `load_all_processed_data() -> pd.DataFrame` | Carga todos los datasets procesados en un DataFrame | Base para generar reporte |
| `generate_report_auto()` | Genera reporte completo, agrega metadata, insights y exporta a PDF/Excel | Ejecutable principal |
| `log(message: str, level="info")` | Logger unificado | Uso interno |

---

## 3. `generate_sample_data.py`
**Descripción:** Genera datasets sintéticos para pruebas, CSV y Excel, con opción de añadir ruido.

| Función | Descripción | Uso |
|---------|------------|-----|
| `generate_sample_rows(num_rows=100)` | Crea filas de datos sintéticos | Generar datos base |
| `add_noise(df: pd.DataFrame, noise_level=0.05)` | Introduce ruido aleatorio a columnas numéricas | Para pruebas de robustez |
| `save_csv(df: pd.DataFrame, filename="sample_data.csv")` | Guarda dataset en CSV | Exportar dataset |
| `save_excel(df: pd.DataFrame, filename="sample_data.xlsx")` | Guarda dataset en Excel | Exportar dataset |
| `generate_sample_data(num_rows=100, add_noise_flag=False)` | Genera dataset completo CSV + Excel con opción de ruido | Ejecutable principal |
| `log(message: str, level="info")` | Logger unificado | Uso interno |

---

## 4. `manage_training.py`
**Descripción:** Gestiona entrenamiento y reentrenamiento (fine-tuning) del modelo Gemma 2B IT.

| Función | Descripción | Uso |
|---------|------------|-----|
| `run_training(epochs=3, batch_size=32, incremental=False)` | Ejecuta entrenamiento o reentrenamiento, evalúa métricas, rollback si falla | Ejecutable principal |
| `log(message: str, level="info")` | Logger unificado | Uso interno |

---

## 5. `setup_env.py`
**Descripción:** Inicializa estructura de carpetas y archivos necesarios para el proyecto.

| Función | Descripción | Uso |
|---------|------------|-----|
| `create_folder(path: Path)` | Crea carpeta si no existe | Uso interno |
| `initialize_directories()` | Inicializa todas las carpetas del proyecto | Uso interno |
| `initialize_version_file()` | Crea archivo de versiones para fine-tuning si no existe | Uso interno |
| `initialize_environment()` | Inicializa entorno completo (carpetas + archivo de versiones) | Ejecutable principal |

---

## 6. `update_model.py`
**Descripción:** Descarga o actualiza modelo base Gemma 2B IT desde Hugging Face y prepara carpetas para fine-tuning.

| Función | Descripción | Uso |
|---------|------------|-----|
| `ensure_directories()` | Verifica y crea carpetas de modelos y checkpoints | Uso interno |
| `clone_or_update_model()` | Descarga modelo base usando `snapshot_download` | Uso interno |
| `prepare_finetune_folder()` | Prepara carpetas para fine-tuning y checkpoints | Uso interno |
| `update_model()` | Flujo completo de actualización del modelo | Ejecutable principal |
| `log(message: str)` | Logger unificado | Uso interno |

---

## 7. `verify_requirements.py`
**Descripción:** Verifica que todas las librerías del proyecto estén instaladas, opcionalmente instala faltantes.

| Función | Descripción | Uso |
|---------|------------|-----|
| `read_requirements(file_path: Path)` | Lee `requirements.txt` | Uso interno |
| `check_package(pkg: str)` | Verifica si paquete está instalado | Uso interno |
| `install_package(pkg: str)` | Instala paquete con pip | Uso interno |
| `verify_requirements(auto_install=False)` | Verifica dependencias y opcionalmente instala faltantes | Ejecutable principal |
| `log(message: str)` | Logger unificado | Uso interno |

---

