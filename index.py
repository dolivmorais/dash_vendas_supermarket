from dash import Dash, html, dcc
from dash.dependencies import Input, Output
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# instanciando o dash
app = Dash(__name__)
server = app.server

# etl
df_data = pd.read_csv("supermarket_sales.csv")
df_data["Date"] = pd.to_datetime(df_data["Date"])

# definindo o layout
list_cities = df_data["City"].unique()

app.layout = html.Div(children=[
    html.H1("Cidades: "),
    dcc.Checklist(options=[{'label': city, 'value': city} for city in list_cities], inline=True, id="check_city"),
    
    html.H5("Variável de Análise: "),
    dcc.RadioItems(["gross income", "Rating"], "gross income", inline=True, id="main_variable"),
    
    dcc.Graph(id="city_fig"),
    dcc.Graph(id="pay_fig"),
    dcc.Graph(id="income_per_product_fig")
])

# callback
@app.callback(
    [Output('city_fig', 'figure'),
     Output('pay_fig', 'figure'),
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

    # Gráfico de pagamento
    df_payment = df_filtered.groupby("Payment")[main_variable].apply(operation).reset_index()
    pay_fig = px.bar(df_payment, x="Payment", y=main_variable, title=f"{main_variable.capitalize()} por Tipo de Pagamento")

    # Gráfico de receita por produto
    df_product = df_filtered.groupby("Product line")[main_variable].apply(operation).reset_index()
    income_per_product_fig = px.bar(df_product, x="Product line", y=main_variable, title=f"{main_variable.capitalize()} por Linha de Produto")

    return city_fig, pay_fig, income_per_product_fig

# Rodando o servidor
if __name__ == "__main__":
    app.run_server(debug=True)
