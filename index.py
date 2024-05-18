import dash
from dash import html, dcc
from dash.dependencies import Input, Output
import pandas as pd
import numpy as np
import plotly.express as px
import dash_bootstrap_components as dbc
from dash_bootstrap_templates import load_figure_template


# instanciando o dash
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.MINTY])
server = app.server

# etl
df_data = pd.read_csv("supermarket_sales.csv")
df_data["Date"] = pd.to_datetime(df_data["Date"])

# definindo o layout
list_cities = df_data["City"].unique()

app.layout = html.Div(children=[
    dbc.Row([      
        dbc.Col([
            dbc.Card([
                html.H2("DOM", style={"text-align": "center"}),
                html.Hr(),

                html.H6("Cidades: "),
                dcc.Checklist(options=[{'label': city, 'value': city} for city in list_cities], inline=True, 
                              id="check_city", inputStyle={"margin-right": "20px"}),
            
                html.H6("Variável de Análise: ", style={"margin-top": "20px"}),
                dcc.RadioItems(["gross income", "Rating"], "gross income", inline=True, id="main_variable",
                               inputStyle={"margin-right": "20px"}),
                
            ], style={"height": "90vh", "margin": "10px", "padding": "10px"}),

        ], sm=2),

        dbc.Col([
            dbc.Row([
                dbc.Col([dcc.Graph(id="city_fig")], sm=4),
                dbc.Col([dcc.Graph(id="gender_fig")], sm=4),
                dbc.Col([dcc.Graph(id="pay_fig")], sm=4)
            ]),
            dbc.Row([dcc.Graph(id="income_per_data_fig")]),
            dbc.Row([dcc.Graph(id="income_per_product_fig")]),
        ], sm=10),
    ]), 
])

# callback
@app.callback(
    [Output('city_fig', 'figure'),
     Output('pay_fig', 'figure'),
     Output('gender_fig', 'figure'),
     Output('income_per_data_fig', 'figure'),
     Output('income_per_product_fig', 'figure')],
    [Input('check_city', 'value'),
     Input('main_variable', 'value')]
)
def render_graph(cities, main_variable):

    if not cities:
        cities = list_cities  # Se nenhuma cidade for selecionada, mostrar todas
    operation = np.sum if main_variable == "gross income" else np.mean
    df_filtered = df_data[df_data["City"].isin(cities)]
    
    # Gráfico por cidade
    df_city = df_filtered.groupby("City")[main_variable].apply(operation).reset_index()
    city_fig = px.bar(df_city, x="City", y=main_variable, title=f"{main_variable.capitalize()} por Cidade")

    # Gráfico por gênero
    df_gender = df_filtered.groupby("Gender")[main_variable].apply(operation).reset_index()
    gender_fig = px.bar(df_gender, x="Gender", y=main_variable, title=f"{main_variable.capitalize()} por Gênero")

    # Gráfico de pagamento
    df_payment = df_filtered.groupby("Payment")[main_variable].apply(operation).reset_index()
    pay_fig = px.bar(df_payment, x="Payment", y=main_variable, title=f"{main_variable.capitalize()} por Tipo de Pagamento")

    # Gráfico de receita por data
    df_date = df_filtered.groupby("Date")[main_variable].apply(operation).reset_index()
    income_per_data_fig = px.line(df_date, x="Date", y=main_variable, title=f"{main_variable.capitalize()} ao longo do Tempo")

    # Gráfico de receita por produto
    df_product = df_filtered.groupby(["Product line", "Customer type"])[main_variable].apply(operation).reset_index()
    income_per_product_fig = px.bar(
        df_product,
        x=main_variable,
        y="Product line",
        color="Customer type",
        orientation='h',
        title=f"{main_variable.capitalize()} por Linha de Produto e Tipo de Cliente"
    )

    # for fig in [city_fig, pay_fig, gender_fig, income_per_data_fig, income_per_product_fig]:
    #     fig.update_layout(margin=dict(l=0, r=0, t=20, b=20), heinth=200)
    
    # fig.update_layout(margin=dict(l=0, r=0, t=20, b=20), heinth=500)
    
    return city_fig, pay_fig, gender_fig, income_per_data_fig, income_per_product_fig

# Rodando o servidor
if __name__ == "__main__":
    app.run_server(debug=True)

