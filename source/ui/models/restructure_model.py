# -*- coding: utf-8 -*-

"""
Module for main restructure model for the HomeView

"""

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

from PyQt5.QtCore import QObject, pyqtSlot

from source.domain import Money, Mortgage
from source.app import RestructureProcess
from source.util import Assertor

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

        self.parent.ui_form.combo_box_lanetype.addItems(self._lanetype)
        self.parent.ui_form.combo_box_laneperiode.addItems(self._laneperiode)
        self.parent.ui_form.combo_box_intervall.addItems(self._intervall)

    @pyqtSlot()
    def restructure_info(self):
        """
        Method for retrieving and formatting all inputted restructured information

        """
        self.parent.ui_form.combo_box_lanetype.activated.connect(
            lambda: self.set_combo_box("lanetype"))
        self.parent.ui_form.combo_box_intervall.activated.connect(
            lambda: self.set_combo_box("intervall"))
        self.parent.ui_form.combo_box_laneperiode.activated.connect(
            lambda: self.set_combo_box("laneperiode"))
        self.parent.ui_form.date_edit_startdato.editingFinished.connect(
            lambda: self.set_date_edit("startdato"))
        self.parent.ui_form.line_edit_egenkapital.textEdited.connect(
            lambda: self.set_line_edit("egenkapital", Money, "value"))
        self.parent.ui_form.line_edit_belaning.textEdited.connect(
            lambda: self.set_line_edit("belaning", Money, "value"))

    def export(self):
        """
        method for analyze mortgage

        """
        restructure_data = {}
        restructure_data.update(self.parent.parent.analysis_model.data)
        restructure_data.update(self.data)
        if all(element in restructure_data.keys() for element in Mortgage.requirements_restructure):
            restructure = RestructureProcess(restructure_data)
            analysis_model = self.parent.parent.analysis_model

            analysis_model.set_line_edits(line_edit_text='',
                                          line_edits=analysis_model.analysis_keys,
                                          data=restructure.restructure())
            self.parent.close()

    def clear_all(self):
        """
        method for clearing all line_edits and combo_boxes in model

        """
        self.clear_combo_boxes(["lanetype", "intervall", "laneperiode"])
        self.clear_date_edits(["startdato"])
        self.clear_line_edits(["egenkapital", "belaning"])