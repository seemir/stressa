# -*- coding: utf-8 -*-

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

from source.settings import db_string
from source.util import Assertor
from pymongo import MongoClient
from source.log import logger
from uuid import uuid4


class Dao:
    """
    Data Access Object (DAO) that provides an abstract interface to MongoDB
    cloud database cluster for persistence. The database cluster is hosted
    on Amazon Web Service (AWS).

    """

    def __init__(self):
        """
        Constructor / Instantiate the class. Should only create one connection to
        the MongoDB cloud database cluster.

        """
        try:
            logger.info("trying to create '{}'".format(self.__class__.__name__))
            self._id = str(uuid4())
            self._client = MongoClient(db_string)
            self._db = None
            self._collection = None
            logger.success(
                "created '{}', with id: [{}]".format(self.__class__.__name__, self.id))
        except Exception as exp:
            logger.exception(exp)
            raise exp

    @property
    def id(self):
        """
        id getter for dao

        Returns
        -------
        out     : str
                  id of dao given as uuid4 string

        """
        return self._id

    def get_all_db(self):
        """
        returns a list all active database names in dao

        Returns
        -------
        out     : list
                  all active db names

        """
        return self._client.list_database_names()

    def get_all_collections(self, db_name: str):
        """
        returns a list of all active collections in dao

        Returns
        -------
        out     : list
                  all active collections names

        """
        Assertor.assert_data_types([db_name], [str])
        return self._client[db_name.lower()].list_collection_names()

    def create(self, db_name: str, col_name: str, document: (dict, list)):
        """
        method for creating posts / documents (dict or list) into collection in database

        Parameters
        ----------
        db_name     : str
                      db to insert record
        col_name    : str
                      collection to insert record
        document    : dict, list
                      record(s) to insert

        """
        try:
            logger.info(
                "trying to '{}' document(s) in collection: '{}' in db: '{}'".format(
                    self.create.__name__, col_name, db_name))
            Assertor.assert_data_types([db_name, col_name, document], [str, str, (dict, list)])

            if not isinstance(document, (dict, list)):
                raise TypeError("expected type '{}', got '{}' "
                                "instead".format((dict.__name__, list.__name__),
                                                 type(document).__name__))

            count = len(document) if isinstance(document, list) else len([document])

            if not self._db:
                self._db = self._client[db_name.lower()]
                self._collection = self._db[col_name.lower()]
            else:
                self._collection = self._db[col_name.lower()]

            self._collection.insert(document)
            logger.success("'{}' successfully completed - '{}' document(s)".format(
                self.create.__name__, count))
        except Exception as exp:
            logger.exception(exp)
            raise exp

    def read(self, db_name: str, col_name: str):
        """
        method for reading all documents in a collection

        Parameters
        ----------
        db_name     : str
                      db name to lookup
        col_name    : str
                      collection name to lookup

        Returns
        -------
        out         : list
                      all documents in collection

        """
        try:
            logger.info(
                "trying to '{}' all documents in collection: '{}' from db: '{}'".format(
                    self.read.__name__, col_name, db_name))
            Assertor.assert_data_types([db_name, col_name], [str, str])

            documents = []
            for document in getattr(self._client[db_name.lower()], col_name.lower()).find():
                documents.append(document)

            logger.success("'{}' successfully completed - '{}' document(s) found".format(
                self.read.__name__, len(documents)))
            return documents
        except Exception as exp:
            logger.exception(exp)
            raise exp

    def update(self, db_name: str, col_name: str, query: dict, new_value: dict):
        """
        method for updating document(s) in a collection

        Parameters
        ----------
        db_name     : str
                      db name to look for collection
        col_name    : str
                      collection name to apply update
        query       : dict
                      document to query
        new_value   : dict
                      new values to apply in document

        """
        try:
            logger.info("trying to '{}' document '{}' with value '{}'".format(
                self.update.__name__, query, new_value))
            Assertor.assert_data_types([db_name, col_name], [str, str])

            collection = getattr(self._client, db_name.lower())[col_name.lower()]
            collection.update_many(query, new_value)

            logger.success("'{}' successfully completed".format(self.update.__name__))
        except Exception as exp:
            logger.exception(exp)
            raise exp

    def delete(self, db_name: str, col_name: str):
        """
        Delete all documents in collection. Will also delete the db that the collection is in.

        Parameters
        ----------
        db_name     : str
                      name of db
        col_name    : str
                      name of collection to be deleted

        """
        try:
            logger.info("trying to '{}' all documents from collection: '{}' in db: '{}'".format(
                self.delete.__name__, col_name, db_name))
            Assertor.assert_data_types([db_name, col_name], [str, str])

            collection = getattr(self._client, db_name)[col_name]
            count = collection.count()
            collection.drop()

            logger.success("'{}' successfully completed - '{}' document(s) deleted".format(
                self.delete.__name__, count))
        except Exception as exp:
            logger.exception(exp)
            raise exp
