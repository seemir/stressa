# -*- coding: utf-8 -*-

"""
Standard payload for public API query against SSB market interest rates for mortgages

"""

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

from datetime import datetime as dt, timedelta

from source.util import LOGGER, Assertor


class SsbPayload:
    """
    Payload for API-query against SSB table nr. 10748

    """

    @staticmethod
    def _date_str(num: int):
        """
        date string n days back in time

        Parameters
        ----------
        num       : int
                    number of days back in time

        Returns
        -------
        out     list
                date string n days back in time

        """
        Assertor.assert_data_types([num], [int])
        return [(dt.today() - timedelta(days=num)).strftime("%Y{}%m".format('M'))]

    @staticmethod
    def _updated_table_date():
        """
        get SSB compatible str that insures that the newest data from table
        nr. 10748 is retrieved

        Returns
        -------
        out         : datetime
                      correct date for table nr. 10748

        """
        return SsbPayload._date_str(90) if dt.today().day < 13 else SsbPayload._date_str(60)

    def __init__(self, utlanstype: list = None, sektor: list = None, rentebinding: list = None,
                 tid: list = None):
        """
        Constructor / Instantiate the class

        Parameters
        ----------
        utlanstype      : list
                          type of loan, default ["70"]
        sektor          : list
                          sektor, default is ["04b"]
        rentebinding    : list
                          type of interest rate, default is ["08", "12", "10", "11", "06"]
        tid             : list
                          time frame

        """
        try:
            LOGGER.info("trying to create '{}'".format(self.__class__.__name__))
            Assertor.assert_data_types([utlanstype, sektor, rentebinding, tid],
                                       [(type(None), list) for _ in range(3)])
            self.utlanstype = ["70"] if not utlanstype else utlanstype
            self.sektor = ["04b"] if not sektor else sektor
            self.rentebinding = ["08", "12", "10", "11", "06"] if not rentebinding else rentebinding
            self.tid = self._updated_table_date() if not tid else tid
            LOGGER.success("created {}".format(self.__class__.__name__))
        except Exception as ssb_payload_exception:
            LOGGER.exception(ssb_payload_exception)
            raise ssb_payload_exception

    def payload(self):
        """
        method for getting the SSB compatible payload

        Returns
        -------
        Out     : dict
                  payload against SSB table nr. 10748

        """
        return \
            {
                "query": [
                    {"code": "Utlanstype",
                     "selection": {"filter": "item", "values": self.utlanstype}},
                    {"code": "Sektor", "selection": {"filter": "item", "values": self.sektor}},
                    {"code": "Rentebinding",
                     "selection": {"filter": "item", "values": self.rentebinding}},
                    {"code": "Tid", "selection": {"filter": "item", "values": self.tid}}],
                "response": {"format": "json-stat2"}
            }
