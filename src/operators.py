from src.connector.connector import Connector
from src.cli.cli import QueryHandler


class Operator:
    def __init__(self, config) -> None:
        self.connector = None
        self.config = config

        self.connector = Connector()
        self.connection = self.connector.init_connection(config=self.config)
        self.query_handler = QueryHandler(
            connection=self.connection, config=self.config
        )

    def refresh_connection(self, database):
        self.config["default"]["database"] = database
        print(self.config)
        self.connection = self.connector.init_connection(config=self.config)
        self.query_handler = QueryHandler(
            connection=self.connection, config=self.config
        )
