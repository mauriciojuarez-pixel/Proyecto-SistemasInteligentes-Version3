#core/utils/time_utils.py

import time
from contextlib import contextmanager

def start_timer():
    return time.time()

def stop_timer(start_time):
    return time.time() - start_time

def elapsed_time(start_time, logger=None, task_name="Tarea"):
    duration = time.time() - start_time
    if logger:
        logger.info(f"[TIME] {task_name}: {duration:.2f} segundos")
    return duration

@contextmanager
def log_execution_time(task_name="Tarea", logger=None):
    start = time.time()
    yield
    end = time.time()
    duration = end - start
    if logger:
        logger.info(f"[TIME] {task_name}: {duration:.2f} segundos")
    else:
        print(f"[TIME] {task_name}: {duration:.2f} segundos")
