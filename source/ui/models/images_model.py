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
        Method for showing images from advert using PyQt
        """
        self.images = images
        self.descriptions = descriptions

        current_image_url = self.images[self.current_image]
        html_image_content = self._render_white_background(current_image_url)
        self.browser.setHtml(html_image_content)

        self.parent.ui_form.label_description.setText(
            self.descriptions[self.current_image])

        self.browser.show()

    def next_image(self):
        """
        method for toggling next image

        """

        number_of_images = len(self.images)
        if self.images:
            if abs(self.current_image) < number_of_images - 1:
                self.current_image += 1
                html_image_content = self._render_white_background(
                    self.images[self.current_image])
                self.browser.setHtml(html_image_content)
                self.parent.ui_form.label_description.setText(
                    self.descriptions[self.current_image])
                self.browser.show()
            else:
                self.current_image = 0
                html_image_content = self._render_white_background(
                    self.images[self.current_image])
                self.browser.setHtml(html_image_content)
                self.parent.ui_form.label_description.setText(
                    self.descriptions[self.current_image])
                self.browser.show()

    def previous_image(self):
        """
        method for togging previous image

        """
        number_of_images = len(self.images)
        if self.images:
            if abs(self.current_image) < number_of_images - 1:
                self.current_image -= 1
                html_image_content = self._render_white_background(
                    self.images[self.current_image])
                self.browser.setHtml(html_image_content)
                self.parent.ui_form.label_description.setText(
                    self.descriptions[self.current_image])
                self.browser.show()
            else:
                self.current_image = 0
                html_image_content = self._render_white_background(
                    self.images[self.current_image])
                self.browser.setHtml(html_image_content)
                self.parent.ui_form.label_description.setText(
                    self.descriptions[self.current_image])
                self.browser.show()

    @staticmethod
    def _render_white_background(current_image_url: str):
        """
        Helper method for rendering image URL with a white background and zoom functionality.
        """
        html_content = f"""
                    <!DOCTYPE html>
                    <html lang="en">
                    <head>
                        <meta charset="UTF-8">
                        <meta name="viewport" content="width=device-width, initial-scale=1.0">
                        <style>
                            body {{
                                margin: 0;
                                background-color: white; /* Set background to white */
                                display: flex;
                                justify-content: center;
                                align-items: center;
                                height: 100vh; /* Full viewport height */
                            }}
                            img {{
                                max-width: 100%;
                                max-height: 100%;
                                object-fit: contain; /* Ensures image fits without distortion */
                                transition: transform 0.2s; /* Smooth transition for zoom effect */
                                cursor: zoom-in; /* Change cursor to zoom-in */
                                position: relative; /* Allow absolute positioning of the zoomed image */
                            }}
                        </style>
                        <script>
                            let isZoomed = false; // Track zoom state
                            let zoomScale = 2; // Set the zoom scale

                            function toggleZoom(event) {{
                                const img = document.querySelector('img');
                                const rect = img.getBoundingClientRect();
                                const offsetX = event.clientX - rect.left; // X position of the cursor relative to the image
                                const offsetY = event.clientY - rect.top; // Y position of the cursor relative to the image

                                if (isZoomed) {{
                                    img.style.transform = 'scale(1)'; // Reset to original size
                                    img.style.transformOrigin = 'center'; // Reset transform origin
                                }} else {{
                                    img.style.transform = 'scale(' + zoomScale + ')'; // Zoom in
                                    img.style.transformOrigin = `${{offsetX}}px ${{offsetY}}px`; // Set transform origin to cursor position
                                }}
                                isZoomed = !isZoomed; // Toggle zoom state
                            }}
                        </script>
                    </head>
                    <body>
                        <img src="{current_image_url}" alt="Image" onclick="toggleZoom(event)">
                    </body>
                    </html>
                    """
        return html_content
