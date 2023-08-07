# Database handlers goes here

import logging
import pymongo
import datetime
logger = logging.getLogger(__name__)


class CollectionNotFoundError(Exception):  # Move this class to its own module
    pass


DBSettings: dict = {
    'host': "localhost",
    'port': 27017,
    'database': "red-light-jumping-detection",
    'collectionList': []
}


class RljdDBHandler:  # Improve this class by creating new class to handle CRUD operations and use Composition

    def __init__(self):
        self.client = pymongo.MongoClient(
            host=DBSettings['host'],
            port=DBSettings['port'],
        )
        self.db = self.client[DBSettings['database']]
        logger.info(f"Using DATABASE: {self.db}")

        self.collection_list = tuple(self.db.list_collection_names())

    def ping(self):     # Complete this
        return self.client.server_info()

    def list_dbs(self) -> tuple:
        return tuple(self.client.list_database_names())

    def insert(self, document: list[dict] | dict, collection: str) -> None:  # Create

        if collection not in self.collection_list:
            raise CollectionNotFoundError(f'collection "{collection}" does not exist in database {self.collection_list}')

        if isinstance(document, dict):
            collection = self.db[collection]
            collection.insert_one(document)
            logger.info(f"Document successfully was inserted in {collection}")

        elif isinstance(document, list):
            collection = self.db[collection]
            collection.insert_many(document)
            logger.info(f"Documents successfully were inserted in {collection}")

        else:
            raise TypeError(f"'{document}' is neither of type dict nor list of dict")

    def update(self) -> None:
        pass

    def delete(self) -> None:

        pass


if __name__ == "__main__":
    et = RljdDBHandler()

    cl = [
        {
            'infringement_data': datetime.datetime.now(tz=datetime.timezone.utc),
            'confidence': 100,
            'is_valid': True,
            'vehicle_id': None
        },
        {
            'infringement_data': datetime.datetime.now(tz=datetime.timezone.utc),
            'confidence': 10,
            'is_valid': False,
            'vehicle_id': None
        },

    ]
    et.insert(cl, "infringement")

