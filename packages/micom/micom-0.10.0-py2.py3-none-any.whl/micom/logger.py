"""configures the logger for micom."""

import logging

logger = logging.getLogger("micom")
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
formatter = logging.Formatter(
    "%(asctime)s | %(name)s | %(levelname)s | %(message)s"
)
handler.setFormatter(formatter)
handler.setLevel(logging.WARNING)
logger.addHandler(handler)


def file_logger(filepath):
    """Log micom messages to file."""
    fh = logging.FileHandler(filepath)
    fh.setFormatter(formatter)
    fh.setLevel(logging.INFO)
    logger.addHandler(fh)
