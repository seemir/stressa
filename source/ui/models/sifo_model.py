# -*- coding: utf-8 -*-

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

from source.domain import Money
from .model import Model


class SifoModel(Model):
    _kjonn = ["", "Mann", "Kvinne"]
    _alder = ["", "0-5 mnd", "6-11 mnd", "1", "2", "3", "4-5",
              "6-9", "10-13", "14-17", "18-19", "20-50", "51-60",
              "61-66", "eldre enn 66"]
    _antall_biler = ["", "1", "2", "3", "4"]
    _sifo_expenses = ['mat', 'klar', 'helse', 'fritid', 'kollektivt', 'spedbarn', 'sumindivid',
                      'dagligvarer', 'husholdsart', 'mobler', 'medier', 'biler', 'barnehage',
                      'sfo', 'sumhusholdning', 'totalt']

    def __init__(self, parent):
        super(SifoModel, self).__init__(parent)
        for num in range(1, 8):
            getattr(self.parent.ui, "combo_box_kjonn_" + str(num)).addItems(
                self._kjonn)
            getattr(self.parent.ui, "combo_box_alder_" + str(num)).addItems(
                self._alder)
        self.parent.ui.combo_box_antall_biler.addItems(self._antall_biler)

    def sifo_info(self):
        self.set_age()
        self.set_gender()
        self.set_cars()
        self.parent.ui.line_edit_brutto_arsinntekt.editingFinished.connect(
            lambda: self.set_line_edit("brutto_arsinntekt", Money, "value"))
        self.parent.ui.push_button_tom_skjema_1.clicked.connect(self.clear_content)
        self.parent.ui.push_button_cancel_1.clicked.connect(self.cancel)

        self.parent.ui.push_button_tom_skjema_2.clicked.connect(self.clear_content)
        self.parent.ui.push_button_cancel_2.clicked.connect(self.cancel)
        self.parent.ui.push_button_back.clicked.connect(self.back)

    def set_age(self):
        self.parent.ui.combo_box_alder_1.activated.connect(
            lambda: self.set_combo_box("alder_1", "person_1"))
        self.parent.ui.combo_box_alder_2.activated.connect(
            lambda: self.set_combo_box("alder_2", "person_2"))
        self.parent.ui.combo_box_alder_3.activated.connect(
            lambda: self.set_combo_box("alder_3", "person_3"))
        self.parent.ui.combo_box_alder_4.activated.connect(
            lambda: self.set_combo_box("alder_4", "person_4"))
        self.parent.ui.combo_box_alder_5.activated.connect(
            lambda: self.set_combo_box("alder_5", "person_5"))
        self.parent.ui.combo_box_alder_6.activated.connect(
            lambda: self.set_combo_box("alder_6", "person_6"))
        self.parent.ui.combo_box_alder_7.activated.connect(
            lambda: self.set_combo_box("alder_7", "person_7"))

    def set_gender(self):
        self.parent.ui.combo_box_kjonn_1.activated.connect(
            lambda: self.set_combo_box("kjonn_1", "person_1"))
        self.parent.ui.combo_box_kjonn_2.activated.connect(
            lambda: self.set_combo_box("kjonn_2", "person_2"))
        self.parent.ui.combo_box_kjonn_3.activated.connect(
            lambda: self.set_combo_box("kjonn_3", "person_3"))
        self.parent.ui.combo_box_kjonn_4.activated.connect(
            lambda: self.set_combo_box("kjonn_4", "person_4"))
        self.parent.ui.combo_box_kjonn_5.activated.connect(
            lambda: self.set_combo_box("kjonn_5", "person_5"))
        self.parent.ui.combo_box_kjonn_6.activated.connect(
            lambda: self.set_combo_box("kjonn_6", "person_6"))
        self.parent.ui.combo_box_kjonn_7.activated.connect(
            lambda: self.set_combo_box("kjonn_7", "person_7"))

    def set_cars(self):
        self.parent.ui.combo_box_antall_biler.activated.connect(
            lambda: self.set_combo_box("antall_biler"))

    def show(self):
        self.sifo_info()
        self.parent.ui.show()

    def clear_content(self):
        self.parent.ui.tabwidget_sifo.setCurrentIndex(0)
        self.parent.ui.combo_box_kjonn_1.setFocus()
        for combo_box in range(1, 8):
            getattr(self.parent.ui, "combo_box_kjonn_" + str(combo_box)).setCurrentIndex(0)
            getattr(self.parent.ui, "combo_box_alder_" + str(combo_box)).setCurrentIndex(0)
        self.parent.ui.line_edit_brutto_arsinntekt.clear()
        self.parent.ui.combo_box_antall_biler.setCurrentIndex(0)
        self.data = {}

    def back(self):
        self.parent.ui.tabwidget_sifo.setCurrentIndex(0)

    def cancel(self):
        self.parent.close()
