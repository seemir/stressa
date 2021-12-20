# -*- coding: utf-8 -*-

"""
Standard payload for public API query against SSB market interest rates for mortgages

"""

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

import os
import json

from datetime import datetime as dt, timedelta

from source.util import LOGGER, Assertor


class SsbPayload:
    """
    Payload for API-query against SSB table nr. 10748

    """

    @staticmethod
    def date_str(num: int):
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
    def updated_table_date():
        """
        get SSB compatible str that insures that the newest data from table
        nr. 10748 is retrieved

        Returns
        -------
        out         : datetime
                      correct date for table nr. 10748

        """
        return SsbPayload.date_str(90) if dt.today().day < 13 else SsbPayload.date_str(60)

    @staticmethod
    def validate_date(dates: list):
        """
        method for validating the format of a string

        Parameters
        ----------
        dates        : list
                      data str to be validated

        """
        try:
            if dates:
                for date in dates:
                    dt.strptime(date, "%Y{}%m".format('M'))
        except ValueError as date_error:
            raise date_error

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
                                       [(type(None), list) for _ in range(4)])
            Assertor.assert_arguments([utlanstype, sektor, rentebinding],
                                      [{"utlanstype": (["04"], ["70"], ["30"])},
                                       {"sektor": (["04b"], ["04a"])},
                                       {"rentebinding": (
                                           ["06"], ["08"], ["09"], ["10"], ["11"], ["12"],
                                           ["99"])}])
            self.validate_date(tid)

            self._utlanstype = ["70"] if not utlanstype else utlanstype
            self._sektor = ["04b"] if not sektor else sektor
            self._rentebinding = ["08", "12", "10", "11",
                                  "06"] if not rentebinding else rentebinding
            self._tid = self.updated_table_date() if not tid else tid
            LOGGER.success("created {}".format(self.__class__.__name__))
        except Exception as ssb_payload_exception:
            LOGGER.exception(ssb_payload_exception)
            raise ssb_payload_exception

    @property
    def utlanstype(self):
        """
        utlanstype getter

        """
        return self._utlanstype

    @utlanstype.setter
    def utlanstype(self, utlans_type: list):
        """
        utlanstype setter

        Parameters
        ----------
        utlans_type : list
                      type of loan, default ["70"]


        """
        Assertor.assert_data_types([utlans_type], [list])
        Assertor.assert_arguments([utlans_type], [{"utlanstype": (["04"], ["70"], ["30"])}])
        self._utlanstype = utlans_type

    @property
    def sektor(self):
        """
        sektor getter

        """
        return self._sektor

    @sektor.setter
    def sektor(self, sekt: list):
        """
        sektor setter

        """
        Assertor.assert_data_types([sekt], [list])
        Assertor.assert_arguments([sekt], [{"sektor": (["04b"], ["04a"])}])
        self._sektor = sekt

    @property
    def rentebinding(self):
        """
        rentebinding getter

        """
        return self._rentebinding

    @rentebinding.setter
    def rentebinding(self, rente_binding: list):
        """
        rentebinding setter

        Parameters
        ----------
        rente_binding   : list
                          new rentebinding to set

        """
        Assertor.assert_data_types([rente_binding], [list])
        Assertor.assert_arguments([rente_binding], [
            {"rentebinding": (["06"], ["08"], ["09"], ["10"], ["11"], ["12"], ["99"])}])
        self._rentebinding = rente_binding

    @property
    def tid(self):
        """
        tid getter

        """
        return self._tid

    @tid.setter
    def tid(self, tid_: list):
        """
        tid setter

        Parameters
        ----------
        tid_        : list
                      new tid to set in object

        """
        Assertor.assert_data_types([tid_], [list])
        self.validate_date(tid_)
        self._tid = tid_

    def payload(self):
        """
        method for getting the SSB compatible payload

        Returns
        -------
        Out     : dict
                  payload against SSB table nr. 10748

        """
        with open(os.path.dirname(__file__) + '\\payloads\\ssb_payload.json') as json_file:
            json_data = json.load(json_file)

        return json.loads(
            json.dumps(json_data)
                .replace("UtlanstypeVerdi", "".join(self.utlanstype))
                .replace("SektorVerdi", "".join(self.sektor))
                .replace("RentebindingVerdi", '", "'.join(self.rentebinding))
                .replace("".join("TidVerdi"), "".join(self.tid)))
