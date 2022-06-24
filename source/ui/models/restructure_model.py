# -*- coding: utf-8 -*-

"""
Module for main restructure model for the HomeView

"""

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

from PyQt5.QtCore import QObject, pyqtSlot

from source.util import Assertor
from source.domain import Money

from .model import Model


class RestructureModel(Model):
    """
    Implementation of restructure Model in the HomeView, i.e. contains logic / mortgage
    related data inputted in the HomeView

    """
    _lanetype = ["", "Sammenligning", "Annuitetslån", "Serielån"]
    _laneperiode = [""] + [str(yr) + " år" for yr in range(1, 31)]
    _intervall = ["", "Årlig", "Halvårlig", "Kvartalsvis", "Annenhver måned", "Månedlig",
                  "Semi-månedlig", "Annenhver uke", "Ukentlig"]

    def __init__(self, parent: QObject):
        """
        Constructor / Instantiation of class

        Parameters
        ----------
        parent  : QObject
                  parent view for which the model resides

        """
        Assertor.assert_data_types([parent], [QObject])
        super().__init__(parent)

        self.parent.ui.combo_box_lanetype.addItems(self._lanetype)
        self.parent.ui.combo_box_laneperiode.addItems(self._laneperiode)
        self.parent.ui.combo_box_intervall.addItems(self._intervall)

    @pyqtSlot()
    def restructure_info(self):
        """
        Method for retrieving and formatting all inputted restructured information

        """
        self.parent.ui.combo_box_lanetype.activated.connect(
            lambda: self.set_combo_box("lanetype"))
        self.parent.ui.combo_box_intervall.activated.connect(
            lambda: self.set_combo_box("intervall"))
        self.parent.ui.combo_box_laneperiode.activated.connect(
            lambda: self.set_combo_box("laneperiode"))
        self.parent.ui.date_edit_startdato.editingFinished.connect(
            lambda: self.set_date_edit("startdato"))
        self.parent.ui.line_edit_egenkapital.textEdited.connect(
            lambda: self.set_line_edit("egenkapital", Money, "value"))
        self.parent.ui.line_edit_belaning.textEdited.connect(
            lambda: self.set_line_edit("belaning", Money, "value"))

    def clear_all(self):
        """
        method for clearing all line_edits and combo_boxes in model

        """
        self.clear_combo_boxes(["lanetype", "intervall", "laneperiode"])
        self.clear_date_edits(["startdato"])
        self.clear_line_edits(["egenkapital", "belaning"])
