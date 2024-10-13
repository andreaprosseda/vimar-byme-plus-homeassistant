import logging

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

handler = logging.StreamHandler()
handler.setLevel(logging.INFO)
handler.setFormatter(formatter)

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(handler)

def log_info(__name__: str, message: str):
    logger.name = __name__
    logger.info(message)
    
def log_debug(__name__: str, message: str):
    logger.name = __name__
    logger.debug(message)