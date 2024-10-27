# -*- coding: utf-8 -*-
"""
Module containing class for creating HTML table

"""
__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'


class CreateHtmlTable:
    """
    creating HTML table class

    """
    trans = {"header": "Adresse", "matrikkel": "Matrikkel", "address": "Gateadresse",
             "zip": "Postnummer", "city": "By", "municipality": "Kommune",
             "census": "Valgkrets", "district": "Distrikt", "lat": "Breddegrad",
             "long": "Lengdegrad", "finnkode": "Finnkode", "name": "Nabolag"}

    def __init__(self, data):
        """
        Constructor / Instantiating

        """
        self.data = data

    def html_table(self):
        """
        method for producing HTML table

        """

        style = """
                <head><style>
                .leaflet-popup-content-wrapper {background-color: #f3f9ff; color:black}
                </style></head>
                """
        info = []
        for keys, values in self.data.items():
            if values and keys not in ["sw", "ne", "orderLineId"]:
                if isinstance(values, dict):
                    for key, val in values.items():
                        element = str(val).replace("/", " / ")
                        if key != "mapBounds":
                            if key == "city":
                                info.append("<tr><td>" + "Område: " + element + "</td></tr>")
                            elif key in self.trans:
                                info.append(
                                    "<tr><td>" + self.trans[key] + ": " + element + "</td></tr>")
                else:
                    if keys in self.trans:
                        element = "<tr><td>" + self.trans[keys] + ": " + \
                                  str(values).replace("/", " / ") + "</td></tr>"
                    else:
                        element = "<tr><td>" + keys + ": " + \
                                  str(values).replace("/", " / ") + "</td></tr>"
                    if keys == "finnkode":
                        info[0] = element
                    else:
                        info.append(element)
        return style + "<table>" + "".join(info) + "</table>"
