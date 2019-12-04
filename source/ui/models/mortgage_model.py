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

    def __init__(self, parent, error):
        super(MortgageModel, self).__init__(parent, error)

    def mortgage_information(self):
        self._parent.ui.combo_box_lanetype.addItems(self._lanetype)
        self._parent.ui.combo_box_lanetype.activated.connect(self.set_lanetype)
        self._parent.ui.combo_box_laneperiode.addItems(self._laneperiode)
        self._parent.ui.combo_box_laneperiode.activated.connect(self.set_laneperiode)
        self._parent.ui.combo_box_intervall.addItems(self._intervall)
        self._parent.ui.combo_box_intervall.activated.connect(self.set_intervall)
        self._parent.ui.line_edit_egenkapital.editingFinished.connect(
            lambda: self.set_line_edit("egenkapital", Money, "value"))

        self._parent.ui.date_edit_startdato.editingFinished.connect(self.set_startdato)

    def set_lanetype(self):
        lanetype = str(self._parent.ui.combo_box_lanetype.currentText())
        if lanetype and lanetype not in self.data.values():
            self.data.update({"lanetype": lanetype})
        else:
            self.data.pop("lanetype") if "lanetype" in self.data.keys() else ""

    def set_laneperiode(self):
        laneperiode = str(self._parent.ui.combo_box_laneperiode.currentText())
        if laneperiode and laneperiode not in self.data.values():
            self.data.update({"laneperiode": laneperiode})
        else:
            self.data.pop("laneperiode") if "laneperiode" in self.data.keys() else ""

    def set_intervall(self):
        intervall = str(self._parent.ui.combo_box_intervall.currentText())
        if intervall and intervall not in self.data.values():
            self.data.update({"intervall": intervall})
        else:
            self.data.pop("intervall") if "intervall" in self.data.keys() else ""

    def set_startdato(self):
        startdato = self._parent.ui.date_edit_startdato.date()
        if startdato.year() != 0000:
            self.data.update({"startdato": startdato})
        else:
            self.data.pop("startdato") if "startdato" in self.data.keys() else ""
