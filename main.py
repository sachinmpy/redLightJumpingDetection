import logging
import settings
import datetime
import RLJDGui as GUI

from databaseHandler import RljdDBHandler

logging.basicConfig(level=logging.DEBUG, format=" [ %(levelname)s ] - %(name)s - %(message)s", )
logger = logging.getLogger(__name__)

if __name__ == '__main__':

    db: RljdDBHandler = RljdDBHandler(settings.DBSettings, 'infringement')
    logger.info("Starting..")
