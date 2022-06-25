# -*- coding: utf-8 -*-

"""
Module for the Model abstract base class

"""

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

from abc import ABC, abstractmethod

from PyQt5.QtCore import pyqtSlot, QObject, QDateTime

from source.util import Assertor


class Model(ABC):
    """
    Implementation of the Model Abstract Base Class

    """

    @abstractmethod
    def __init__(self, parent: QObject):
        """
        Constructor / Instantiation

        Parameters
        ----------
        parent  : QObject
                  parent view for which the model resides

        """
        Assertor.assert_data_types([parent], [QObject])
        super().__init__()
        self._parent = parent
        self._data = {}

    @property
    def parent(self):
        """
        parent getter

        Returns
        -------
        out     : OQbject
                  active parent in model

        """
        return self._parent

    @property
    def data(self):
        """
        data getter

        Returns
        -------
        out     : dict
                  active data that has been inputted in model

        """
        return self._data

    @data.setter
    def data(self, new_data: dict):
        """
        data setter

        Parameters
        ----------
        new_data    : dict
                      new data dict to be set in model

        """
        Assertor.assert_data_types([new_data], [dict])
        self._data = new_data

    @pyqtSlot()
    def set_date_edit(self, date_edit_name: str):
        """
        method for setting value in a date_edit

        Parameters
        ----------
        date_edit_name  : str
                          name of date_edit

        """
        try:
            Assertor.assert_data_types([date_edit_name], [str])
            date_edit_text = getattr(self.parent.ui_form, "date_edit_" + date_edit_name).dateTime()
            self.data.update({date_edit_name: date_edit_text.toString("dd.MM.yyyy")})
        except Exception as set_date_edit_error:
            self.parent.error_view.show_error(set_date_edit_error, self.data)

    @pyqtSlot()
    def clear_date_edits(self, date_edits: list):
        """
        method for clearing content in date_edits

        Parameters
        ----------
        date_edits  : list
                      list of date_edits

        """
        Assertor.assert_data_types([date_edits], [list])
        date = QDateTime.fromString("01.01.2000", "dd.MM.yyyy")
        for date_edit in date_edits:
            getattr(self.parent.ui_form, "date_edit_" + date_edit).setDateTime(date)
            if date_edit in self.data.keys():
                self.data.pop(date_edit)

    @pyqtSlot()
    def set_combo_box(self, combo_box_name: str, common_key: str = None, key_name: str = None):
        """
        method for setting value in single combo_box

        Parameters
        ----------
        combo_box_name  : str
                          name of combo_box
        common_key      : str, None
                          common data key to append all values
        key_name        : str, None
                          customized name of key

        """
        try:
            Assertor.assert_data_types([combo_box_name, common_key, key_name],
                                       [str, (type(None), str), (type(None), str)])
            combo_box_text = str(
                getattr(self.parent.ui_form, "combo_box_" + combo_box_name).currentText())
            values = {key_name if key_name else combo_box_name: combo_box_text}

            if common_key and common_key not in self.data.keys():
                self.data.update({common_key: values})
            elif common_key and common_key in self.data.keys():
                self.data[common_key].update(values)
            else:
                self.data.update(values)

            for keys, vals in self.data.copy().items():
                if isinstance(vals, dict):
                    self.data.update({keys: dict(sorted(vals.items()))})

            for keys, vals in self.data.copy().items():
                if isinstance(vals, dict):
                    for key, val in vals.copy().items():
                        if not val:
                            self.data[keys].pop(key)
                if not vals:
                    self.data.pop(keys)
        except Exception as set_combo_box_error:
            self.parent.error_view.show_error(set_combo_box_error)

    @pyqtSlot()
    def clear_combo_boxes(self, combo_boxes: list):
        """
        method for clearing content of combo_boxes

        Parameters
        ----------
        combo_boxes     : list
                          list of comboboxes

        """
        Assertor.assert_data_types([combo_boxes], [list])
        for combo_box in combo_boxes:
            getattr(self.parent.ui_form, "combo_box_" + combo_box).setCurrentIndex(0)
            self.set_combo_box(combo_box)

    @pyqtSlot()
    def update_line_edits(self, line_edit_name: str, line_edits: list, obj: object = None,
                          method: str = None, postfix: str = None, data: dict = None):
        """
        method for updating the value of multiple line_edits

        Parameters
        ----------
        line_edit_name  : str
                          name of line_edit to get values from
        line_edits      : list
                          all line_edits to update values for based on input, see line_edit_name
        obj             : object
                          name of object to get values to update line_edits
        method          : str
                          name of method in obj to use to get values to update line_edits
        postfix         : str
                          index if used in naming of line_edits
        data            : dict
                          dictionary with data to set if no object or method used

        """
        postfix = postfix if postfix else ""
        line_edit = getattr(self.parent.ui_form, "line_edit_" + line_edit_name + postfix)
        try:
            Assertor.assert_data_types([line_edit_name, line_edits, obj, method, postfix],
                                       [str, list, (type(None), object), (type(None), str),
                                        (type(None), str), (type(None), str)])
            line_edit_text = line_edit.text().strip()
            if line_edit_text and line_edit_text not in self.data.values():
                self.set_line_edits(line_edit_text, line_edits, obj, method, postfix, data)
            elif line_edit_text and line_edit_text in self.data.values():
                self.get_line_edits(line_edits, postfix)
            else:
                self.clear_line_edits(line_edits, postfix)
        except Exception as update_error:
            self.clear_line_edits(line_edits, postfix)
            self.parent.error_view.show_error(update_error, self.data)
            line_edit.setFocus()

    @pyqtSlot()
    def clear_empty_line_edits(self, line_edit_name: str, line_edits: list, postfix: str):
        """
        method for clearing empty line edits

        Parameters
        ----------
        line_edit_name  : str
                          name of line_edit to get values from
        line_edits      : list
                          all line_edits to update values for based on input, see line_edit_name
        postfix         : str
                          index if used in naming of line_edits

        """
        line_edit = getattr(self.parent.ui_form, "line_edit_" + line_edit_name + postfix).text()
        if not line_edit:
            self.clear_line_edits(line_edits, postfix)

    @pyqtSlot()
    def set_line_edits(self, line_edit_text: str, line_edits: list, obj: object = None,
                       method: str = None, postfix: str = None, data: dict = None):
        """
        method for setting values of multiple line_edits

        Parameters
        ----------
        line_edit_text  : str
                          value of inputted line_edit
        line_edits      : list
                          list of line_edit names to update values
        obj             : object
                          object with method for extracting values to update line_edits
        method          : str
                          name of method to call in object
        postfix         : str
                          index if used in naming of line_edits
        data            : dict
                          dictionary with data to set if no object or method used

        """
        model_info = getattr(obj(line_edit_text), method)() if obj and method else data
        try:
            Assertor.assert_data_types([line_edit_text, line_edits, obj, method, postfix, data],
                                       [str, list, (object, type(None)), (str, type(None)),
                                        (str, type(None)), (dict, type(None))])
            if not model_info:
                return
            for line_edit in line_edits:
                if line_edit in model_info.keys():
                    info = model_info[line_edit]
                    line_edit_name = line_edit + postfix if postfix else line_edit
                    self.set_line_edit(line_edit_name, data=info)
        except Exception as set_line_edits_error:
            self.clear_line_edits(line_edits, postfix)
            self.parent.error_view.show_error(set_line_edits_error, self.data)

    @pyqtSlot()
    def set_line_edit(self, line_edit_name: str, obj: object = None, method: str = None,
                      data: str = None, clearing: object = None):
        """
        method for setting value of a single line_edit

        Parameters
        ----------
        line_edit_name  : str
                          name of line_edit to set value
        obj             : object
                          object to get values from
        method          : str
                          name of method to call in obj to get values
        data            : str
                          value to set if no obj or method used
        clearing        : object
                          object for clearing data after exceptions

        """
        line_edit = getattr(self.parent.ui_form, "line_edit_" + line_edit_name)
        try:
            Assertor.assert_data_types([line_edit_name, obj, method, data, clearing],
                                       [str, (object, type(None)), (str, type(None)),
                                        (str, type(None)), (object, type(None))])
            line_edit_text = line_edit.text().strip() if not data else data
            new_value = line_edit_text not in self.data.values()
            if line_edit_text and new_value and obj:
                output = getattr(obj(line_edit_text), method)() if not data else data
                self.data.update({line_edit_name: output})
            elif line_edit_text and new_value and not obj:
                output = line_edit_text
                self.data.update({line_edit_name: output})
            elif line_edit_text and not new_value:
                output = line_edit_text
                self.data.update({line_edit_name: output})
            else:
                output = ""
                self.clear_line_edit(line_edit_name)
            getattr(self.parent.ui_form, "line_edit_" + line_edit_name).setText(output)
        except Exception as set_line_edit_error:
            self.parent.error_view.show_error(set_line_edit_error, self.data)
            self.clear_line_edit(line_edit_name)
            getattr(self.parent.ui_form, "line_edit_" + line_edit_name).setFocus()
            if clearing:
                clearing()

    @pyqtSlot()
    def get_line_edits(self, line_edits: list, postfix: str = None):
        """
        method for getting values of multiple line_edits

        Parameters
        ----------
        line_edits  : list
                      names of line_edits to get
        postfix     : str
                      index if used in naming of line_edits

        """
        Assertor.assert_data_types([line_edits, postfix], [list, (str, type(None))])
        for line_edit in line_edits:
            line_edit = "line_edit_" + (line_edit + postfix if postfix else line_edit)
            if line_edit in self.data.keys():
                getattr(self.parent.ui_form, line_edit).setText(
                    self.data[line_edit])

    @pyqtSlot()
    def clear_line_edits(self, line_edits: list, postfix: str = None):
        """
        method for clearing the content of multiple line_edits

        Parameters
        ----------
        line_edits  : list
                      list of names of line_edits to clear content
        postfix     : str
                      index if used in naming of line_edits

        """
        Assertor.assert_data_types([line_edits, postfix], [list, (str, type(None))])
        for line_edit in line_edits:
            line_edit_name = line_edit + postfix if postfix else line_edit
            self.clear_line_edit(line_edit_name)

    @pyqtSlot()
    def clear_line_edit(self, line_edit_name: str):
        """
        method for clearing content of a single line_edit

        Parameters
        ----------
        line_edit_name  : str
                          name of line_edit to clear the content

        """
        Assertor.assert_data_types([line_edit_name], [str])
        line_edit = "line_edit_" + line_edit_name
        if line_edit_name in self.data.keys():
            getattr(self.parent.ui_form, line_edit).clear()
            self.data.pop(line_edit_name)
        else:
            getattr(self.parent.ui_form, line_edit).clear()

    @pyqtSlot()
    def clear_data(self, key_name: str, common_key: str):
        """
        method for clearing single data point from self.data

        Parameters
        ----------
        key_name    : str
                      key_name to pop
        common_key  : str
                      common_key if data point stored as common_key

        """
        for key, val in self.data.items():
            if common_key == key and isinstance(val, dict):
                if key_name in val.keys():
                    val.pop(key_name)
