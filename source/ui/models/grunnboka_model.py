# -*- coding: utf-8 -*-

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

from PyQt5.QtCore import QObject

from source.util import Assertor

from .model import Model


class GrunnbokaModel(Model):
    _grunnboka_keys = ['kommunenr', 'gardsnr', 'bruksnr', 'borettslag-navn', 'borettslag-orgnummer',
                       'borettslag-andelsnummer']

    def __init__(self, parent: QObject):
        super().__init__(parent)

    def add_grunnboka_data(self, postfix: str):
        Assertor.assert_data_types([postfix], [str])

        grandparent = self.parent.parent
        if grandparent.finn_model.finn_data:
            for key, val in grandparent.finn_model.finn_data.items():
                if key == "matrikkel" + postfix:
                    if key not in self.data.keys():
                        self.data.update({key: val})

        if "matrikkel" + postfix in self.data.keys():
            matrikkel = self.data["matrikkel" + postfix]

            for value in self._grunnboka_keys:
                if value in matrikkel.keys():
                    getattr(self.parent.ui, "line_edit_" + value.replace("-", "_")).setText(
                        matrikkel[value])

        if "matrikkel" + postfix not in self.data.keys():
            for element in self._grunnboka_keys:
                getattr(self.parent.ui, "line_edit_" + element.replace("-", "_")).setText("")

    def clear_grunnboka_data(self, postfix):
        full_key = "matrikkel" + postfix
        self.clear_finn_data(full_key)

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
