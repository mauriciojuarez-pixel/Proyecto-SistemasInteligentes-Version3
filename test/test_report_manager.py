# test/test_report_manager.py
# pytest -v test/test_report_manager.py

import pytest
from unittest.mock import patch, MagicMock
from core.controller.report_manager import ReportManager

@pytest.fixture
def report_manager():
    """Fixture para inicializar ReportManager"""
    return ReportManager()

def test_generate_report_returns_string(report_manager):
    """Verifica que generate_report devuelve un string"""
    data = [{"id": 1, "value": 100}, {"id": 2, "value": 200}]
    insights = {"summary": "Prueba"}
    
    report = report_manager.generate_report(data, insights)
    
    assert isinstance(report, str)
    assert "Reporte" in report or len(report) > 0

def test_generate_report_logs_info(report_manager):
    """Verifica que generate_report llama a log_info"""
    data = [{"id": 1, "value": 100}]
    insights = {"summary": "Prueba"}
    
    with patch("core.utils.logger.log_info") as mock_log:
        report_manager.generate_report(data, insights)
        mock_log.assert_called()  # al menos una llamada a log_info

def test_generate_report_handles_none_data(report_manager):
    """Verifica que generate_report maneja None y llama a log_error"""
    insights = {"summary": "Prueba"}
    
    with patch("core.utils.logger.log_error") as mock_log:
        report = report_manager.generate_report(None, insights)
        assert isinstance(report, str)  # debe retornar algo seguro
        mock_log.assert_called()        # log_error debe llamarse

def test_generate_report_empty_data(report_manager):
    """Verifica que generate_report maneja lista vacía"""
    data = []
    insights = {"summary": "Prueba"}
    
    report = report_manager.generate_report(data, insights)
    assert isinstance(report, str)
    assert "sin datos" in report.lower() or len(report) > 0

def test_generate_summary_returns_dict(report_manager):
    """Verifica que generate_summary devuelve un dict con totales"""
    data = [{"id": 1, "value": 50}, {"id": 2, "value": 150}]
    summary = report_manager.generate_summary(data)
    
    assert isinstance(summary, dict)
    assert "total" in summary
    assert "count" in summary
    assert summary["total"] == 200
    assert summary["count"] == 2

def test_generate_summary_empty_list(report_manager):
    """Verifica que generate_summary maneja lista vacía"""
    data = []
    summary = report_manager.generate_summary(data)
    
    assert isinstance(summary, dict)
    assert summary["total"] == 0
    assert summary["count"] == 0
