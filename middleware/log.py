from datetime import datetime
import logging.handlers
import os
import logging


def log_setting (__name__ : str, log_dir: str = "logs") -> logging.Logger:
    os.makedirs(log_dir, exist_ok=True)
    log_file = os.path.join(log_dir, f"app_{datetime.now():%Y-%m-%d}.log")      #Tạo file log


    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)

    format = logging.Formatter('[%(asctime)s] [%(levelname)s] [%(name)s] - %(message)s')    #Format của log

    #Tạo biến console, kiểm soát qua terminal để lấy info
    console = logging.StreamHandler()
    console.setLevel(logging.DEBUG)
    console.setFormatter(format)

    #File handler (IDK whast's it for)
    file_handler = logging.handlers.TimedRotatingFileHandler(
        log_file, when='midnight', interval=1, backupCount=7, encoding='utf-8'
    )
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(format)
    file_handler.suffix = "%Y-%m-%d"

    logger.addHandler(console)
    logger.addHandler(file_handler)

    return logger

