
import logging

from pymongo import MongoClient
from typing import Union
from pymongo.results import InsertOneResult, InsertManyResult

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
        self.client = MongoClient(
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

    def insert(self, document: list[dict] | dict, collection: str) -> Union[InsertOneResult, InsertManyResult]:
        # Create

        if collection not in self.collection_list:
            raise CollectionNotFoundError(
                f'collection "{collection}" does not exist in database {self.collection_list}'
                )

        if isinstance(document, dict):
            collection = self.db[collection]
            logger.info(f"Document successfully was inserted in {collection}")
            return collection.insert_one(document)

        elif isinstance(document, list):
            collection = self.db[collection]
            logger.info(f"Documents successfully were inserted in {collection}")
            return collection.insert_many(document)

        else:
            raise TypeError(f"'{document}' is neither of type dict nor list of dict")

    def update(self) -> None:
        pass

    def delete(self) -> None:

        pass


if __name__ == "__main__":
    pass
