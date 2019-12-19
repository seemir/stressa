# -*- coding: utf-8 -*-

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

from source.domain import Money

from .model import Model


class MortgageModel(Model):
    _lanetype = ["", "Sammenligning", "Annuitetslån", "Serielån"]
    _laneperiode = [""] + [str(yr) + " år" for yr in range(1, 31)]
    _intervall = ["", "Ukentlig", "Annenhver uke", "Månedlig", "Annenhver måned",
                  "Kvartalsvis", "Årlig"]

    def __init__(self, parent):
        super(MortgageModel, self).__init__(parent)
        self.parent.ui.combo_box_lanetype.addItems(self._lanetype)
        self.parent.ui.combo_box_laneperiode.addItems(self._laneperiode)
        self.parent.ui.combo_box_intervall.addItems(self._intervall)

    def mortgage_info(self):
        self.parent.ui.combo_box_lanetype.activated.connect(
            lambda: self.set_combo_box("lanetype"))
        self.parent.ui.combo_box_laneperiode.activated.connect(
            lambda: self.set_combo_box("laneperiode"))
        self.parent.ui.combo_box_intervall.activated.connect(
            lambda: self.set_combo_box("intervall"))
        self.parent.ui.line_edit_egenkapital.editingFinished.connect(
            lambda: self.set_line_edit("egenkapital", Money, "value"))
        self.parent.ui.date_edit_startdato.editingFinished.connect(
            lambda: self.set_date_edit("startdato"))
