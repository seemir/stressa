# -*- coding: utf-8 -*-

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

from io import BytesIO
from os.path import dirname as up

from folium import Map, Marker, TileLayer, LayerControl, Popup
from folium.features import CustomIcon

from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QObject

from .model import Model

from ..util import CreateHtmlTable


class MapModel(Model):

    def __init__(self, parent: QObject):
        super().__init__(parent)

    @staticmethod
    def show_map(coords: list, web_engine_view: QWebEngineView, pop_up: str = None, pois=None):
        icon_size = (40, 40)
        max_width = 400
        bytes_io = BytesIO()
        map_builder = Map(location=coords, tiles="CartoDB positron", zoom_start=16)
        map_icon = CustomIcon(up(up(__file__)) + "/images/marker.png",
                              icon_size=icon_size)
        if pop_up:
            Marker(coords, icon=map_icon, popup=Popup(pop_up, max_width=max_width)).add_to(
                map_builder)
        else:
            Marker(coords, icon=map_icon).add_to(map_builder)

        if pois:
            for poi in pois:
                pois_icon = CustomIcon(up(up(__file__)) + "/images/university.png",
                                       icon_size=icon_size)
                lat = poi["Breddegrad"]
                long = poi["Lengdegrad"]
                pois_pop_up = Popup(CreateHtmlTable(poi).html_table(),
                                    max_width=max_width)
                Marker(location=[lat, long], icon=pois_icon,
                       popup=pois_pop_up).add_to(map_builder)

        TileLayer('OpenStreetMap').add_to(map_builder)
        TileLayer('Stamen Toner').add_to(map_builder)
        TileLayer('Stamen Terrain').add_to(map_builder)
        LayerControl().add_to(map_builder)
        map_builder.save(bytes_io, close_file=False)
        web_engine_view.setHtml(bytes_io.getvalue().decode())
        web_engine_view.show()
