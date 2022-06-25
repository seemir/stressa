# -*- coding: utf-8 -*-
"""
Module containing logic for handling Images from housing advert

"""

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

from PyQt5.QtCore import QObject
from PyQt5.QtCore import QUrl

from .model import Model


class ImagesModel(Model):
    """
    Implementation of Image model

    """

    def __init__(self, parent: QObject):
        """
        Constructor / Instantiating class

        """
        super().__init__(parent)

        self.browser = self.parent.ui_form.web_view_images
        self.images = []
        self.descriptions = []
        self.current_image = 0

    def show_images(self, images: list, descriptions: list):
        """
        method for showing images from advert

        """
        self.images = images
        self.descriptions = descriptions
        self.browser.setUrl(QUrl(self.images[self.current_image]))
        self.parent.ui_form.label_description.setText(self.descriptions[self.current_image])
        self.browser.show()

    def next_image(self):
        """
        method for toggling next image

        """

        number_of_images = len(self.images)
        if self.images:
            if abs(self.current_image) < number_of_images - 1:
                self.current_image += 1
                self.browser.setUrl(QUrl(self.images[self.current_image]))
                self.parent.ui_form.label_description.setText(self.descriptions[self.current_image])
                self.browser.show()
            else:
                self.current_image = 0
                self.browser.setUrl(QUrl(self.images[self.current_image]))
                self.parent.ui_form.label_description.setText(self.descriptions[self.current_image])
                self.browser.show()

    def previous_image(self):
        """
        method for togging previous image

        """
        number_of_images = len(self.images)
        if self.images:
            if abs(self.current_image) < number_of_images - 1:
                self.current_image -= 1
                self.browser.setUrl(QUrl(self.images[self.current_image]))
                self.parent.ui_form.label_description.setText(self.descriptions[self.current_image])
                self.browser.show()
            else:
                self.current_image = 0
                self.browser.setUrl(QUrl(self.images[self.current_image]))
                self.parent.ui_form.label_description.setText(self.descriptions[self.current_image])
                self.browser.show()
