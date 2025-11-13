# Reporte del Proyecto Maquiña

**Fecha de generación:** 2025-11-12 17:13:07

## Información del Sistema

| Parámetro | Valor |
|------------|-------|
| Sistema Operativo | Windows |
| Versión OS | 10.0.19045 |
| Arquitectura | AMD64 |
| Procesador | Intel64 Family 6 Model 151 Stepping 2, GenuineIntel |
| CPU Núcleos | 24 |
| RAM Total (GB) | 15.82 |
| Uso actual de CPU (%) | 7.0 |
| Uso actual de RAM (%) | 67.8 |

## Dependencias Instaladas

```
PySocks==1.7.1
absl-py==2.3.1
accelerate==1.11.0
altgraph==0.17.4
annotated-types==0.7.0
anyio==4.11.0
astunparse==1.6.3
attrs==25.4.0
autocommand==2.2.2
backports.tarfile==1.2.0
beautifulsoup4==4.14.2
blinker==1.9.0
certifi==2025.10.5
cffi==1.17.1
charset-normalizer==3.4.3
click==8.3.0
clipspy==1.0.5
colorama==0.4.6
contourpy==1.3.3
customtkinter==5.2.2
cycler==0.12.1
darkdetect==0.8.0
deepface==0.0.95
et-xmlfile==2.0.0
filelock==3.20.0
fire==0.7.1
flask-cors==6.0.1
flask==3.1.2
flatbuffers==25.9.23
fonttools==4.60.1
fpdf==1.7.2
fsspec==2025.10.0
gast==0.6.0
gdown==5.2.0
google-pasta==0.2.0
grpcio==1.75.1
gunicorn==23.0.0
h11==0.16.0
h5py==3.14.0
hf-xet==1.2.0
httpcore==1.0.9
httpx==0.28.1
huggingface-hub==0.36.0
idna==3.10
importlib-metadata==8.0.0
imutils==0.5.4
inflect==7.3.1
iniconfig==2.3.0
itsdangerous==2.2.0
jaraco.collections==5.1.0
jaraco.context==5.3.0
jaraco.functools==4.0.1
jaraco.text==3.12.1
jinja2==3.1.6
joblib==1.5.2
jsonpatch==1.33
jsonpointer==3.0.0
jsonschema-specifications==2025.9.1
jsonschema==4.25.1
keras==3.11.3
kiwisolver==1.4.9
langchain-core==1.0.4
langchain==1.0.5
langchainhub==0.1.21
langgraph-checkpoint==3.0.1
langgraph-prebuilt==1.0.2
langgraph-sdk==0.2.9
langgraph==1.0.2
langsmith==0.4.42
libclang==18.1.1
loguru==0.7.3
lz4==4.4.4
markdown-it-py==4.0.0
markdown==3.9
markupsafe==3.0.3
matplotlib==3.10.7
mdurl==0.1.2
ml-dtypes==0.5.3
more-itertools==10.3.0
mpmath==1.3.0
mtcnn==1.0.0
namex==0.1.0
networkx==3.5
numpy==2.3.4
opencv-contrib-python==4.12.0.88
openpyxl==3.1.5
opt-einsum==3.4.0
optree==0.17.0
orjson==3.11.4
ormsgpack==1.12.0
packaging==24.1
pandas==2.3.3
pefile==2023.2.7
pillow==12.0.0
pip==25.2
platformdirs==4.2.2
pluggy==1.6.0
protobuf==6.32.1
psutil==7.1.3
pycparser==2.22
pydantic-core==2.41.5
pydantic==2.12.4
pygments==2.19.2
pyinstaller-hooks-contrib==2025.9
pyinstaller==6.16.0
pyparsing==3.2.5
pytest==9.0.0
python-dateutil==2.9.0.post0
python-dotenv==1.2.1
pytz==2025.2
pywin32-ctypes==0.2.3
pyyaml==6.0.3
referencing==0.37.0
regex==2025.11.3
reportlab==4.4.4
requests-toolbelt==1.0.0
requests==2.32.5
retina-face==0.0.17
rich==14.2.0
rpds-py==0.28.0
safetensors==0.6.2
scikit-learn==1.7.2
scipy==1.16.3
sentencepiece==0.2.1
setuptools==80.9.0
shellingham==1.5.4
six==1.17.0
sniffio==1.3.1
soupsieve==2.8
sympy==1.14.0
tenacity==9.1.2
tensorboard-data-server==0.7.2
tensorboard==2.20.0
tensorflow==2.20.0
termcolor==3.1.0
tf-keras==2.20.1
threadpoolctl==3.6.0
tokenizers==0.22.1
tomli==2.0.1
torch==2.9.0
tqdm==4.67.1
transformers==4.57.1
typeguard==4.3.0
typer-slim==0.20.0
types-requests==2.32.4.20250913
typing-extensions==4.15.0
typing-inspection==0.4.2
tzdata==2025.2
urllib3==2.5.0
werkzeug==3.1.3
wheel==0.45.1
win32-setctime==1.2.0
wrapt==1.17.3
xlsxwriter==3.2.9
xxhash==3.6.0
zipp==3.19.2
zstandard==0.25.0
```

