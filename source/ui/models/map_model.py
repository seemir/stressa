# -*- coding: utf-8 -*-
"""
Module containing all GIS related data from advert

"""

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

from io import BytesIO
from os.path import dirname as up

from folium import Map, Marker, TileLayer, LayerControl, Popup, FeatureGroup
from folium.plugins import MarkerCluster
from folium.features import CustomIcon

from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QObject

from .model import Model

from ..util import CreateHtmlTable


class MapModel(Model):
    """
    Implementation of Map Model class

    """

    def __init__(self, parent: QObject):
        """
        Constructor / Instantiating of class

        """
        super().__init__(parent=parent)

    @staticmethod
    def show_map(coords: list, web_engine_view: QWebEngineView, pop_up: str = None, university=None,
                 kindergarden=None, schools=None, highschools=None, transport=None, charging=None,
                 bicycle=None, groceries=None, services=None, sports=None):
        """
        method for showing map

        """
        icon_size = (45, 45)
        small_icon = (40, 40)
        max_width = 400
        bytes_io = BytesIO()
        map_builder = Map(location=coords, tiles="CartoDB positron", zoom_start=16)
        map_icon = CustomIcon(up(up(__file__)) + "/images/marker.png",
                              icon_size=icon_size)

        if kindergarden:
            kindergarden_cluster = MarkerCluster(name='barnehage', show=False).add_to(map_builder)
            for pois in kindergarden:
                pois_icon = CustomIcon(up(up(__file__)) + "/images/kindergarden.png",
                                       icon_size=small_icon)
                lat = pois["Breddegrad"]
                long = pois["Lengdegrad"]
                pois_pop_up = Popup(CreateHtmlTable(pois).html_table(),
                                    max_width=max_width)
                Marker(location=[lat, long], icon=pois_icon,
                       popup=pois_pop_up).add_to(kindergarden_cluster)

        if schools:
            schools_cluster = MarkerCluster(name="barneskole", show=False).add_to(map_builder)
            for pois in schools:
                pois_icon = CustomIcon(up(up(__file__)) + "/images/schools.png",
                                       icon_size=small_icon)
                lat = pois["Breddegrad"]
                long = pois["Lengdegrad"]
                pois_pop_up = Popup(CreateHtmlTable(pois).html_table(),
                                    max_width=max_width)
                Marker(location=[lat, long], icon=pois_icon,
                       popup=pois_pop_up).add_to(schools_cluster)

        if highschools:
            highschools_cluster = MarkerCluster(name='vidregåendeskole', show=False).add_to(
                map_builder)
            for pois in highschools:
                pois_icon = CustomIcon(up(up(__file__)) + "/images/highschools.png",
                                       icon_size=small_icon)
                lat = pois["Breddegrad"]
                long = pois["Lengdegrad"]
                pois_pop_up = Popup(CreateHtmlTable(pois).html_table(),
                                    max_width=max_width)
                Marker(location=[lat, long], icon=pois_icon,
                       popup=pois_pop_up).add_to(highschools_cluster)

        if university:
            university_cluster = MarkerCluster(name='hogskole_universitet', show=False).add_to(
                map_builder)
            for pois in university:
                pois_icon = CustomIcon(up(up(__file__)) + "/images/university.png",
                                       icon_size=small_icon)
                lat = pois["Breddegrad"]
                long = pois["Lengdegrad"]
                pois_pop_up = Popup(CreateHtmlTable(pois).html_table(),
                                    max_width=max_width)
                Marker(location=[lat, long], icon=pois_icon,
                       popup=pois_pop_up).add_to(university_cluster)

        if transport:
            transport_cluster = MarkerCluster(name='holdeplass', show=False).add_to(map_builder)
            for pois in transport:
                pois_icon = CustomIcon(up(up(__file__)) + "/images/transport.png",
                                       icon_size=small_icon)
                lat = pois["Breddegrad"]
                long = pois["Lengdegrad"]
                pois_pop_up = Popup(CreateHtmlTable(pois).html_table(),
                                    max_width=max_width)
                Marker(location=[lat, long], icon=pois_icon,
                       popup=pois_pop_up).add_to(transport_cluster)

        if charging:
            charging_cluster = MarkerCluster(name='ladeplass', show=False).add_to(map_builder)
            for pois in charging:
                pois_icon = CustomIcon(up(up(__file__)) + "/images/charging.png",
                                       icon_size=small_icon)
                lat = pois["Breddegrad"]
                long = pois["Lengdegrad"]
                pois_pop_up = Popup(CreateHtmlTable(pois).html_table(),
                                    max_width=max_width)
                Marker(location=[lat, long], icon=pois_icon,
                       popup=pois_pop_up).add_to(charging_cluster)

        if bicycle:
            bicyle_cluster = MarkerCluster(name='bysykler', show=False).add_to(map_builder)
            for pois in bicycle:
                pois_icon = CustomIcon(up(up(__file__)) + "/images/bicycle.png",
                                       icon_size=small_icon)
                lat = pois["Breddegrad"]
                long = pois["Lengdegrad"]
                pois_pop_up = Popup(CreateHtmlTable(pois).html_table(),
                                    max_width=max_width)
                Marker(location=[lat, long], icon=pois_icon,
                       popup=pois_pop_up).add_to(bicyle_cluster)

        shops_cluster = MarkerCluster(name="butikker", show=False).add_to(map_builder)

        if groceries:
            for pois in groceries:
                pois_icon = CustomIcon(up(up(__file__)) + "/images/groceries.png",
                                       icon_size=small_icon)
                lat = pois["Breddegrad"]
                long = pois["Lengdegrad"]
                pois_pop_up = Popup(CreateHtmlTable(pois).html_table(),
                                    max_width=max_width)
                Marker(location=[lat, long], icon=pois_icon,
                       popup=pois_pop_up).add_to(shops_cluster)

        if services:
            for pois in services:
                pois_icon = CustomIcon(up(up(__file__)) + "/images/services.png",
                                       icon_size=small_icon)
                lat = pois["Breddegrad"]
                long = pois["Lengdegrad"]
                pois_pop_up = Popup(CreateHtmlTable(pois).html_table(),
                                    max_width=max_width)
                Marker(location=[lat, long], icon=pois_icon,
                       popup=pois_pop_up).add_to(shops_cluster)

        if sports:
            sports_cluster = MarkerCluster(name='sportsaktiviteter', show=False).add_to(map_builder)
            for pois in sports:
                pois_icon = CustomIcon(up(up(__file__)) + "/images/sports.png",
                                       icon_size=small_icon)
                lat = pois["Breddegrad"]
                long = pois["Lengdegrad"]
                pois_pop_up = Popup(CreateHtmlTable(pois).html_table(),
                                    max_width=max_width)
                Marker(location=[lat, long], icon=pois_icon,
                       popup=pois_pop_up).add_to(sports_cluster)

        if pop_up:
            Marker(coords, icon=map_icon, popup=Popup(pop_up, max_width=max_width)).add_to(
                map_builder)
        else:
            Marker(coords, icon=map_icon).add_to(map_builder)

        TileLayer('CartoDB dark_matter').add_to(map_builder)
        TileLayer('OpenStreetMap').add_to(map_builder)

        TileLayer('https://{s}.tile.openstreetmap.fr/hot/{z}/{x}/{y}{r}.png',
                  attr='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> '
                       'contributors, Tiles style by <a href="https://www.hotosm.org/" '
                       'target="_blank">Humanitarian OpenStreetMap Team</a> hosted by '
                       '<a href="https://openstreetmap.fr/" target="_blank">OpenStreetMap '
                       'France</a>', name='openstreetmap_hot').add_to(map_builder)

        TileLayer('https://{s}.tile-cyclosm.openstreetmap.fr/cyclosm/{z}/{x}/{y}.png',
                  attr='<a href="https://github.com/cyclosm/cyclosm-cartocss-style/releases" '
                       'title="CyclOSM - Open Bicycle render">CyclOSM</a> | Map data: &copy; '
                       '<a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> '
                       'contributors',
                  name='cyclosm').add_to(map_builder)

        TileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/'
                  'tile/{z}/{y}/{x}', attr='Tiles &copy; Esri &mdash; Source: Esri, i-cubed, USDA, '
                                           'USGS, AEX, GeoEye, Getmapping, Aerogrid, IGN, IGP, '
                                           'UPR-EGP, and the GIS User Community',
                  name='esri_worldimagery').add_to(map_builder)

        TileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/World_Street_Map/MapServer/'
                  'tile/{z}/{y}/{x}', attr='Tiles &copy; Esri &mdash; Source: Esri, DeLorme, '
                                           'NAVTEQ, USGS, Intermap, iPC, NRCAN, Esri Japan, METI, '
                                           'Esri China (Hong Kong), Esri (Thailand), TomTom, 2012',
                  name='esri_worldstreetmap').add_to(map_builder)

        TileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/World_Topo_Map/MapServer/'
                  'tile/{z}/{y}/{x}', attr='Tiles &copy; Esri &mdash; Esri, DeLorme, NAVTEQ, '
                                           'TomTom, Intermap, iPC, USGS, FAO, NPS, NRCAN, GeoBase, '
                                           'Kadaster NL, Ordnance Survey, Esri Japan, METI, Esri '
                                           'China (Hong Kong), and the GIS User Community',
                  name='esri_worldtopomap').add_to(map_builder)

        TileLayer('https://tileserver.memomaps.de/tilegen/{z}/{x}/{y}.png',
                  attr='Map <a href="https://memomaps.de/">memomaps.de</a> '
                       '<a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, '
                       'map data &copy; <a href="https://www.openstreetmap.org/copyright">'
                       'OpenStreetMap</a> contributors', name='openvkarte').add_to(map_builder)

        TileLayer('https://{s}.tile-cyclosm.openstreetmap.fr/cyclosm/{z}/{x}/{y}.png',
                  attr='<a href="https://github.com/cyclosm/cyclosm-cartocss-style/releases" '
                       'title="CyclOSM - Open Bicycle render">CyclOSM</a> | Map data: &copy; '
                       '<a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> '
                       'contributors', name='cyclosm').add_to(map_builder)

        TileLayer('http://tile.mtbmap.cz/mtbmap_tiles/{z}/{x}/{y}.png',
                  attr='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> '
                       'contributors &amp; USGS', name='mtbmap').add_to(map_builder)

        railway_feature = FeatureGroup('jernbane_tbane', show=False)
        TileLayer('https://{s}.tiles.openrailwaymap.org/standard/{z}/{x}/{y}.png',
                  attr='Map data: &copy; <a href="https://www.openstreetmap.org/copyright'
                       '">OpenStreetMap</a> contributors | Map style: &copy; <a href='
                       '"https://www.OpenRailwayMap.org">OpenRailwayMap</a> (<a href='
                       '"https://creativecommons.org/licenses/by-sa/3.0/">CC-BY-SA</a>)',
                  name='openrailwaymap').add_to(railway_feature)
        railway_feature.add_to(map_builder)

        safecast_feature = FeatureGroup('miljø', show=False)
        TileLayer('https://s3.amazonaws.com/te512.safecast.org/{z}/{x}/{y}.png',
                  attr='Map data: &copy; <a href="https://www.openstreetmap.org/copyright">'
                       'OpenStreetMap</a> contributors | Map style: &copy; '
                       '<a href="https://blog.safecast.org/about/">SafeCast</a> '
                       '(<a href="https://creativecommons.org/licenses/by-sa/3.0/">CC-BY-SA</a>)',
                  name='safecast').add_to(safecast_feature)
        safecast_feature.add_to(map_builder)

        trails_feature = FeatureGroup('turstil', show=False)
        TileLayer('https://tile.waymarkedtrails.org/hiking/{z}/{x}/{y}.png',
                  attr='Map data: &copy; <a href="https://www.openstreetmap.org/copyright">'
                       'OpenStreetMap</a> contributors | Map style: &copy; '
                       '<a href="https://waymarkedtrails.org">waymarkedtrails.org</a> '
                       '(<a href="https://creativecommons.org/licenses/by-sa/3.0/">CC-BY-SA</a>)',
                  name='waymarkedtrails_hiking').add_to(trails_feature)
        trails_feature.add_to(map_builder)

        cycling_feature = FeatureGroup('sykkelsti', show=False)
        TileLayer('https://tile.waymarkedtrails.org/cycling/{z}/{x}/{y}.png',
                  attr='Map data: &copy; <a href="https://www.openstreetmap.org/copyright">'
                       'OpenStreetMap</a> contributors | Map style: &copy; '
                       '<a href="https://waymarkedtrails.org">waymarkedtrails.org</a> '
                       '(<a href="https://creativecommons.org/licenses/by-sa/3.0/">CC-BY-SA</a>)',
                  name='waymarkedtrails_cycling').add_to(cycling_feature)
        cycling_feature.add_to(map_builder)

        slopes_feature = FeatureGroup('bakker_helning', show=False)
        TileLayer('https://tile.waymarkedtrails.org/slopes/{z}/{x}/{y}.png',
                  attr='Map data: &copy; <a href="https://www.openstreetmap.org/copyright">'
                       'OpenStreetMap</a> contributors | Map style: &copy; '
                       '<a href="https://waymarkedtrails.org">waymarkedtrails.org</a> '
                       '(<a href="https://creativecommons.org/licenses/by-sa/3.0/">CC-BY-SA</a>)',
                  name='waymarkedtrails_slopes').add_to(slopes_feature)
        slopes_feature.add_to(map_builder)

        LayerControl().add_to(map_builder)
        map_builder.save(bytes_io, close_file=False)
        web_engine_view.setHtml(bytes_io.getvalue().decode())
        web_engine_view.show()
