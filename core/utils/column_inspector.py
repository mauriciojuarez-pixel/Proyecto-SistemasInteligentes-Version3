# core/utils/column_inspector.py
import pandas as pd

def infer_column_roles(df: pd.DataFrame) -> dict:
    """
    Infiera el rol de cada columna automáticamente basado en el tipo de datos
    y nombres de columna.
    
    Retorna un diccionario {columna: rol_descriptivo}.
    """
    roles = {}
    for col in df.columns:
        dtype = df[col].dtype
        name_lower = col.lower()

        # Heurísticas por nombre
        if any(k in name_lower for k in ["precio", "monto", "total", "importe"]):
            role = "numérico, monto/valor monetario"
        elif any(k in name_lower for k in ["cantidad", "stock", "unidades"]):
            role = "numérico, cantidad"
        elif any(k in name_lower for k in ["cliente", "usuario", "nombre"]):
            role = "categórico, nombre de cliente/usuario"
        elif any(k in name_lower for k in ["producto", "item", "servicio"]):
            role = "categórico, producto/servicio"
        elif any(k in name_lower for k in ["pais", "ciudad", "region"]):
            role = "categórico, ubicación geográfica"
        elif "fecha" in name_lower or "time" in name_lower:
            role = "fecha, timestamp"
        else:
            # fallback por tipo
            if pd.api.types.is_numeric_dtype(dtype):
                role = "numérico, no clasificado"
            elif pd.api.types.is_datetime64_any_dtype(dtype):
                role = "fecha, no clasificada"
            else:
                role = "categórico, no clasificado"

        roles[col] = role
    return roles
