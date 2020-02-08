# -*- coding: utf-8 -*-

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

from PyQt5.QtCore import QObject, pyqtSlot

from source.util import Assertor

from .model import Model


class HistoryModel(Model):
    _finn_history_keys = ["finn_adresse", "eieform", "kommunenr", "gardsnr", "bruksnr",
                          "bruksenhetsnr", "seksjonsnr"]

    def __init__(self, parent: QObject):
        """
        Constructor / Instantiation of class

        Parameters
        ----------
        parent      : QObject
                      Parent view for which the model in to be linked

        """
        Assertor.assert_data_types([parent], [QObject])
        super().__init__(parent)

    @pyqtSlot()
    def add_finn_history(self, postfix: str):
        """
        method for adding Finn ownership history to front end

        Parameters
        ----------
        postfix     : str
                      index if used in naming of line_edits

        """
        Assertor.assert_data_types([postfix], [str])
        grandparent = self.parent.parent.finn_model
        history_data = {}
        if grandparent.finn_data:
            for key, val in grandparent.finn_data.items():
                if key[:-len(postfix)] in self._finn_history_keys:
                    history_data.update({key: val})
        self.data.update(history_data)
        for key in self._finn_history_keys:
            getattr(self.parent.ui, "line_edit_" + key).clear()
            if key + postfix in self.data.keys():
                getattr(self.parent.ui, "line_edit_" + key).setText(self.data[key + postfix])

    @pyqtSlot()
    def clear_finn_history(self, postfix: str):
        """
        method for clearing finn ownership history from line_edit

        Parameters
        ----------
        postfix     : str
                      index if used in naming of line_edits

        """
        Assertor.assert_data_types([postfix], [str])
        grandparent = self.parent.parent.finn_model
        for key in self._finn_history_keys:
            full_key = key + postfix
            if full_key in self.data.keys():
                self.data.pop(full_key)
            if full_key in grandparent.data.keys():
                grandparent.data.pop(full_key)
            if full_key in grandparent.finn_data.keys():
                grandparent.finn_data.pop(full_key)
            getattr(self.parent.ui, "line_edit_" + key).clear()
