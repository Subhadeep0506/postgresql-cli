import psycopg2


class Connector:
    def __init__(self) -> None:
        pass

    def init_connection(self, config):
        connection = psycopg2.connect(
            host=config["default"]["host"],
            database=config["default"]["database"],
            user=config["default"]["user"],
            port=config["default"]["port"],
            password=config["default"]["password"],
        )

        return connection

    def close_connection(self, connection):
        connection.close()
