# -*- coding: utf-8 -*-

"""
Dao implementation

"""

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

from uuid import uuid4

from source.util import Assertor, LOGGER

# from .settings import DB_STRING

DB_STRING = ""


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
            LOGGER.info(f"trying to create '{self.__class__.__name__}'")
            self._id_str = str(uuid4())
            self._client = {"foo": "bar"}
            self._db = None
            self._collection = None
            LOGGER.success(f"created '{self.__class__.__name__}', with id: [{self.id_str}]")
        except Exception as dao_exception:
            LOGGER.exception(dao_exception)
            raise dao_exception

    @property
    def id_str(self):
        """
        id getter for dao

        Returns
        -------
        out     : str
                  id of dao given as uuid4 string

        """
        return self._id_str

    def get_all_db(self):
        """
        returns a list all active database names in dao

        Returns
        -------
        out     : list
                  all active db names

        """
        return self._client.list_database_names()  # pylint: disable=no-member

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
            LOGGER.info(
                f"trying to '{self.create.__name__}' document(s) in collection: '{col_name}' "
                f"in db: '{db_name}'")
            Assertor.assert_data_types([db_name, col_name, document], [str, str, (dict, list)])

            if not isinstance(document, (dict, list)):
                raise TypeError(
                    f"expected type '{(dict.__name__, list.__name__)}', "
                    f"got '{type(document).__name__}' instead")

            count = len(document) if isinstance(document, list) else len([document])

            if not self._db:
                self._db = self._client[db_name.lower()]
                self._collection = self._db[col_name.lower()]
            else:
                self._collection = self._db[col_name.lower()]

            self._collection.insert(document)
            LOGGER.success(
                f"'{self.create.__name__}' successfully completed - '{count}' document(s)")
        except Exception as exp:
            LOGGER.exception(exp)
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
            LOGGER.info(
                f"trying to '{self.read.__name__}' all documents in collection: '{col_name}' "
                f"from db: '{db_name}'")
            Assertor.assert_data_types([db_name, col_name], [str, str])

            documents = []
            for document in getattr(self._client[db_name.lower()], col_name.lower()).find():
                documents.append(document)

            LOGGER.success(f"'{self.read.__name__}' successfully completed - '{len(documents)}' "
                           f"document(s) found")
            return documents
        except Exception as exp:
            LOGGER.exception(exp)
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
            LOGGER.info(f"trying to '{self.update.__name__}' document '{query}' with value "
                        f"'{new_value}'")
            Assertor.assert_data_types([db_name, col_name], [str, str])

            collection = getattr(self._client, db_name.lower())[col_name.lower()]
            collection.update_many(query, new_value)

            LOGGER.success(f"'{self.update.__name__}' successfully completed")
        except Exception as exp:
            LOGGER.exception(exp)
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
            LOGGER.info(f"trying to '{self.delete.__name__}' all documents from collection: "
                        f"'{col_name}' in db: '{db_name}'")
            Assertor.assert_data_types([db_name, col_name], [str, str])

            collection = getattr(self._client, db_name)[col_name]
            count = collection.count()
            collection.drop()

            LOGGER.success(f"'{self.delete.__name__}' successfully completed - '{count}' "
                           f"document(s) deleted")
        except Exception as exp:
            LOGGER.exception(exp)
            raise exp
