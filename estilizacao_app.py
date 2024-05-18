import dash
from dash import html, dcc
from dash.dependencies import Input, Output
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import dash_bootstrap_components as dbc

app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server


card_content = [
    dbc.CardHeader("Card header"),
    dbc.CardBody(
        [
            html.H5("Card title", className="card-title"),
            html.P(
                "This is some card content that we'll reuse",
                className="card-text",
            ),
        ]
    ),
]


app.layout = html.Div([
    dbc.Row([
        dbc.Col([
            dbc.Card(card_content, color="primary", inverse=True, style={"height": "90vh", "margin": "10px"}),
        ], sm=4),

        dbc.Col([
            dbc.Row([
                dbc.Col(dbc.Card(card_content, color="info", inverse=True, style={"margin": "10px"})),
                dbc.Col(dbc.Card(card_content, color="info", inverse=True, style={"margin": "10px"})),
                ]),
            dbc.Row([
                dbc.Col(dbc.Card(card_content, color="warning", inverse=True)),
                dbc.Col(dbc.Card(card_content, color="warning", inverse=True)),
                dbc.Col(dbc.Card(card_content, color="warning", inverse=True)),
                ]),
            ]),
        ]),
    ])

if __name__ == "__main__":
    app.run_server(port=8050, debug=True)