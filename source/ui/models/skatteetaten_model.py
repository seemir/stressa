# -*- coding: utf-8 -*-
"""
Module with model for Skattetaten processing

"""

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

from PyQt5.QtCore import QObject

from source.util import Assertor

from .model import Model


class SkatteetatenModel(Model):
    """
    Implementation of Model for Skatteetaten processing

    """
    _skatteetaten_keys = ['kommunenr', 'gardsnr', 'bruksnr', 'seksjonsnr', 'borettslag-navn',
                          'borettslag-orgnummer', 'borettslag-andelsnummer']

    def __init__(self, parent: QObject):
        """
        Constructor / Instantiating class

        """
        super().__init__(parent=parent)

    @property
    def skatteetaten_keys(self):
        """
        Skatteetaten getter

        Returns
        -------
        out         : list
                      active skatteetaten keys list

        """
        return self._skatteetaten_keys

    def add_skatteetaten_data(self, postfix: str):
        """
        method for adding skatteetaten data

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

            for value in self.skatteetaten_keys:
                if value in matrikkel.keys():
                    getattr(self.parent.ui_form, "line_edit_" + value.replace("-", "_")).setText(
                        matrikkel[value])

        if "matrikkel" + postfix not in self.data.keys():
            for element in self.skatteetaten_keys:
                getattr(self.parent.ui_form, "line_edit_" + element.replace("-", "_")).setText("")

    def clear_skatteetaten_data(self):
        """
        method for clearing all skatteetaten data

        """
        self.clear_line_edits([elem.replace("-", "_") for elem in self.skatteetaten_keys])
        self.parent.ui_form.web_view_primary.close()
