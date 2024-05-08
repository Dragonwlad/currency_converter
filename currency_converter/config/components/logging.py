import logging
from logging.handlers import RotatingFileHandler

file_handler = RotatingFileHandler('my_logger.log', maxBytes=50000000, backupCount=5, encoding='utf-8')

console_handler = logging.StreamHandler()

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s, %(levelname)s, %(message)s, %(name)s',
    handlers=[file_handler, console_handler]
)
