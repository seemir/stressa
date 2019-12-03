# -*- coding: utf-8 -*-

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

from abc import ABC, abstractmethod

from PyQt5.QtCore import pyqtSlot


class Model(ABC):

    @abstractmethod
    def __init__(self, parent, error):
        super().__init__()
        self._data = {}
        self._parent = parent
        self._error = error

    @property
    def data(self):
        return self._data

    @pyqtSlot()
    def set_content(self, line_edit_name, model, method):
        try:
            line_edit_text = getattr(self._parent.ui, "line_edit_" + line_edit_name).text()
            if line_edit_text and line_edit_text != self.data[line_edit_name]:
                output = getattr(model(line_edit_text), method)()
                self.data.update({line_edit_name: output})
                getattr(self._parent.ui, "line_edit_" + line_edit_name).setText(output)
        except Exception as content_error:
            error = self._error(self._parent, content_error)
            getattr(self._parent.ui, "line_edit_" + line_edit_name).clear()
            error.exec_()

    @pyqtSlot()
    def update_line_edits(self, line_edit_name, line_edits, model, method, index=None):
        postfix = "_" + str(index) if index else ""
        line_edit_text = getattr(self._parent.ui, "line_edit_" + line_edit_name + postfix).text()
        try:
            if line_edit_text and line_edit_text != self.data[line_edit_name]:
                model_info = getattr(model(line_edit_text), method)()
                for line_edit in line_edits:
                    info = model_info[line_edit] if line_edit in model_info.keys() else ""
                    getattr(self._parent.ui, "line_edit_" + line_edit + postfix).setText(info)
                    self.data.update({line_edit: info})
            elif line_edit_text and line_edit_text == self.data[line_edit_name]:
                for line_edit in line_edits:
                    getattr(self._parent.ui, "line_edit_" + line_edit + postfix).setText(
                        self.data[line_edit])
            else:
                self.clear_line_edits(line_edits, index)
        except Exception as update_error:
            error = self._error(self._parent, update_error)
            self.clear_line_edits(line_edits, index)
            error.exec_()

    @pyqtSlot()
    def clear_line_edits(self, line_edits, index=None):
        postfix = "_" + str(index) if index else ""
        for line_edit in line_edits:
            getattr(self._parent.ui, "line_edit_" + line_edit + postfix).clear()
