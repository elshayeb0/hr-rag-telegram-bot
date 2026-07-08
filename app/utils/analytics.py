from time import perf_counter
from typing import Any

from app.utils.logging import get_logger


logger = get_logger("rag.analytics")


class RequestTimer:
    def __enter__(self):
        self.start = perf_counter()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.latency_ms = round((perf_counter() - self.start) * 1000, 2)


def log_request_event(event: str, payload: dict[str, Any]) -> None:
    logger.info("%s | %s", event, payload)
