# app.py
import pandas as pd
import plotly.express as px
from dash import Dash, html, dcc
from flask import Flask

# Criar o servidor Flask
server = Flask(__name__)

# Configurar o Dash
app = Dash(__name__, server=server, suppress_callback_exceptions=True)

# Configuração para evitar o erro before_first_request
@server.before_request
def before_first_request():
    pass

# Ler o arquivo do ENEM
df = pd.read_excel("ENEMDados2023.xls", engine='xlrd')

# Criar um dicionário para mapear os códigos para descrições
mapa_sexo = {
    'M': 'Masculino',
    'F': 'Feminino'
}

# Converter os códigos para descrições
df['Sexo'] = df['TP_SEXO'].map(mapa_sexo)

# Criar o DataFrame para o gráfico
df_graph = df['Sexo'].value_counts().reset_index()
df_graph.columns = ['Sexo', 'Quantidade']  # Renomeando as colunas

# Criar o gráfico de barras
fig = px.bar(
    df_graph,
    x='Sexo',
    y='Quantidade',
    title='Distribuição de Candidatos por Sexo - ENEM 2023',
    color='Sexo',
    color_discrete_map={'Masculino': '#2E86C1', 'Feminino': '#E74C3C'},
    text='Quantidade'
)

# Atualizar layout do gráfico
fig.update_traces(textposition='outside')
fig.update_layout(
    xaxis_title="Sexo",
    yaxis_title="Número de Candidatos",
    showlegend=False,
    plot_bgcolor='white',
    paper_bgcolor='white',
    font=dict(size=12)
)

# Layout da aplicação
app.layout = html.Div(
    children=[
        html.H1(
        html.Img(src=dash.get_asset_url('ENEM.png'))
    ],
    style={
        'padding': '20px',
        'backgroundColor': '#F8F9F9'}
)
    
        html.H1(
            children='Análise de Gênero dos Candidatos do ENEM 2023',
            style={
                'textAlign': 'center',
                'color': '#2C3E50',
                'marginTop': '20px',
                'marginBottom': '20px',
                'fontFamily': 'Arial, sans-serif'
            }
        ),
        html.Div(
            children='''Visualização da distribuição dos candidatos por sexo no ENEM 2023''',
            style={
                'textAlign': 'center',
                'color': '#7F8C8D',
                'marginBottom': '30px'
            }
        ),
        dcc.Graph(
            id='grafico-sexo',
            figure=fig,
            style={'height': '600px'}
        )
    ],
    style={
        'padding': '20px',
        'backgroundColor': '#F8F9F9'
    }
)

# Configuração do servidor
server = app.server

if __name__ == '__main__':
    app.run_server(debug=False, host='0.0.0.0', port=8080)
