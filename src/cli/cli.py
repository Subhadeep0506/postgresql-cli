from psycopg2.errors import *


class QueryException(Exception):
    pass


class QueryHandler:
    def __init__(self, connection, config) -> None:
        self.connection = connection
        self.config = config

    def execute_query(self, query: str):
        try:
            cursor = self.connection.cursor()
            cursor.execute(query)
            rows = cursor.fetchall()
            columns = [column.name for column in cursor.description]
            cursor.close()
            return columns, rows

        except (Exception, DatabaseError) as error:
            cursor.close()
            print(error)
            raise QueryException

    def list_databases(self):
        try:
            cursor = self.connection.cursor()
            cursor.execute("""SELECT datname FROM pg_catalog.pg_database""")
            tables = cursor.fetchall()
            tables = [
                table[0]
                for table in tables
                if table[0] not in ["postgres", "template0", "template1"]
            ]
            cursor.close()
            return tables
        except (Exception, DatabaseError) as error:
            cursor.close()
            print(error)