## Estructura del Proyecto

```
.env
data
data\datasets
data\datasets\processed
data\datasets\raw
data\models
data\models\fine_tuned
data\models\gemma_2b_it
data\models\gemma_2b_it\.cache
data\models\gemma_2b_it\.cache\huggingface
data\models\gemma_2b_it\.cache\huggingface\.gitignore
data\models\gemma_2b_it\.cache\huggingface\download
data\models\gemma_2b_it\.cache\huggingface\download\.gitattributes.metadata
data\models\gemma_2b_it\.cache\huggingface\download\README.md.metadata
data\models\gemma_2b_it\.cache\huggingface\download\config.json.metadata
data\models\gemma_2b_it\.cache\huggingface\download\gemma-2b-it.gguf.metadata
data\models\gemma_2b_it\.cache\huggingface\download\generation_config.json.metadata
data\models\gemma_2b_it\.cache\huggingface\download\model-00001-of-00002.safetensors.metadata
data\models\gemma_2b_it\.cache\huggingface\download\model-00002-of-00002.safetensors.metadata
data\models\gemma_2b_it\.cache\huggingface\download\model.safetensors.index.json.metadata
data\models\gemma_2b_it\.cache\huggingface\download\special_tokens_map.json.metadata
data\models\gemma_2b_it\.cache\huggingface\download\tokenizer.json.metadata
data\models\gemma_2b_it\.cache\huggingface\download\tokenizer.model.metadata
data\models\gemma_2b_it\.cache\huggingface\download\tokenizer_config.json.metadata
data\models\gemma_2b_it\.gitattributes
data\models\gemma_2b_it\README.md
data\models\gemma_2b_it\config.json
data\models\gemma_2b_it\gemma-2b-it.gguf
data\models\gemma_2b_it\generation_config.json
data\models\gemma_2b_it\model-00001-of-00002.safetensors
data\models\gemma_2b_it\model-00002-of-00002.safetensors
data\models\gemma_2b_it\model.safetensors.index.json
data\models\gemma_2b_it\special_tokens_map.json
data\models\gemma_2b_it\tokenizer.json
data\models\gemma_2b_it\tokenizer.model
data\models\gemma_2b_it\tokenizer_config.json
data\outputs
data\outputs\logs
data\outputs\logs\benchmark.log
data\outputs\logs\setup_env.log
data\outputs\metrics
data\outputs\reports
data\outputs\reports\benchmark_report.txt
docs
docs\reports
requirements.txt
scripts
scripts\__pycache__
scripts\__pycache__\utils.cpython-313.pyc
scripts\cleanup_outputs.py
scripts\others
scripts\others\benchmark.py
scripts\others\generate_report.py
scripts\others\update_model.py
scripts\setup_env.py
scripts\utils.py
scripts\verify
scripts\verify\__pycache__
scripts\verify\__pycache__\verify_requirements.cpython-313.pyc
scripts\verify\__pycache__\verify_setup.cpython-313.pyc
scripts\verify\verify_requirements.py
scripts\verify\verify_setup.py
```

## Logs Recientes

```
Archivo: benchmark.log2025-11-12 17:13:00,737 - INFO - Inicio del benchmark del sistema.
2025-11-12 17:13:05,756 - INFO - CPU promedio: 4.34% | RAM promedio: 68.12%
2025-11-12 17:13:06,144 - INFO - Tarea de prueba completada en 0.39 segundos
2025-11-12 17:13:06,151 - INFO - Reporte generado en D:\Proyecto-SistemasInteligentes-Version3\data\outputs\reports\benchmark_report.txt
2025-11-12 17:13:06,151 - INFO - Benchmark completado exitosamente.
2025-11-12 17:13:06,151 - INFO - Log detallado guardado en D:\Proyecto-SistemasInteligentes-Version3\data\outputs\logs\benchmark.log
```

---
_Generado automáticamente por `generate_report.py`_