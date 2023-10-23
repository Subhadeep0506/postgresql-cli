from psycopg2.errors import *


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

    def list_databases(self):
        try:
            cursor = self.connection.cursor()
            cursor.execute("""SELECT datname FROM pg_catalog.pg_database""")
            tables = list(cursor.fetchall())
            cursor.close()
            return tables
        except (Exception, DatabaseError) as error:
            cursor.close()
            print(error)
