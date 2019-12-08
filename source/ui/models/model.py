# -*- coding: utf-8 -*-

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

import time

from abc import ABC, abstractmethod

from PyQt5.QtCore import pyqtSlot


class Model(ABC):

    @abstractmethod
    def __init__(self, parent, error):
        super().__init__()
        self._parent = parent
        self._error = error
        self._data = {}

    @property
    def parent(self):
        return self._parent

    @property
    def error(self):
        return self._error

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, new_data):
        self._data = new_data

    @pyqtSlot()
    def set_date_edit(self, date_edit_name):
        date_edit = getattr(self.parent.ui, "date_edit_" + date_edit_name).date()
        if date_edit.year() != 0000:
            self.data.update({date_edit_name: date_edit})
        else:
            self.data.pop(date_edit_name) if date_edit_name in self.data.keys() else ""
        print(self.data)

    @pyqtSlot()
    def set_combo_box(self, combo_box_name):
        combo_box = str(getattr(self.parent.ui, "combo_box_" + combo_box_name).currentText())
        if combo_box and combo_box not in self.data.values():
            self.data.update({combo_box_name: combo_box})
        else:
            self.data.pop(combo_box_name) if combo_box_name in self.data.keys() else ""
        print(self.data)

    @pyqtSlot()
    def set_line_edit(self, line_edit_name, model, method):
        try:
            line_edit_text = getattr(self.parent.ui, "line_edit_" + line_edit_name).text()
            if line_edit_text and line_edit_text not in self.data.values():
                output = getattr(model(line_edit_text), method)()
                self.data.update({line_edit_name: output})
            elif line_edit_text and line_edit_text in self.data.values():
                output = self.data[line_edit_name]
                self.data.update({line_edit_name: output})
            else:
                output = ""
                self.data.pop(line_edit_name) if line_edit_name in self.data.keys() else ""
            getattr(self.parent.ui, "line_edit_" + line_edit_name).setText(output)
            print(self.data)
        except Exception as content_error:
            self.error.show_error(content_error)
            getattr(self.parent.ui, "line_edit_" + line_edit_name).clear()
            self.error.exec_()

    @pyqtSlot()
    def update_line_edits(self, line_edit_name, line_edits, model, method, index=None):
        postfix = "_" + str(index) if index else ""
        line_edit_text = getattr(self.parent.ui, "line_edit_" + line_edit_name).text()
        try:
            if line_edit_text and line_edit_text not in self.data.values():
                self.set_line_edits(line_edit_text, line_edits, model, method, postfix)
            elif line_edit_text and line_edit_text in self.data.values():
                self.get_line_edits(line_edits, postfix)
            else:
                self.clear_line_edits(line_edits, postfix)
            print(self.data)
        except Exception as update_error:
            self.error.show_error(update_error)
            self.clear_line_edits(line_edits, postfix)
            self.error.exec_()

    @pyqtSlot()
    def clear_line_edits(self, line_edits, postfix=None):
        for line_edit in line_edits:
            line_edit = line_edit + postfix if postfix else line_edit
            if line_edit in self.data.keys():
                getattr(self.parent.ui, "line_edit_" + line_edit).clear()
                self._data.pop(line_edit)

    @pyqtSlot()
    def set_line_edits(self, line_edit_text, line_edits, model, method, postfix=None):
        model_info = getattr(model(line_edit_text), method)()
        for line_edit in line_edits:
            if line_edit in model_info.keys():
                info = model_info[line_edit]
                line_edit = line_edit + postfix if postfix else line_edit
                getattr(self.parent.ui, "line_edit_" + line_edit).setText(info)
                self.data.update({line_edit: info})

    @pyqtSlot()
    def get_line_edits(self, line_edits, postfix=None):
        for line_edit in line_edits:
            line_edit = line_edit + postfix if postfix else line_edit
            if line_edit in self.data.keys():
                getattr(self.parent.ui, "line_edit_" + line_edit).setText(
                    self.data[line_edit])
