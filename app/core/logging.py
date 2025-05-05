import logging

def setup_logger():
    logging.basicConfig(
        format='%(asctime)s - %(levelname)s: %(message)s',
        level=logging.INFO
    )
    return logging.getLogger(__name__)

logger = setup_logger()
