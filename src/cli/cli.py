from psycopg2.errors import *


class QueryException(Exception):
    pass


class QueryHandler:
    def __init__(self, connection, config) -> None:
        self.connection = connection
        self.config = config

    def execute_query(self, query: str):
        cursor = self.connection.cursor()
        try:
            cursor.execute(query)
            rows = cursor.fetchall()
            columns = [column.name for column in cursor.description]
            cursor.close()
            return columns, rows

        except (Exception, DatabaseError) as error:
            cursor.execute("ROLLBACK")
            cursor.close()
            raise QueryException(f"An error occured: {error}")

    def list_databases(self):
        cursor = self.connection.cursor()
        try:
            cursor.execute("""SELECT datname FROM pg_catalog.pg_database""")
            databases = cursor.fetchall()
            databases = [
                database[0]
                for database in databases
                if database[0] not in ["postgres", "template0", "template1"]
            ]
            cursor.close()
            return databases
        except (Exception, DatabaseError) as error:
            cursor.close()
            print(error)

    def list_tables(self):
        cursor = self.connection.cursor()
        try:
            cursor.execute(
                """
                SELECT table_name
                FROM information_schema.tables
                WHERE table_schema = 'public'
                ORDER BY table_name;
                """
            )
            tables = cursor.fetchall()
            tables = [
                database[0]
                for database in tables
                if database[0] not in ["postgres", "template0", "template1"]
            ]
            cursor.close()
            return tables
        except (Exception, DatabaseError) as error:
            cursor.close()
            print(error)
