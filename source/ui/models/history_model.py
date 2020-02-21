# -*- coding: utf-8 -*-

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

from pandas import DataFrame

import pyqtgraph as pg
from pyqtgraph import BarGraphItem
from pyqtgraph.exporters import ImageExporter

from PyQt5.QtCore import QObject, pyqtSlot
from source.util import Assertor

from .table_model import TableModel
from .model import Model

pg.setConfigOption('background', 'w')


class HistoryModel(Model):
    _finn_history_keys = ["finn_adresse", "eieform", "kommunenr", "gardsnr", "bruksnr",
                          "bruksenhetsnr", "seksjonsnr", "historikk"]

    def __init__(self, parent: QObject):
        """
        Constructor / Instantiation of class

        Parameters
        ----------
        parent      : QObject
                      Parent view for which the model in to be linked

        """
        Assertor.assert_data_types([parent], [QObject])
        super().__init__(parent)
        self.legend = None

    @pyqtSlot()
    def add_finn_history(self, postfix: str):
        """
        method for adding Finn ownership history to front end

        Parameters
        ----------
        postfix     : str
                      index if used in naming of line_edits

        """
        Assertor.assert_data_types([postfix], [str])
        grandparent = self.parent.parent
        history_data = {}
        if grandparent.finn_model.finn_data:
            for key, val in grandparent.finn_model.finn_data.items():
                if key[:-len(postfix)] in self._finn_history_keys:
                    if key[:-len(postfix)] == "historikk":
                        history_data.update(
                            {key: val.to_dict() if isinstance(val, DataFrame) else {}})
                    else:
                        history_data.update({key: val})
        self.data.update(history_data)
        for key in self._finn_history_keys:
            if key == "historikk":
                self.clear_graphics()
                if key + postfix in self.data.keys():
                    # table
                    history_data_model = TableModel(DataFrame(self.data[key + postfix]))
                    self.parent.ui.table_view_historikk.setModel(history_data_model)

                    # bar chart
                    history = self.data["historikk" + postfix]["Pris"]
                    keys = [int(key) + 1.5 for key in list(history.keys())]
                    values = [int(val.replace("kr", "").replace(" ", "").replace("\xa0", "")) for
                              val in history.values()][::-1]
                    history_item = BarGraphItem(x=keys, height=values, width=0.66, brush="#93c0e7")
                    if not self.legend and "finnkode" + postfix in \
                            grandparent.finn_model.finn_data.keys():
                        self.legend = pg.LegendItem()
                        finn_code = grandparent.finn_model.finn_data["finnkode" + postfix]
                        bolig_type = grandparent.finn_model.finn_data["boligtype" + postfix]
                        status = grandparent.finn_model.finn_data["status" + postfix]
                        self.legend.setParentItem(self.parent.ui.graphics_view.graphicsItem())
                        self.legend.addItem(history_item, "FINN kode: " + finn_code)
                        self.legend.addItem(history_item, "Boligtype: " + bolig_type)
                        self.legend.addItem(history_item, "Status: " + status)
                    self.parent.ui.graphics_view.addItem(history_item)
            else:
                getattr(self.parent.ui, "line_edit_" + key).clear()
                if key + postfix in self.data.keys():
                    getattr(self.parent.ui, "line_edit_" + key).setText(self.data[key + postfix])

        self.parent.ui.graphics_view.setMouseEnabled(x=False, y=False)
        self.parent.ui.graphics_view.showGrid(x=True, y=True)
        self.parent.ui.graphics_view.getAxis('left').setStyle(showValues=False)
        self.parent.ui.graphics_view.getAxis('bottom').setStyle(showValues=False)
        exporter = ImageExporter(self.parent.ui.graphics_view.plotItem)
        exporter.params.param('width').setValue(1920, blockSignal=exporter.widthChanged)
        exporter.params.param('height').setValue(1080, blockSignal=exporter.heightChanged)

    @pyqtSlot()
    def clear_finn_history(self, postfix: str):
        """
        method for clearing finn ownership history from line_edit

        Parameters
        ----------
        postfix     : str
                      index if used in naming of line_edits

        """
        Assertor.assert_data_types([postfix], [str])
        grandparent = self.parent.parent.finn_model
        for key in self._finn_history_keys:
            full_key = key + postfix
            if key == "historikk":
                if full_key in self.data.keys():
                    self.data.pop(full_key)
                if full_key in grandparent.data.keys():
                    grandparent.data.pop(full_key)
                if full_key in grandparent.finn_data.keys():
                    grandparent.finn_data.pop(full_key)
                self.clear_graphics()
            else:
                if full_key in self.data.keys():
                    self.data.pop(full_key)
                if full_key in grandparent.data.keys():
                    grandparent.data.pop(full_key)
                if full_key in grandparent.finn_data.keys():
                    grandparent.finn_data.pop(full_key)
                getattr(self.parent.ui, "line_edit_" + key).clear()

    def clear_graphics(self):
        self.parent.ui.table_view_historikk.setModel(None)
        self.parent.ui.graphics_view.clear()
        for item in self.parent.ui.graphics_view.childItems():
            if isinstance(item, pg.LegendItem):
                self.parent.ui.graphics_view.scene().removeItem(item)
        self.legend = None
