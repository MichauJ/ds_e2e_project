# src/ds_e2e_project/__init__.py
import os
import sys
import logging

def setup_logging():
    logging_str = "[%(asctime)s: %(levelname)s: %(module)s: %(message)s]"
    log_dir = "logs"
    log_filepath = os.path.join(log_dir, "logging.log")
    os.makedirs(log_dir, exist_ok=True)

    logging.basicConfig(
        level=logging.INFO,
        format=logging_str,
        handlers=[
            logging.FileHandler(log_filepath),
            logging.StreamHandler(sys.stdout)
        ]
    )

setup_logging()
logger = logging.getLogger("ds_e2e_project_logger")