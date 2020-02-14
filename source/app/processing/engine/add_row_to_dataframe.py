# -*- coding: utf-8 -*-
"""
Module containing operation for adding a row to a dataframe

"""

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

from pandas import DataFrame

from source.util import Assertor

from .operation import Operation


class AddRowToDataFrame(Operation):
    """
    Implementation of Module for Adding a row to a Pandas DataFrame

    """

    def __init__(self, row: dict, dataframe: dict, desc: str):
        """
        Constructor / Instantiating class

        Parameters
        ----------
        row         : dict
                      row to be added as dictionary
        dataframe   : dict
                      dataframe as a dictionary to add the row
        desc        : str
                      description of operation

        """
        Assertor.assert_data_types([row, dataframe, desc], [dict, (dict, type(None)), str])
        self.name = self.__class__.__name__
        super().__init__(name=self.name, desc="id: {}".format(desc))
        self.row = row
        self.dataframe = dataframe

    def run(self):
        """
        method for running the operation

        """
        if self.dataframe:
            data_frame = list(self.dataframe.values())[0].copy()
            first_row = data_frame.copy().values[0]
            first_row[0] = list(self.row.keys())[0].capitalize()
            first_row[1], first_row[2] = "-", "-"
            first_row[-1] = list(self.row.values())[0]
            price_data_frame = DataFrame([first_row], columns=data_frame.columns.values)
            final_data_frame = price_data_frame.append(data_frame)
            return final_data_frame.reset_index(drop=True).to_dict()
        first_row = [list(self.row.keys())[0].capitalize(), "-", "-",
                     list(self.row.values())[0]]
        return DataFrame([first_row],
                         columns=["Tinglyst", "Boligtype", "Bolig identifikasjon",
                                  "Pris"]).to_dict()
