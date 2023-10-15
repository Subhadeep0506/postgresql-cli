import yaml

from src.connector.connector import Connector
from src.cli.cli import Cli


with open("config.yaml") as file:
    config = yaml.safe_load(file)


connector = Connector()
connection = connector.init_connection(config=config)
cli = Cli(connection=connection)


query = """
SELECT * FROM employees LIMIT 10
"""
cli.execute_query(query=query)


connector.close_connection(connection=connection)
