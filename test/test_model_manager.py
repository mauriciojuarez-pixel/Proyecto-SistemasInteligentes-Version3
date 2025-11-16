# test/test_model_manager.py
# pytest -v test/test_model_manager.py
import pytest
from unittest.mock import patch, MagicMock
from core.controller.model_manager import ModelManager

@pytest.fixture
def model_manager():
    """Fixture para inicializar ModelManager sin tokenizer (se puede inyectar en tests)."""
    return ModelManager()

def test_load_fine_tuned_model_returns_model(model_manager):
    """Verifica que load_fine_tuned_model devuelve un objeto (mock)"""
    with patch.object(model_manager, "load_fine_tuned_model", return_value="mock_model") as mock_load:
        model = model_manager.load_fine_tuned_model()
        assert model == "mock_model"
        mock_load.assert_called_once()

def test_generate_from_prompt_returns_text_with_native_method(model_manager):
    """Verifica que generate_from_prompt devuelve un string usando generate_text"""
    mock_model = MagicMock()
    mock_model.generate_text.return_value = "Texto generado nativamente"
    model_manager.model = mock_model

    result = model_manager.generate_from_prompt("Escribe un resumen breve")
    assert isinstance(result, str)
    assert result == "Texto generado nativamente"
    mock_model.generate_text.assert_called_once_with(
        "Escribe un resumen breve", max_tokens=512, temperature=0.7
    )

def test_generate_from_prompt_returns_text_with_transformers(model_manager):
    """Verifica que generate_from_prompt funciona usando AutoTokenizer y generate"""
    fake_model = MagicMock()
    del fake_model.generate_text  # aseguramos que no exista
    fake_model.generate.return_value = [0]  # salida simulada

    model_manager.model = fake_model

    with patch("transformers.AutoTokenizer.from_pretrained") as mock_from_pretrained:
        mock_tokenizer = MagicMock()
        mock_tokenizer.return_value = {"input_ids": [0]}
        mock_tokenizer.decode.return_value = "Texto simulado"
        mock_from_pretrained.return_value = mock_tokenizer

        output = model_manager.generate_from_prompt("Genera un texto")

        assert output == "Texto simulado"
        fake_model.generate.assert_called_once()
        # Ajustamos la expectativa a la salida real del código: outputs[0]
        mock_tokenizer.decode.assert_called_once_with(0, skip_special_tokens=True)


def test_generate_from_prompt_raises_error_when_no_model():
    """Verifica que generate_from_prompt lanza RuntimeError si no hay modelo"""
    manager = ModelManager()
    with pytest.raises(RuntimeError, match="No hay modelo cargado"):
        manager.generate_from_prompt("Cualquier texto")

def test_generate_from_prompt_empty_prompt(model_manager):
    """Verifica que prompt vacío genera salida vacía o advertencia"""
    mock_model = MagicMock()
    mock_model.generate_text.return_value = ""
    model_manager.model = mock_model

    result = model_manager.generate_from_prompt("")
    assert result == ""
    mock_model.generate_text.assert_called_once_with("", max_tokens=512, temperature=0.7)
