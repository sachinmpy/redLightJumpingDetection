# Settings variables and enums goes here

import logging
logger = logging.getLogger(__name__)

DBSettings: dict = {
    'host': "localhost",
    'port': 27017,
    'database': "red-light-jumping-detection",
    'collectionList': []
}
