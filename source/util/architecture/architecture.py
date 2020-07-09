# -*- coding: utf-8 -*-
"""
Architecture diagram

"""

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

from diagrams import Cluster, Diagram, Edge
from diagrams.programming.language import Python, C, Bash
from diagrams.oci.monitoring import Logging
from diagrams.onprem.client import User
from diagrams.oci.storage import Filestorage, FilestorageGrey
from diagrams.aws.database import DocumentdbMongodbCompatibility

from source.util import __version__

name = "Stressa v." + __version__

with Diagram(name=name, show=False, direction="TB"):
    users = User()
    bash = Bash("")
    main = Python("main")

    with Cluster("presentation layer (source/ui)"):
        with Cluster("package: views"):
            views = Python("views")
            with Cluster("forms"):
                forms = FilestorageGrey("forms")

            with Cluster("logs"):
                ui_log = Logging("ui")

        with Cluster("package: models"):
            models = Python("models")

        with Cluster("package: util"):
            ui_util = Python("util")

        with Cluster("images"):
            images = FilestorageGrey("images")

        with Cluster("package: graphics"):
            graphics = Python("graphics")

    with Cluster("application layer (source/app)"):
        with Cluster("package: scrapers"):
            with Cluster("temp"):
                cache = C("cache")
            scrapers = Python("scrapers")

        with Cluster("package: processing"):
            with Cluster("package: engine"):
                operations = Python("operations")
                signals = Python("signals")
                process = Python("process")
                sub_model = Python("submodel")

                engine = [operations, signals, process, sub_model]

            processes = Python("processes")

            with Cluster("procedure"):
                procedure = FilestorageGrey("procedure")

    with Cluster("domain layer (source/domain)"):
        entities = Python("entities")
        values = Python("values")

    with Cluster("persistence layer (source/db)"):
        mongo_db = Python("dao")

    with Cluster("cross-cutting layer (source/util)"):
        with Cluster("logs"):
            util_logs = Logging("app")
        logging = Python("logging")
        caching = Python("caching")
        profiling = Python("profiling")

    mongo_db_atlas = DocumentdbMongodbCompatibility("MongoDB Atlas:\n stressa-6pyxy.mongodb.net")

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

    processes << engine
    processes << scrapers
    processes >> procedure
    processes << entities
    operations << entities
    operations << values
    operations << sub_model
    scrapers << entities
    scrapers >> cache

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

