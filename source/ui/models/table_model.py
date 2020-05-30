# -*- coding: utf-8 -*-
"""
TableModel used for presenting table information in GUI

"""

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

from PyQt5.QtCore import QAbstractTableModel, Qt

from pandas import DataFrame

from source.util import Assertor


class TableModel(QAbstractTableModel):
    """
    Implementation of the TableModel used for presenting tabular information in GUI

    """

    def __init__(self, data: DataFrame):
        """
        Constructor / Instantiating the class

        Parameters
        ----------
        data        : DataFrame
                      data to be displayed in table

        """
        Assertor.assert_data_types([data], [DataFrame])
        QAbstractTableModel.__init__(self)
        self._data = data

    def rowCount(self, parent=None):
        """
        method for counting rows

        Returns
        -------
        out         : int
                      rowCount

        """
        return self._data.shape[0]

    def columnCount(self, parent=None):
        """
        method for counting columns

        Returns
        -------
        out         : int
                      columnCount

        """
        return self._data.shape[1]

    def data(self, index, role=Qt.DisplayRole):
        """
        data getter

        """
        if index.isValid():
            if role == Qt.DisplayRole:
                return str(self._data.iloc[index.row(), index.column()])
        return None

    def headerData(self, col, orientation, role):
        """
        headerData getter

        """
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self._data.columns[col]
        return None
