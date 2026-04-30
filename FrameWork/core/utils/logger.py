import logging
import os
from datetime import datetime

class MyLogger:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)

            logger = logging.getLogger("MyLogger")
            logger.setLevel(logging.INFO)

            if not logger.handlers:
                console_handler = logging.StreamHandler()

                os.makedirs("logs", exist_ok=True)
                timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
                file_handler = logging.FileHandler(f"logs/test_{timestamp}.log")

                formatter = logging.Formatter(
                    "%(asctime)s | %(levelname)s | %(message)s"
                )

                console_handler.setFormatter(formatter)
                file_handler.setFormatter(formatter)

                logger.addHandler(console_handler)
                logger.addHandler(file_handler)

            cls._instance.logger = logger

        return cls._instance

    def get_logger(self):
        return self.logger