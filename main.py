import yaml
from src.operators import Operator


with open("config.yaml") as file:
    config = yaml.safe_load(file)

operator = Operator(config=config)
operator.query_handler.list_tables()

operator.connector.close_connection(connection=operator.connection)
