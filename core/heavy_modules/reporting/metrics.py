# core/heavy_modules/reporting/metrics.py

from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from core.utils.logger import init_logger, log_info, log_error

logger = init_logger("Metrics")


def calculate_custom_metrics(predictions, labels) -> dict:
    try:
        metrics = {
            "accuracy": accuracy_score(labels, predictions),
            "precision": precision_score(labels, predictions, average="weighted", zero_division=0),
            "recall": recall_score(labels, predictions, average="weighted", zero_division=0),
            "f1_score": f1_score(labels, predictions, average="weighted", zero_division=0),
        }
        log_info(logger, "Métricas personalizadas calculadas correctamente.")
        return metrics
    except Exception as e:
        log_error(logger, f"Error calculando métricas: {e}")
        raise


def evaluate_model_performance(results: dict) -> dict:
    try:
        preds = results.get("predictions")
        labels = results.get("labels")
        if preds is None or labels is None:
            raise ValueError("Se requieren 'predictions' y 'labels' en los resultados.")
        metrics = calculate_custom_metrics(preds, labels)
        log_info(logger, "Evaluación de desempeño completada.")
        return metrics
    except Exception as e:
        log_error(logger, f"Error evaluando desempeño del modelo: {e}")
        raise


def summarize_results(metrics: dict) -> str:
    try:
        summary = (
            f"El modelo obtuvo un accuracy de {metrics.get('accuracy', 0):.2f}, "
            f"precision promedio de {metrics.get('precision', 0):.2f}, "
            f"recall de {metrics.get('recall', 0):.2f}, y un F1-score de {metrics.get('f1_score', 0):.2f}."
        )
        log_info(logger, "Resumen de resultados generado correctamente.")
        return summary
    except Exception as e:
        log_error(logger, f"Error generando resumen de métricas: {e}")
        raise
