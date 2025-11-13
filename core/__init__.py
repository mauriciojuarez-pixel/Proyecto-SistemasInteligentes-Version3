import sys
import os

# Obtener la ruta absoluta del proyecto (2 niveles arriba de este archivo)
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

# Agregar la raíz del proyecto al sys.path si no está ya incluida
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)
