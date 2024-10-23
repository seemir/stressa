# -*- coding: utf-8 -*-
"""
Module with model for Grunnboka processing

"""

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

from PyQt5.QtCore import QObject

from source.util import Assertor

from .model import Model


class GrunnbokaModel(Model):
    """
    Implementation of Model for Grunnboka

    """
    _grunnboka_keys = ['kommunenr', 'gardsnr', 'bruksnr', 'seksjonsnr',
                       'borettslag-navn', 'borettslag-orgnummer',
                       'borettslag-andelsnummer']

    def __init__(self, parent: QObject):
        """
        Constructor / Instantiating class

        """
        super().__init__(parent=parent)

    @property
    def grunnboka_keys(self):
        """
        Grunnboka getter

        Returns
        -------
        out         : list
                      active grunnboka keys list

        """
        return self._grunnboka_keys

    def add_grunnboka_data(self, postfix: str):
        """
        method for adding grunnboka data

        """
        Assertor.assert_data_types([postfix], [str])

        grandparent = self.parent.parent
        if grandparent.finn_model.finn_data:
            for key, val in grandparent.finn_model.finn_data.items():
                if key == "matrikkel" + postfix:
                    if key not in self.data.keys():
                        self.data.update({key: val})

        if "matrikkel" + postfix in self.data.keys():
            matrikkel = self.data["matrikkel" + postfix]

            for value in self.grunnboka_keys:
                if value in matrikkel.keys():
                    getattr(self.parent.ui_form,
                            "line_edit_" + value.replace("-", "_")).setText(
                        matrikkel[value])

        if "matrikkel" + postfix not in self.data.keys():
            for element in self.grunnboka_keys:
                getattr(self.parent.ui_form,
                        "line_edit_" + element.replace("-", "_")).setText("")

    def clear_grunnboka_data(self, postfix):
        """
        method for clearing all grunnboka data

        """
        full_key = "matrikkel" + postfix
        self.clear_line_edits(
            [elem.replace("-", "_") for elem in self.grunnboka_keys])
        self.clear_finn_data(full_key)
        self.parent.ui_form.web_view_grunnboka.close()

    def clear_finn_data(self, full_key):
        """
        helper method for clearing inputted Finn data

        """
        grandparent = self.parent.parent.finn_model
        if full_key in self.data.keys():
            self.data.pop(full_key)
        if full_key in grandparent.data.keys():
            grandparent.data.pop(full_key)
        if full_key in grandparent.finn_data.keys():
            grandparent.finn_data.pop(full_key)
