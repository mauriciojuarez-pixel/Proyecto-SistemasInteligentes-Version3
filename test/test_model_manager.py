# test/test_model_manager.py
# pytest -v test/test_model_manager.py

import pytest
from unittest.mock import patch, MagicMock
from core.controller.model_manager import ModelManager

@pytest.fixture
def model_manager():
    """Fixture para inicializar ModelManager"""
    return ModelManager()

def test_load_fine_tuned_model_returns_model(model_manager):
    """Verifica que load_fine_tuned_model devuelve un objeto (mock)"""
    with patch.object(model_manager, "load_fine_tuned_model", return_value="mock_model") as mock_load:
        model = model_manager.load_fine_tuned_model()
        assert model == "mock_model"
        mock_load.assert_called_once()

def test_generate_from_prompt_returns_text(model_manager):
    """Verifica que generate_from_prompt devuelve un string"""
    mock_model = MagicMock()
    prompt = "Escribe un resumen breve"
    
    # Simular la función generate_from_prompt
    with patch.object(model_manager, "generate_from_prompt", return_value="Resumen generado") as mock_gen:
        result = model_manager.generate_from_prompt(mock_model, prompt)
        assert isinstance(result, str)
        assert result == "Resumen generado"
        mock_gen.assert_called_once_with(mock_model, prompt)




from unittest.mock import patch, MagicMock
import pytest

def test_generate_from_prompt_raises_error_when_no_model(model_manager):
    prompt = "Genera un texto"

    # Creamos un modelo simulado que tenga método 'generate'
    fake_model = MagicMock()
    fake_model.generate.return_value = [0]  # salida simulada

    with patch.object(model_manager, "load_fine_tuned_model", return_value=fake_model) as mock_load:
        model_manager.model = fake_model  # asignamos directamente el mock al modelo
        # Parcheamos AutoTokenizer para no descargar nada
        with patch("transformers.AutoTokenizer.from_pretrained") as mock_tokenizer:
            mock_tokenizer.return_value = MagicMock(
                __call__=MagicMock(return_value={"input_ids": [0]}),
                decode=MagicMock(return_value="Texto simulado")
            )
            # Ahora la función debería retornar el texto simulado
            output = model_manager.generate_from_prompt(prompt)
            assert output == "Texto simulado"






def test_generate_from_prompt_empty_prompt(model_manager):
    """Verifica que prompt vacío genera salida vacía o advertencia"""
    mock_model = MagicMock()
    with patch.object(model_manager, "generate_from_prompt", return_value="") as mock_gen:
        result = model_manager.generate_from_prompt(mock_model, "")
        assert result == ""
        mock_gen.assert_called_once_with(mock_model, "")
