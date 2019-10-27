# -*- coding: utf-8 -*-

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

from source.infrastructure import Dao
from uuid import UUID


class TestDao:

    @classmethod
    def setup(cls):
        """
        Executed before all tests

        """
        cls.dao = Dao()

    def test_dao_has_uuid4_id(self):
        """
        Test that dao ids are uuid4 compatible

        """
        assert UUID(str(self.dao.id))

    def test_active_mongo_client(self):
        """
        Test that dao always has active MongoClient

        """
        assert self.dao._client.test
