import logging

from logging.handlers import RotatingFileHandler


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s, %(levelname)s, %(message)s, %(name)s',
    handlers=[
        RotatingFileHandler('my_logger.log', maxBytes=50000000, backupCount=5),
        logging.StreamHandler()
    ]
)
