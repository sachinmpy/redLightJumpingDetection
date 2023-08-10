# Storing all the custom exceptions

import logging
logger = logging.getLogger(__name__)


class CollectionNotFoundError(Exception):  # Move this class to its own module
    pass