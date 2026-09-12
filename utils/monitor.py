import sys
import functools
import logging
import config
from time import perf_counter

app_logger = logging.getLogger("anddo-app")
app_logger.setLevel(logging.DEBUG if config.DEBUG else logging.INFO)

if not app_logger.handlers:

    if (config.DEBUG):
        formatter = logging.Formatter("\033[92m%(levelname)s\033[0m [\033[94m%(name)s\033[0m] %(message)s")
    else:
        formatter = logging.Formatter("%(levelname)s | %(name)s | %(message)s")

    console_handler = logging.StreamHandler(sys.stdout)    
    console_handler.setFormatter(formatter)    
    app_logger.addHandler(console_handler)
    app_logger.propagate = False

def monitor_telemetry(func):
    
    monitor_logger = logging.getLogger(f"anddo-app.monitor")
    
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = perf_counter()
        try:
            return func(*args, **kwargs)
        except Exception as e:
            # Isso vira uma "Exception" no App Insights
            monitor_logger.error(f"Falha em {func.__name__}: {str(e)}", exc_info=True)
            raise # Repassa para a Function decidir o status HTTP
        finally:
            duration = perf_counter() - start
            # Isso vira um "Trace" com tempo de execução
            monitor_logger.info(f"Performance: {func.__name__} levou {duration:.4f}s")
    return wrapper