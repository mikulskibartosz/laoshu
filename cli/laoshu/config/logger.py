import logging
from rich.logging import RichHandler


def setup_logger() -> None:
    logging.basicConfig(
        level="INFO", format="%(message)s", datefmt="[%X]", handlers=[RichHandler()]
    )
