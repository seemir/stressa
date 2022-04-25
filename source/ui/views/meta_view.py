# -*- coding: utf-8 -*-

"""
Metadata Dialog which contains information of all relevant metadata

"""

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

import os
import json

from PyQt5.QtWidgets import QDialog, QWidget
from PyQt5.uic import loadUi
from PyQt5.QtCore import Qt

from source.util import Assertor


class MetaView(QDialog):
    """
    MetaView with metadata information, one of several QDialog views

    """

    def __init__(self, parent: QWidget):
        """
        Constructor / Instantiation of class

        Parameters
        ----------
        parent  : QWidget
                  parent view of the metaview

        """
        Assertor.assert_data_types([parent], [QWidget])
        super().__init__(parent)
        self.ui = loadUi(os.path.join(os.path.dirname(__file__), "forms/meta_form.ui"), self)
        self.ui.setWindowFlag(Qt.WindowMinimizeButtonHint, True)
        self.ui.setWindowFlag(Qt.WindowMaximizeButtonHint, True)
        self.ui.setWindowFlag(Qt.WindowContextHelpButtonHint, False)
        self._parent = parent

    @property
    def parent(self):
        """
        parent getter

        Returns
        -------
        out     : QWidget
                  active parent in view

        """
        return self._parent

    def display(self):
        """
        method for showing the MetaView

        """
        try:
            meta_data = self.get_all_meta_data()
            self.ui.plain_text_edit_meta_data.setPlainText(
                json.dumps(meta_data if meta_data else {}, ensure_ascii=False, indent=4))
            self.exec_()
        except Exception as metadata_error:
            self.parent.error.show_error(metadata_error)
            self.parent.error.exec_()

    def get_all_meta_data(self):
        """
        method for getting all the metadata in all models

        Returns
        -------
        out     : dict
                  dictionary with all metadata

        """
        models = {"_mortgage_model": "låne_informasjon", "_budget_model": "budsjett_informasjon",
                  "_sifo_model": "sifo_informasjon", "_finn_model": "finn_informasjon",
                  "_statistics_model": "statistikk_informasjon", "_tax_model": "skatte_informasjon",
                  "_home_model": "likviditets_informasjon"}
        meta_data = {}
        attr = [str(key) for key in list(self.parent.__dict__.keys())]
        for model, name in models.items():
            if model in attr:
                if getattr(self.parent, model).data:
                    meta_data.update({name: getattr(self.parent, model).data})
        return meta_data
