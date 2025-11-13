
# core/heavy_modules/fine_tuning/evaluate_model.py

import numpy as np
from sklearn.metrics import accuracy_score, f1_score, classification_report
from core.utils.logger import init_logger, log_info, log_error
import json
from pathlib import Path

logger = init_logger("EvaluateModel")


def compute_metrics(pred):
    """
    Calcula métricas básicas (accuracy, f1).
    """
    try:
        labels = pred.label_ids
        preds = np.argmax(pred.predictions, axis=1)
        metrics = {
            "accuracy": accuracy_score(labels, preds),
            "f1": f1_score(labels, preds, average="weighted")
        }
        log_info(logger, f"Métricas calculadas: {metrics}")
        return metrics
    except Exception as e:
        log_error(logger, f"Error al calcular métricas: {e}")
        raise


def compare_with_baseline(new_results: dict, baseline_results: dict):
    """
    Compara los resultados actuales con una línea base anterior.
    """
    try:
        comparison = {metric: new_results[metric] - baseline_results.get(metric, 0)
                      for metric in new_results.keys()}
        log_info(logger, f"Comparación con baseline: {comparison}")
        return comparison
    except Exception as e:
        log_error(logger, f"Error al comparar con baseline: {e}")
        raise


def generate_evaluation_report(metrics: dict, output_file: str = "reports/evaluation/eval_results.json"):
    """
    Genera un reporte de evaluación en JSON.
    """
    try:
        Path(output_file).parent.mkdir(parents=True, exist_ok=True)
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(metrics, f, indent=4)
        log_info(logger, f"Reporte de evaluación generado: {output_file}")
    except Exception as e:
        log_error(logger, f"Error al generar reporte de evaluación: {e}")
        raise
