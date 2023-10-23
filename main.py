import yaml
import readline

from src.connector.connector import Connector
from src.cli.cli import Cli


with open("config.yaml") as file:
    config = yaml.safe_load(file)


connector = Connector()
connection = connector.init_connection(config=config)
cli = Cli(connection=connection)

print("Welcome to PostgreSQL CLI. Enter '\q' to quit the CLI.")
query = """"""
query = input("\npostgres $ ")

while query != "\q":
    cli.execute_query(query=query)
    query = input("\npostgres $ ")


connector.close_connection(connection=connection)
