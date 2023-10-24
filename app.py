import yaml
import pandas as pd
import gradio as gr
from src.cli.cli import QueryException
from src.operators import Operator
from src.css import CSS

with open("config.yaml") as file:
    config = yaml.safe_load(file)

operator = Operator(config=config)
databases_choices = operator.query_handler.list_databases()
tables = operator.query_handler.list_tables()
data = pd.DataFrame(tables, columns=["table"])


def change_database(database):
    print("refresh connection", database)
    operator.refresh_connection(database=database)
    tables = operator.query_handler.list_tables()
    data = pd.DataFrame(tables, columns=["table"])
    return data


def execute_query(query):
    try:
        if query == "":
            return None, "Query can't be empty."
        else:
            columns, rows = operator.query_handler.execute_query(query=query)
            data = pd.DataFrame(rows, columns=columns)
            message = f"Returned {len(data)} rows."
            return data, message
    except QueryException as error:
        return None, str(error)


with gr.Blocks(css=CSS) as demo:
    gr.Markdown("# PostgreSQL Query Editor.")
    gr.Markdown("")
    with gr.Row():
        with gr.Column(scale=2):
            databases = gr.Radio(
                value=config["default"]["database"],
                label="Select Database",
                choices=databases_choices,
                type="value",
            )
            tables = gr.DataFrame(
                label="Tables", value=data, container=False, elem_id="dataframe"
            )

        with gr.Column(scale=8):
            query_editor = gr.TextArea(
                label="🗒️ Query Editor",
                interactive=True,
                placeholder="Enter query here...",
                elem_id="query-editor",
            )
            with gr.Row():
                log = gr.TextArea(
                    label="Log message",
                    scale=8,
                    interactive=False,
                    max_lines=2,
                    lines=2,
                )
                with gr.Column():
                    run_query = gr.Button(
                        value="▶️ Run Query",
                        size="sm",
                        scale=2,
                        variant="primary",
                    )
                    clear = gr.Button(
                        value="Clear",
                        size="sm",
                        scale=2,
                        variant="secondary",
                    )
            result_table = gr.DataFrame(label="Output", value=None)

    run_query.click(
        fn=execute_query,
        inputs=[query_editor],
        outputs=[result_table, log],
    )
    databases.change(fn=change_database, inputs=[databases], outputs=[tables])

if __name__ == "__main__":
    demo.launch()
    operator.connector.close_connection(operator.connection)
    print("App stopped")
