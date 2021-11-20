# -*- coding: utf-8 -*-

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

from PyQt5.QtCore import QObject
from PyQt5.QtCore import QUrl

from .model import Model


class ImagesModel(Model):

    def __init__(self, parent: QObject):
        super().__init__(parent)

        self.browser = self.parent.ui.web_view_images
        self.images = []
        self.current_image = 0

    def show_images(self, images: list):
        self.images = images
        self.browser.setUrl(QUrl(self.images[self.current_image]))
        self.browser.show()

    def next_image(self):
        number_of_images = len(self.images)
        if self.images:
            if abs(self.current_image) < number_of_images - 1:
                self.current_image += 1
                self.browser.setUrl(QUrl(self.images[self.current_image]))
                self.browser.show()
            else:
                self.current_image = 0
                self.browser.setUrl(QUrl(self.images[self.current_image]))
                self.browser.show()

    def previous_image(self):
        number_of_images = len(self.images)
        if self.images:
            if abs(self.current_image) < number_of_images - 1:
                self.current_image -= 1
                self.browser.setUrl(QUrl(self.images[self.current_image]))
                self.browser.show()
            else:
                self.current_image = 0
                self.browser.setUrl(QUrl(self.images[self.current_image]))
                self.browser.show()
