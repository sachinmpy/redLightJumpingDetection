import logging

logging.basicConfig(level=logging.DEBUG, format=" %(levelname)-8s - %(name)s - %(message)s", )
logger = logging.getLogger(__name__)

if __name__ == '__main__':
    logger.info("Starting..")

