from dash import Dash, html, dcc, Input, Output
import plotly.express as px
import pandas as pd

# Inicialização do app - aqui estava o primeiro erro
app = Dash(__name__)  # Era app.Dash que está incorreto

# Leitura do arquivo
df = pd.read_excel("ENEMDados2023.xls")

# Criando o gráfico
#fig = px.bar(df, x="Produto", y="Quantidade", color="ID Loja", barmode="group")
fig = px.bar(
    df['TP_SEXO'].value_counts().reset_index(),
    x='index',
    y='TP_SEXO',
    title='Distribuição de Candidatos por Sexo - ENEM 2023',
    labels={'index': 'Sexo', 'TP_SEXO': 'Número de Candidatos'},
    color='index',
    text='TP_SEXO'
)

# Criando lista de opções para o dropdown
opcoes = list(df['TP_SEXO'].unique())
opcoes.append("Todos os Sexos")
#opcoes.append("Todas as lojas")

fig.update_traces(textposition='outside')
fig.update_layout(
    xaxis_title="Sexo",
    yaxis_title="Número de Candidatos",
    showlegend=False
)

app.layout = html.Div(children=[
    html.H1(children='Análise de Gênero dos Candidatos do ENEM 2023',
            style={'textAlign': 'center', 'color': '#503D36', 'marginBottom': 30}
           ),
    
#    html.H2(children='Gráfico com o faturamento de Todos os Produtos separados por Loja'),
#    html.Div(children='''
#        Obs: Esse gráfico mostra a quantidade de produtos vendidos, não o faturamento.
#    '''),
    html.Div(children='''
        Distribuição dos candidatos por sexo no ENEM 2023
    ''', style={'textAlign': 'center', 'marginBottom': 30}),

#    dcc.Dropdown(opcoes, value='Todas as lojas', id='lista_lojas'),
    dcc.Dropdown(opcoes, value='Todos os Sexos', id='lista_sexo'),
    dcc.Graph(
#        id='grafico_quantidade_vendas',
        id='grafico_sexo',
        figure=fig
    )
])

@app.callback(
    Output('grafico_sexo', 'figure'),
    Input('lista_sexo', 'value')
)
def update_output(value):
#    if value == "Todas as lojas":
    if value == "Todos os Sexos":
#        fig = px.bar(df, x="Produto", y="Quantidade", color="ID Loja", barmode="group")
##        fig = px.bar(df, x="Produto", y="Quantidade", color="ID Loja", barmode="group")
        fig = px.bar(df['TP_SEXO'].value_counts().reset_index(), x='index', y='TP_SEXO', title='Distribuição de Candidatos por Sexo - ENEM 2023', labels={'index': 'Sexo', 'TP_SEXO': 'Número de Candidatos'}, color='index', text='TP_SEXO')
    else:
#        tabela_filtrada = df.loc[df['ID Loja']==value, :]
        tabela_filtrada = df.loc[df['TP_SEXO']==value, :]
#        fig = px.bar(tabela_filtrada, x="Produto", y="Quantidade", color="ID Loja", barmode="group")
        fig = px.bar(tabela_filtrada, df['TP_SEXO'].value_counts().reset_index(), x='index', y='TP_SEXO', title='Distribuição de Candidatos por Sexo - ENEM 2023', labels={'index': 'Sexo', 'TP_SEXO': 'Número de Candidatos'}, color='index', text='TP_SEXO')

    return fig

# Definição do server para o Gunicorn não alterar a partir daqui
server = app.server

if __name__ == '__main__':
    app.run(debug=True)
