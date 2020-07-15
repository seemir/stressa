# -*- coding: utf-8 -*-
"""
Architecture diagram

"""

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

from diagrams.aws.database import DocumentdbMongodbCompatibility
from diagrams.programming.language import Python, Bash
from diagrams.oci.storage import FilestorageGrey
from diagrams import Cluster, Diagram, Edge
from diagrams.oci.monitoring import Logging
from diagrams.onprem.client import User

from custom import Finansportalen, Finn, Posten, SIFO, Sqlite, SSB
from settings import name, font_size

with Diagram(name=name, show=False, direction="TB", outformat="pdf",
             node_attr={"fontsize": font_size}):
    users = User()
    bash = Bash("")
    main = Python("main")

    with Cluster("presentation layer (source/ui)", graph_attr={"fontsize": font_size}):
        with Cluster("package: views", graph_attr={"fontsize": font_size}):
            views = Python("views")
            with Cluster("forms", graph_attr={"fontsize": font_size}):
                forms = FilestorageGrey("forms")

            with Cluster("logs", graph_attr={"fontsize": font_size}):
                ui_log = Logging("ui")

        with Cluster("package: models", graph_attr={"fontsize": font_size}):
            models = Python("models")

        with Cluster("package: util", graph_attr={"fontsize": font_size}):
            ui_util = Python("util")

        with Cluster("images", graph_attr={"fontsize": font_size}):
            images = FilestorageGrey("images")

        with Cluster("package: graphics", graph_attr={"fontsize": font_size}):
            graphics = Python("graphics")

    with Cluster("application layer (source/app)", graph_attr={"fontsize": font_size}):
        with Cluster("package: scrapers", graph_attr={"fontsize": font_size}):
            with Cluster("temp", graph_attr={"fontsize": font_size}):
                cache = Sqlite("cache")
            scrapers = Python("scrapers")

        with Cluster("package: processing", graph_attr={"fontsize": font_size}):
            with Cluster("package: engine", graph_attr={"fontsize": font_size}):
                operations = Python("operations")
                signals = Python("signals")
                process = Python("process")
                sub_model = Python("submodel")

                engine = [operations, signals, process, sub_model]

            processes = Python("processes")

            with Cluster("procedure", graph_attr={"fontsize": font_size}):
                procedure = FilestorageGrey("procedure")

    with Cluster("domain layer (source/domain)", graph_attr={"fontsize": font_size}):
        entities = Python("entities")
        values = Python("values")

    with Cluster("persistence layer (source/db)", graph_attr={"fontsize": font_size}):
        mongo_db = Python("dao")

    with Cluster("cross-cutting layer (source/util)", graph_attr={"fontsize": font_size}):
        with Cluster("logs", graph_attr={"fontsize": font_size}):
            util_logs = Logging("app")
        logging = Python("logging")
        caching = Python("caching")
        profiling = Python("profiling")

    with Cluster("API service", graph_attr={"fontsize": font_size}):
        web = [Finn("Finn API"), Posten("\nPosten \n Adressesøk API"),
               Finansportalen("Finansportalen\n Grunndata\n XML Feed"),
               SIFO("SIFO API"), SSB("SSB API (pyjstat)")]

    mongo_db_atlas = DocumentdbMongodbCompatibility("\nMongoDB Atlas:\n stressa-6pyxy.mongodb.net")

    users << bash << main << views
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

    mongo_db_atlas >> Edge(color="gray") << mongo_db
    mongo_db << logging

    bash << util_logs
    logging >> util_logs
    logging >> processes
    logging >> scrapers
    logging >> operations
    caching >> scrapers
    profiling >> processes

    processes << engine
    processes << scrapers
    processes >> procedure
    processes << entities
    operations << entities
    operations << values
    operations << sub_model
    scrapers << entities
    scrapers >> cache
    web >> scrapers
