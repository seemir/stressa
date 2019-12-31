# -*- coding: utf-8 -*-

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

from abc import ABC, abstractmethod

from PyQt5.QtCore import pyqtSlot


class Model(ABC):

    @abstractmethod
    def __init__(self, parent):
        super().__init__()
        self._parent = parent
        self._data = {}

    @property
    def parent(self):
        return self._parent

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, new_data):
        self._data = new_data

    @pyqtSlot()
    def set_date_edit(self, date_edit_name):
        try:
            date_edit_text = getattr(self.parent.ui,
                                     "date_edit_" + date_edit_name).date()
            if date_edit_text.year() != 0000:
                self.data.update({date_edit_name: date_edit_text.toString()})
            else:
                self.data.pop(date_edit_name) if date_edit_name in self.data.keys() else ""
        except Exception as set_date_edit_error:
            self.parent.error.show_error(set_date_edit_error)
            self.parent.error.exec_()

    @pyqtSlot()
    def set_combo_box(self, combo_box_name, common_key=None):
        try:
            combo_box_text = str(
                getattr(self.parent.ui, "combo_box_" + combo_box_name).currentText())
            values = {combo_box_name: combo_box_text}

            if common_key and combo_box_text and common_key not in self.data.keys():
                self.data.update({common_key: values})
            elif common_key and combo_box_text and common_key in self.data.keys():
                self.data[common_key].update(values)
            else:
                self.data.pop(common_key) if common_key in self.data.keys() else ""
                if combo_box_text and (combo_box_text not in self.data.values()
                                       or combo_box_name not in self.data.keys()):
                    self.data.update(values)
                else:
                    self.data.pop(combo_box_name) if combo_box_name in self.data.keys() else ""

            for key, val in self.data.items():
                if isinstance(val, dict):
                    self.data.update({key: dict(sorted(val.items()))})
                else:
                    self.data.update({key: val})
        except Exception as set_combo_box_error:
            self.parent.error.show_error(set_combo_box_error)
            self.parent.error.exec_()

    @pyqtSlot()
    def update_line_edits(self, line_edit_name, line_edits, obj, method, index=None):
        postfix = "_" + str(index) if index else ""
        line_edit = getattr(self.parent.ui, "line_edit_" + line_edit_name + postfix)
        try:
            line_edit_text = line_edit.text().strip()
            if line_edit_text and line_edit_text not in self.data.values():
                self.set_line_edits(line_edit_text, line_edits, obj, method, postfix)
            elif line_edit_text and line_edit_text in self.data.values():
                self.get_line_edits(line_edits, postfix)
            else:
                self.clear_line_edits(line_edits, postfix)
        except Exception as update_error:
            self.clear_line_edits(line_edits, postfix)
            self.parent.error.show_error(update_error, self.data)
            self.parent.error.exec_()
            line_edit.setFocus()

    @pyqtSlot()
    def set_line_edits(self, line_edit_text, line_edits, obj=None, method=None, postfix=None,
                       data=None):
        model_info = getattr(obj(line_edit_text), method)() if obj and method else data
        try:
            for line_edit in line_edits:
                if line_edit in model_info.keys():
                    info = model_info[line_edit]
                    line_edit_name = line_edit + postfix if postfix else line_edit
                    self.set_line_edit(line_edit_name, data=info)
        except Exception as set_line_edits_error:
            self.clear_line_edits(line_edits, postfix)
            self.parent.error.show_error(set_line_edits_error, self.data)
            self.parent.error.exec_()

    @pyqtSlot()
    def set_line_edit(self, line_edit_name, obj=None, method=None, data=None):
        line_edit = getattr(self.parent.ui, "line_edit_" + line_edit_name)
        try:
            line_edit_text = line_edit.text() if not data else data
            new_value = line_edit_text not in self.data.values()
            if line_edit_text and new_value:
                output = getattr(obj(line_edit_text), method)() if not data else data
                self.data.update({line_edit_name: output})
            elif line_edit_text and not new_value:
                output = line_edit_text
                self.data.update({line_edit_name: output})
            else:
                output = ""
                self.data.pop(line_edit_name) if line_edit_name in self.data.keys() else ""
            getattr(self.parent.ui, "line_edit_" + line_edit_name).setText(output)
        except Exception as set_line_edit_error:
            self.clear_line_edit(line_edit_name)
            self.parent.error.show_error(set_line_edit_error, self.data)
            self.parent.error.exec_()
            line_edit.setFocus()

    @pyqtSlot()
    def get_line_edits(self, line_edits, postfix=None):
        for line_edit in line_edits:
            line_edit = "line_edit_" + (line_edit + postfix if postfix else line_edit)
            if line_edit in self.data.keys():
                getattr(self.parent.ui, line_edit).setText(
                    self.data[line_edit])

    @pyqtSlot()
    def clear_line_edits(self, line_edits, index=None):
        postfix = str(index) if index else ""
        for line_edit in line_edits:
            line_edit_name = line_edit + postfix if postfix else line_edit
            self.clear_line_edit(line_edit_name)

    @pyqtSlot()
    def clear_line_edit(self, line_edit_name):
        if line_edit_name in self.data.keys():
            getattr(self.parent.ui, "line_edit_" + line_edit_name).clear()
            self.data.pop(line_edit_name)
        else:
            getattr(self.parent.ui, "line_edit_" + line_edit_name).clear()
