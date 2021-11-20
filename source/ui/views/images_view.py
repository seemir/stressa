# -*- coding: utf-8 -*-

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

import os

from PyQt5.QtWidgets import QDialog, QWidget
from PyQt5.QtCore import Qt, pyqtSlot
from PyQt5.uic import loadUi

from source.util import Assertor

from ..models import ImagesModel


class ImagesView(QDialog):
    """
    Implementation of MapView

    """

    def __init__(self, parent: QWidget):
        """
        Constructor / Instantiation of class

        Parameters
        ----------
        parent  : QWidget
                  parent view of the metaview

        """
        Assertor.assert_data_types([parent], [QWidget])
        super().__init__(parent)
        self.ui = loadUi(os.path.join(os.path.dirname(__file__), "forms/images_form.ui"), self)
        self.ui.setWindowFlag(Qt.WindowMinimizeButtonHint, True)
        self.ui.setWindowFlag(Qt.WindowMaximizeButtonHint, True)
        self.ui.setWindowFlag(Qt.WindowContextHelpButtonHint, False)
        self._parent = parent
        self._images_model = ImagesModel(self)

        self.ui.push_button_forward.clicked.connect(self.next_image)
        self.ui.push_button_back.clicked.connect(self.previous_image)

    @property
    def parent(self):
        """
        parent getter

        Returns
        -------
        out     : QWidget
                  active parent in view

        """
        return self._parent

    @property
    def images_model(self):
        """
        images_model getter

        Returns
        -------
        out     : ImagesModel
                  active ImagesModel in view

        """
        return self._images_model

    @pyqtSlot()
    def previous_image(self):
        """
        method for selecting previous image

        """
        self.images_model.previous_image()

    @pyqtSlot()
    def next_image(self):
        """
        method for selecting next image

        """
        self.images_model.next_image()

    def clear_images(self):
        """
        method for clearing all images

        """
        self.ui.web_view_images.close()
        self.images_model.images = []
        self.images_model.current_image = 0
