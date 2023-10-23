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


def change_database(database):
    print("refresh connection", database)
    operator.refresh_connection(database=database)


def execute_query(query):
    try:
        if query == "":
            raise gr.Error("Query can't be empty.")
        else:
            columns, rows = operator.query_handler.execute_query(query=query)
            data = pd.DataFrame(rows, columns=columns)
            return data
    except QueryException as error:
        raise gr.Error(f"An error occured: {error}")


with gr.Blocks(css=CSS) as demo:
    gr.Markdown("# PostgreSQL Query Editor.")
    gr.Markdown("")
    with gr.Row():
        with gr.Column(scale=2):
            databases = gr.Radio(
                value=databases_choices[0],
                label="Select Database",
                choices=databases_choices,
                type="value",
            )

        with gr.Column(scale=8):
            query_editor = gr.TextArea(
                label="🗒️ Query Editor",
                interactive=True,
                placeholder="Enter query here...",
                elem_id="query-editor",
            )
            run_query = gr.Button(
                value="▶️ Run Query",
                size="sm",
                variant="primary",
            )
            result_table = gr.DataFrame(label="Output", value=None)

    run_query.click(
        fn=execute_query,
        inputs=[query_editor],
        outputs=[result_table],
    )
    databases.change(fn=change_database, inputs=[databases], outputs=[])

if __name__ == "__main__":
    demo.launch()
