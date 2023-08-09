
import logging

from pymongo import MongoClient
from typing import Union
from pymongo.results import InsertOneResult, InsertManyResult
from pymongo.collection import Collection

logger = logging.getLogger(__name__)


class CollectionNotFoundError(Exception):  # Move this class to its own module
    pass


class RljdDBHandler:  # Improve this class by creating new class to handle CRUD operations and use Composition

    def __init__(self, dbsettings: dict, collection_name: str) -> None:
        self.dbsettings = dbsettings
        self.client = MongoClient(
            host=dbsettings['host'],
            port=dbsettings['port'],
        )
        self.db = self.client[dbsettings['database']]
        logger.info(f"Using DATABASE: {self.db}")

        self.collection_list = tuple(self.db.list_collection_names())
        self.current_collection: Collection = self.set_collection(collection_name)

    def set_collection(self, collection_name) -> Collection:
        if collection_name in self.collection_list:
            return self.db[collection_name]

        else:
            raise CollectionNotFoundError(
                f'collection "{collection_name}" does not exist in database {self.collection_list}'
            )

    def get_current_collection(self) -> Collection:
        return self.current_collection

    def ping(self):     # Complete this
        return self.client.server_info()["ok"]

    def list_dbs(self) -> tuple:
        return tuple(self.client.list_database_names())

    def insert(self, document: list[dict] | dict) -> Union[InsertOneResult, InsertManyResult]:
        # Create

        if isinstance(document, dict):
            logger.info(f"Document successfully was inserted in {self.current_collection}")
            return self.current_collection.insert_one(document)

        elif isinstance(document, list):
            logger.info(f"Documents successfully were inserted in {self.current_collection}")
            return self.current_collection.insert_many(document)

        else:
            raise TypeError(f"'{document}' is neither of type dict nor list of dict")

    def update(self) -> None:
        pass

    def delete(self) -> None:
        pass

    def query(self, querystring):
        pass

