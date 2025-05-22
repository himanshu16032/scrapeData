import os
import logging
from datetime import datetime, timedelta, timezone

# Relative path for logs folder and file
LOG_DIR = "logs"
LOG_FILE = "app.log"
LOG_PATH = os.path.join(LOG_DIR, LOG_FILE)

# Ensure the log directory exists
os.makedirs(LOG_DIR, exist_ok=True)

# Set up IST timezone
IST = timezone(timedelta(hours=5, minutes=30))

class ISTFormatter(logging.Formatter):
    def formatTime(self, record, datefmt=None):
        dt = datetime.fromtimestamp(record.created, IST)
        if datefmt:
            return dt.strftime(datefmt)
        return dt.isoformat()

# Set up logger
logger = logging.getLogger("AppLogger")
logger.setLevel(logging.DEBUG)

# Formatter with IST time
formatter = ISTFormatter('%(asctime)s | %(levelname)s | %(message)s', datefmt="%Y-%m-%d %H:%M:%S IST")

# File Handler
file_handler = logging.FileHandler(LOG_PATH, mode='a', encoding='utf-8')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

# Console Handler (optional)
console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)

# Logging functions
def log_debug(message: str):
    logger.debug(message)

def log_info(message: str):
    logger.info(message)

def log_warning(message: str):
    logger.warning(message)

def log_error(message: str):
    logger.error(message)

def log_critical(message: str):
    logger.critical(message)

