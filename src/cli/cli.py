from psycopg2.errors import *


class Cli:
    def __init__(self, connection) -> None:
        self.connection = connection

    def execute_query(self, query: str):
        try:
            if self._verify_query(query=query):
                cursor = self.connection.cursor()
                cursor.execute(query)
                rows = cursor.fetchall()
                columns = [column.name for column in cursor.description]
                print("\t".join(columns))
                for row in rows:
                    print(" ".join([str(item) for item in row]))
                cursor.close()
            else:
                pass
        except (Exception, DatabaseError) as error:
            print(error)

    def _verify_query(self, query: str) -> bool:
        if query.strip().endswith(";"):
            return True
        else:
            return True
