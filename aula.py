from dash import Dash, html, dcc, Input, Output
import plotly.express as px
import pandas as pd

# Inicialização do app - aqui estava o primeiro erro
app = Dash(__name__)  # Era app.Dash que está incorreto

# Leitura do arquivo
df = pd.read_excel("Vendas.xlsx")

# Criando o gráfico
fig = px.bar(df, x="Produto", y="Quantidade", color="ID Loja", barmode="group")

# Criando lista de opções para o dropdown
opcoes = list(df['ID Loja'].unique())
opcoes.append("Todas as lojas")

app.layout = html.Div(children=[
    html.H1(children='Faturamento das Lojas'),
    html.H2(children='Gráfico com o faturamento de Todos os Produtos separados por Loja'),
    html.Div(children='''
        Obs: Esse gráfico mostra a quantidade de produtos vendidos, não o faturamento.
    '''),
    dcc.Dropdown(opcoes, value='Todas as lojas', id='lista_lojas'),
    dcc.Graph(
        id='grafico_quantidade_vendas',
        figure=fig
    )
])

@app.callback(
    Output('grafico_quantidade_vendas', 'figure'),
    Input('lista_lojas', 'value')
)
def update_output(value):
    if value == "Todas as lojas":
        fig = px.bar(df, x="Produto", y="Quantidade", color="ID Loja", barmode="group")
    else:
        tabela_filtrada = df.loc[df['ID Loja']==value, :]
        fig = px.bar(tabela_filtrada, x="Produto", y="Quantidade", color="ID Loja", barmode="group")
    return fig

# Definição do server para o Gunicorn
server = app.server

# Correção na condição if __name__ (estava com ** ao invés de __)
if __name__ == '__main__':
    app.run(debug=True)
