# -*- coding: utf-8 -*-

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

import os

from PyQt5.QtWidgets import QDialog, QWidget
from PyQt5.QtCore import pyqtSlot, Qt
from PyQt5.uic import loadUi

from source.util import Assertor

from .meta_view import MetaView
from ..models import BudgetModel


class BudgetView(QDialog):
    """
    Budget dialog window

    """

    def __init__(self, parent: QWidget):
        """
        Constructor / Instantiate the class

        Parameters
        ----------
        parent      : QObject
                      parent class for which this dialog window is part

        """
        Assertor.assert_data_types([parent], [QWidget])
        super().__init__(parent)
        self._parent = parent
        self.ui = loadUi(os.path.join(os.path.dirname(__file__), "forms/budget_form.ui"), self)
        self.ui.setWindowFlag(Qt.WindowMinimizeButtonHint, True)
        self.ui.setWindowFlag(Qt.WindowMaximizeButtonHint, True)

        self._error_view = self.parent.error_view
        self._meta_view = MetaView(self)

        self._budget_model = BudgetModel(self)

        self.ui.push_button_exporter_1.clicked.connect(self.export)
        self.ui.push_button_tom_skjema_1.clicked.connect(self.clear_all)
        self.ui.push_button_budget_meta_data_1.clicked.connect(self.meta_view.display)
        self.ui.push_button_avbryt_1.clicked.connect(self.close)

    @property
    def parent(self):
        """
        parent getter

        Returns
        -------
        out     : QObject
                  active parent view for the SifoView

        """
        return self._parent

    @property
    def error_view(self):
        """
        ErrorView getter

        Returns
        -------
        out     : QObject
                  active ErrorView in the SifoView

        """
        return self._error_view

    @property
    def meta_view(self):
        """
        MetaView getter

        Returns
        -------
        out     : MetaView
                  View with the metadata for the SifoView

        """
        return self._meta_view

    @property
    def budget_model(self):
        return self._budget_model

    @pyqtSlot()
    def budget_info(self):
        self.budget_model.budget_info()

    @pyqtSlot()
    def display(self):
        self.ui.combo_box_interval_1.setFocus()
        self.show()

    @pyqtSlot()
    def export(self):
        self.parent.mortgage_model.set_line_edits("", self.budget_model.budget_posts,
                                                  data=self.budget_model.data)
        for budget_post in self.budget_model.budget_posts:
            if budget_post not in self.budget_model.data.keys():
                self.parent.mortgage_model.clear_line_edit(budget_post)
        self.ui.combo_box_interval_1.setFocus()
        self.close()

    @pyqtSlot()
    def clear_all(self):
        self.parent.mortgage_model.clear_line_edits(self.budget_model.budget_posts)
        for combo_box in range(1, 19):
            getattr(self.ui, "combo_box_interval_" + str(combo_box)).setCurrentIndex(0)
        self.budget_model.clear_line_edits(self.budget_model.budget_posts)
        self.ui.radio_button_skattefrie_inntekt_1.setChecked(False)
        self.ui.combo_box_interval_1.setFocus()
