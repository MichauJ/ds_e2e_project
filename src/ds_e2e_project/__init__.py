import os
import sys
import logging

logging_str = "[%(asctime)s: %(levelname)s: %(module)s: %(message)s]"
log_dir = "logs"
log_filepath = os.path.join(log_dir, "logging.log")
os.makedirs(log_dir,exist_ok=True)

logger = logging.basicConfig(
    level=logging.INFO,
    format=logging_str,
    handlers= [
        logging.FileHandler(log_filepath),  #Writes log messages to a file on disk
        logging.StreamHandler(sys.stdout)  #Prints log messages to the terminal/console
    ]
)

logger = logging.getLogger("ds_e2e_project_logger")