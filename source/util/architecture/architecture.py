# -*- coding: utf-8 -*-
"""
Architecture diagram

"""

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

from diagrams.programming.language import Python, Bash
from diagrams.onprem.client import User, Client
from diagrams.oci.storage import FileStorage
from diagrams import Cluster, Diagram, Edge
from diagrams.oci.governance import Logging

from source.util.architecture.custom import Finansportalen, Finn, Posten, SIFO, Sqlite, SSB, \
    Skatteetaten
from source.util.architecture.settings import name, font_size

with Diagram(name=name, show=False, direction="TB", outformat="pdf",
             node_attr={"fontsize": font_size}):
    users = User()
    gui = Client()
    bash = Bash("")
    main = Python("main")

    with Cluster("presentation layer (source/ui)", graph_attr={"fontsize": font_size}):
        with Cluster("package: views", graph_attr={"fontsize": font_size}):
            views = Python("views")
            with Cluster("forms", graph_attr={"fontsize": font_size}):
                forms = FileStorage("forms")

            with Cluster("logs", graph_attr={"fontsize": font_size}):
                ui_log = Logging("ui")

        with Cluster("package: models", graph_attr={"fontsize": font_size}):
            models = Python("models")

        with Cluster("package: util", graph_attr={"fontsize": font_size}):
            ui_util = Python("util")

        with Cluster("images", graph_attr={"fontsize": font_size}):
            images = FileStorage("images")

        with Cluster("package: graphics", graph_attr={"fontsize": font_size}):
            graphics = Python("graphics")

    with Cluster("application layer (source/app)", graph_attr={"fontsize": font_size}):
        with Cluster("package: connectors", graph_attr={"fontsize": font_size}):
            with Cluster("temp", graph_attr={"fontsize": font_size}):
                cache = Sqlite("cache")
            connectors = Python("connectors")

        with Cluster("package: processing", graph_attr={"fontsize": font_size}):
            with Cluster("package: engine", graph_attr={"fontsize": font_size}):
                operations = Python("operations")
                signals = Python("signals")
                process = Python("process")
                sub_model = Python("submodel")

                engine = [operations, signals, process, sub_model]

            processes = Python("processes")

            with Cluster("procedure", graph_attr={"fontsize": font_size}):
                procedure = FileStorage("procedure")

    with Cluster("domain layer (source/domain)", graph_attr={"fontsize": font_size}):
        entities = Python("entities")
        values = Python("values")

    with Cluster("persistence layer (source/db)", graph_attr={"fontsize": font_size}):
        dao = Python("dao")

    with Cluster("cross-cutting layer (source/util)", graph_attr={"fontsize": font_size}):
        with Cluster("logs", graph_attr={"fontsize": font_size}):
            util_logs = Logging("app")
        logging = Python("logging")
        caching = Python("caching")
        profiling = Python("profiling")

    with Cluster("API service", graph_attr={"fontsize": font_size}):
        web = [Finn("Finn API"), Posten("\nPosten \n Adressesøk API"),
               Finansportalen("Finansportalen\n Grunndata\n XML Feed"),
               SIFO("SIFO API"), SSB("SSB API (pyjstat)"), Skatteetaten("\nSkatte- \nkalkulator API")]

    users >> bash << main << views
    users << gui << bash
    bash << ui_log

    views << forms << images
    views << models
    views >> Edge(color="gray") << ui_log
    models << ui_util
    models << graphics
    models << values
    models << processes
    graphics << values

    values >> entities

    dao << logging

    bash << util_logs
    logging >> util_logs
    logging >> processes
    logging >> connectors
    logging >> operations
    caching >> connectors
    profiling >> processes

    processes << engine
    processes << connectors
    processes >> procedure
    processes << entities
    operations << entities
    operations << values
    operations << sub_model
    connectors << entities
    connectors >> cache
    web >> connectors
