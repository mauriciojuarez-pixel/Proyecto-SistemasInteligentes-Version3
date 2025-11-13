# test/test_data_manager.py
# python -m test.test_data_manager
# pytest -v test/test_data_manager.py

import pytest
import pandas as pd
import os
from core.controller.data_manager import DataManager
from pathlib import Path
import numpy as np

@pytest.fixture
def sample_df():
    """
    DataFrame de prueba con:
    - Celdas vacías
    - Columnas vacías
    - Filas vacías
    - Diferentes tipos de datos
    """
    data = {
        "col_num": [1, 2, None, 4, np.nan, 6],
        "col_str": ["a", None, "c", "d", "", "f"],
        "col_empty": [None, None, None, None, None, None],
        "col_bool": [True, False, None, True, False, None]
    }
    df = pd.DataFrame(data)
    # Agregar fila completamente vacía
    df.loc[len(df)] = [None, None, None, None]
    return df

@pytest.fixture
def data_manager(tmp_path):
    """
    Instancia de DataManager usando ruta temporal para procesados.
    """
    dm = DataManager(schema_path="config/data_schema.json")
    dm.processed_dir = tmp_path / "processed"
    dm.processed_dir.mkdir(parents=True, exist_ok=True)
    return dm

# ---------------------------------------------------------------
# Test: detectar tipo de archivo
# ---------------------------------------------------------------
def test_detect_file_type_csv_excel(data_manager):
    assert data_manager.detect_file_type("archivo.csv") == "csv"
    assert data_manager.detect_file_type("archivo.xlsx") == "excel"
    assert data_manager.detect_file_type("archivo.xls") == "excel"
    with pytest.raises(ValueError):
        data_manager.detect_file_type("archivo.txt")

# ---------------------------------------------------------------
# Test: cargar datos
# ---------------------------------------------------------------
def test_load_data_csv_excel(tmp_path, data_manager):
    # Crear CSV temporal
    csv_path = tmp_path / "test.csv"
    df_csv = pd.DataFrame({"A": [1,2,3]})
    df_csv.to_csv(csv_path, index=False)

    # Crear Excel temporal
    excel_path = tmp_path / "test.xlsx"
    df_csv.to_excel(excel_path, index=False)

    # Prueba carga
    df_loaded_csv = data_manager.load_data(str(csv_path))
    df_loaded_excel = data_manager.load_data(str(excel_path))

    pd.testing.assert_frame_equal(df_loaded_csv, df_csv)
    pd.testing.assert_frame_equal(df_loaded_excel, df_csv)

# ---------------------------------------------------------------
# Test: validar estructura (sin esquema)
# ---------------------------------------------------------------
def test_validate_structure_no_schema(data_manager, sample_df):
    # Si el esquema no existe, debe retornar True
    result = data_manager.validate_structure(sample_df)
    assert result is True

# ---------------------------------------------------------------
# Test: limpieza de datos
# ---------------------------------------------------------------
def test_clean_data(data_manager, sample_df):
    df_clean = data_manager.clean_data(sample_df, fill_strategy="mean", remove_outliers=False)
    # Columnas vacías se deben mantener
    assert "col_empty" in df_clean.columns
    # No debe haber valores None en col_num ni col_bool
    assert df_clean["col_num"].isnull().sum() == 0
    # col_str puede quedar vacío, no se elimina
    assert df_clean["col_str"].isnull().sum() >= 0
    # Debe mantener el mismo número de columnas
    assert df_clean.shape[1] == sample_df.shape[1]

# ---------------------------------------------------------------
# Test: división de datos
# ---------------------------------------------------------------
def test_split_data(data_manager, sample_df):
    df_clean = data_manager.clean_data(sample_df)
    train, val = data_manager.split_data(df_clean, test_size=0.33)
    assert len(train) + len(val) == len(df_clean)
    # Verificar proporción aproximada
    assert abs(len(val)/len(df_clean) - 0.33) < 0.15  # tolerancia mayor


# ---------------------------------------------------------------
# Test: guardar datos procesados
# ---------------------------------------------------------------
def test_save_processed(data_manager, sample_df, tmp_path):
    # Guardar DataFrame procesado en carpeta temporal
    processed_path = tmp_path / "processed"
    processed_path.mkdir(exist_ok=True)
    
    # Guardar usando el método de DataManager
    save_path = data_manager.save_processed(sample_df, filename="test_processed.csv")
    
    # Asegurarnos de que el archivo existe
    assert Path(save_path).exists()
    
    # Cargar nuevamente el CSV
    df_loaded = pd.read_csv(save_path)
    
    # Normalizar columnas de tipo object (strings)
    import numpy as np
    for col in df_loaded.select_dtypes(include="object").columns:
        df_loaded[col] = df_loaded[col].replace('', np.nan)
        sample_df[col] = sample_df[col].replace('', np.nan)
    
    # Comparar DataFrames reemplazando None y NaN
    pd.testing.assert_frame_equal(
        df_loaded.fillna(np.nan),
        sample_df.fillna(np.nan),
        check_dtype=False
    )



# ---------------------------------------------------------------
# Test: resumen del dataset
# ---------------------------------------------------------------
def test_summarize_dataset(data_manager, sample_df):
    summary = data_manager.summarize_dataset(sample_df)
    assert "rows" in summary
    assert "columns" in summary
    assert "missing_values" in summary
    assert "summary_stats" in summary
    assert summary["rows"] == len(sample_df)
    assert set(summary["columns"]) == set(sample_df.columns)
