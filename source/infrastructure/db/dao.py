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
    cloud database cluster for persistence.

    """

    def __init__(self):
        """
        Constructor / Instantiate the class. Should only create one connection to
        the MongoDB cloud database cluster.

        """
        logger.info("trying to create '{}'".format(self.__class__.__name__))
        try:
            self._id = str(uuid4())
            self._client = MongoClient(db_string)
            self._db = None
            self._collection = None
        except Exception as exp:
            logger.exception(exp)
            raise exp
        logger.success(
            "created '{}', with id: [{}]".format(self.__class__.__name__, self.id))

    @property
    def id(self):
        """
        id setter for dao

        Returns
        -------
        out     : str
                  id of dao given as uuid4 string

        """
        return self._id

    def create_db(self, name: str):
        """
        method for creating db

        Parameters
        ----------
        name        : str
                      name of database

        """
        logger.info("trying to {}".format(self.create_db.__name__))
        try:
            Assertor.assert_data_type({name: str})
            self._db = self._client[name]
        except Exception as exp:
            logger.exception(exp)
            raise exp
        logger.info("'{}' successfully completed".format(self.create_db.__name__))

    def create_collection(self, db_name: str, col_name: str):
        """
        method for creating db collection

        Parameters
        ----------
        db_name     : str
                      name of database to create collection in
        col_name    : str
                      collection name

        """
        logger.info("trying to {}".format(self.create_collection.__name__))
        try:
            Assertor.assert_data_type({db_name: str, col_name: str})
            if not self._db:
                self.create_db(db_name)
                self._collection = self._db[col_name]
            else:
                self._collection = self._db[col_name]
        except Exception as exp:
            logger.exception(exp)
            raise exp
        logger.info("'{}' successfully completed".format(self.create_collection.__name__))

    def insert(self, db_name: str, col_name: str, document: dict):
        """
        method for inserting posts / documents (dict) into collection in database

        Parameters
        ----------
        db_name     : str
                      db to insert record
        col_name    : str
                      collection to insert record
        document      : dict
                      record to insert

        """
        logger.info("trying to {}".format(self.insert.__name__))
        try:
            Assertor.assert_data_type({db_name: str, col_name: str})
            if not isinstance(document, dict):
                raise TypeError("expected type '{}', got '{}' "
                                "instead".format(dict.__name__, type(document).__name__))
            if not self._collection:
                self.create_collection(db_name, col_name)
                self._collection.insert(document)
            else:
                self._collection.insert(document)
        except Exception as exp:
            logger.exception(exp)
            raise exp
        logger.info("'{}' successfully completed".format(self.insert.__name__))
