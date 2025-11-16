# core/utils/column_inspector.py
import pandas as pd
import json
import logging

logger = logging.getLogger("ColumnInspector")

def infer_column_roles(df: pd.DataFrame, use_model: bool = False) -> dict:
    """
    Infiera el rol de cada columna automáticamente.
    
    Si use_model=True, se utiliza Gemma 2B IT para inferir roles
    basándose en los valores de ejemplo. Si es False, se usan heurísticas simples.
    
    Retorna un diccionario {columna: rol_descriptivo}.
    """
    roles = {}

    if df.empty or df.shape[1] == 0:
        logger.warning("El DataFrame no tiene columnas.")
        return roles

    if use_model:
        try:
            # Import local para evitar circular import
            from core.utils.prompt_builder import BuilderPrompt

            prompt_builder = BuilderPrompt()
            prompt = prompt_builder.build_column_prompt(df)

            # Ejecutar Gemma para inferir roles
            response = prompt_builder.execute_model(prompt, max_length=500)

            # Intentar parsear JSON
            inferred_roles = json.loads(response)
            if isinstance(inferred_roles, dict):
                return inferred_roles
            else:
                logger.warning("Respuesta de Gemma no es un JSON válido, usando heurísticas.")
        except Exception as e:
            logger.error(f"Error usando Gemma para inferir roles: {e}")
            logger.warning("Usando heurísticas simples como fallback.")

    # Fallback: heurísticas simples basadas en tipo y nombre
    for col in df.columns:
        dtype = df[col].dtype
        name_lower = col.lower()

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
            if pd.api.types.is_numeric_dtype(dtype):
                role = "numérico, no clasificado"
            elif pd.api.types.is_datetime64_any_dtype(dtype):
                role = "fecha, no clasificada"
            else:
                role = "categórico, no clasificado"

        roles[col] = role

    return roles
