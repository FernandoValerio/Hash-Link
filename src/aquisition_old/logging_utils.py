import logging

def get_logger(name:str='hashlink'):
    logging.basicConfig(level=logging.INFO)
    return logging.getLogger(name)
