import logging
import os

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('[%(levelname)s] %(asctime)s >> %(message)s')
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)