# -*- coding: utf-8 -*-
"""
Module containing operation for adding a row to a dataframe

"""

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

from typing import Union

import pandas as pd
from pandas import DataFrame

from source.util import Assertor, Tracking

from .operation import Operation


class AddRowToDataFrame(Operation):
    """
    Implementation of Module for Adding a row to a Pandas DataFrame

    """

    @Tracking
    def __init__(self, row: Union[dict, None], dataframe: Union[dict, None],
                 desc: str):
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
        self.name = self.__class__.__name__
        Assertor.assert_data_types([row, dataframe, desc],
                                   [(dict, type(None)), (dict, type(None)),
                                    str])
        super().__init__(name=self.name, desc="id: {}".format(desc))
        self.row = row if row else None
        self.dataframe = dataframe if dataframe else None

    @Tracking
    def run(self):
        """
        method for running the operation

        """
        data_frame = self.dataframe
        if self.dataframe and self.row:
            if len(self.row) > 1:
                data_frame = DataFrame.from_dict(self.dataframe)
                first_row = list(self.row.keys())
                first_row[0] = "Salgspris ({})".format(
                    list(self.row.values())[0])
                first_row[1], first_row[2] = "-", "-"
                first_row[-1] = list(self.row.values())[-1]
                sales_price = DataFrame([first_row],
                                        columns=data_frame.columns.values)
                final_data_frame = pd.concat([sales_price, data_frame])
                data_frame = final_data_frame.reset_index(drop=True).to_dict()
            else:
                data_frame = DataFrame.from_dict(
                    list(self.dataframe.values())[0])
                first_row = data_frame.copy().values[0]
                first_row[0] = list(self.row.keys())[0].capitalize()
                first_row[1], first_row[2] = "-", "-"
                first_row[-1] = list(self.row.values())[0]
                price_data_frame = DataFrame([first_row],
                                             columns=data_frame.columns.values)
                final_data_frame = pd.concat([price_data_frame, data_frame])
                data_frame = final_data_frame.reset_index(drop=True).to_dict()
        elif not self.dataframe and self.row:
            first_row = [list(self.row.keys())[0].capitalize(), "-", "-",
                         list(self.row.values())[0]]
            data_frame = DataFrame([first_row],
                                   columns=["Tinglyst", "Boligtype",
                                            "Bolig identifikasjon",
                                            "Pris"]).to_dict()
        return data_frame
