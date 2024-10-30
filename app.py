# app.py
import pandas as pd
import plotly.express as px
from dash import Dash, html, dcc, callback, Input, Output
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
df = pd.read_excel("ENEMDados2023.xlsx", engine='openpyxl')

# Criar dicionários para mapear os códigos para descrições
mapa_sexo = {
    'M': 'Masculino',
    'F': 'Feminino'
}

mapa_cor_raca = {
    0: 'Não declarado',
    1: 'Branca',
    2: 'Preta',
    3: 'Parda',
    4: 'Amarela',
    5: 'Indígena',
    6: 'Não dispõe de informação'
}

# Converter os códigos para descrições
df['Sexo'] = df['TP_SEXO'].map(mapa_sexo)
df['Cor/Raça'] = df['TP_COR_RACA'].map(mapa_cor_raca)

# Função para criar o gráfico de sexo
def create_sex_graph(selected_sex='Todos'):
    if selected_sex == 'Todos':
        filtered_df = df
    else:
        filtered_df = df[df['Sexo'] == selected_sex]
    
    df_graph = filtered_df['Sexo'].value_counts().reset_index()
    df_graph.columns = ['Sexo', 'Quantidade']
    
    fig = px.bar(
        df_graph,
        x='Sexo',
        y='Quantidade',
        title=f'Distribuição de Candidatos por Sexo - ENEM 2023 ({selected_sex})',
        color='Sexo',
        color_discrete_map={'Masculino': '#2E86C1', 'Feminino': '#E74C3C'},
        text='Quantidade'
    )
    
    fig.update_traces(textposition='outside')
    fig.update_layout(
        xaxis_title="Sexo",
        yaxis_title="Número de Candidatos",
        showlegend=False,
        plot_bgcolor='white',
        paper_bgcolor='white',
        font=dict(size=12)
    )
    
    return fig

# Função para criar o gráfico de cor/raça
def create_race_graph(selected_sex='Todos'):
    if selected_sex == 'Todos':
        filtered_df = df
    else:
        filtered_df = df[df['Sexo'] == selected_sex]
    
    df_graph = filtered_df['Cor/Raça'].value_counts().reset_index()
    df_graph.columns = ['Cor/Raça', 'Quantidade']
    
    # Cores personalizadas para cada categoria
    color_map = {
        'Não declarado': '#808080',
        'Branca': '#E6E6E6',
        'Preta': '#2C3E50',
        'Parda': '#C4A484',
        'Amarela': '#FFD700',
        'Indígena': '#8B4513',
        'Não dispõe de informação': '#D3D3D3'
    }
    
    fig = px.bar(
        df_graph,
        x='Cor/Raça',
        y='Quantidade',
        title=f'Distribuição de Candidatos por Cor/Raça - ENEM 2023 ({selected_sex})',
        color='Cor/Raça',
        color_discrete_map=color_map,
        text='Quantidade'
    )
    
    fig.update_traces(textposition='outside')
    fig.update_layout(
        xaxis_title="Cor/Raça",
        yaxis_title="Número de Candidatos",
        showlegend=True,
        plot_bgcolor='white',
        paper_bgcolor='white',
        font=dict(size=12),
        xaxis={'tickangle': 45}
    )
    
    return fig

# Layout da aplicação
app.layout = html.Div(
    children=[
        # Header com as imagens
        html.Div(
            className='header',
            children=[
                html.Img(
                    src='/assets/ENEM.png',
                    style={
                        'height': '100px',
                        'marginRight': '20px'
                    }
                ),
                html.H1(
                    children='Análise de Candidatos do ENEM 2023',
                    style={
                        'textAlign': 'center',
                        'color': '#2C3E50',
                        'marginTop': '20px',
                        'marginBottom': '20px',
                        'fontFamily': 'Arial, sans-serif',
                        'flex': '1'
                    }
                ),
                html.Img(
                    src='/assets/Univesp.png',
                    style={
                        'height': '100px',
                        'marginLeft': '20px'
                    }
                ),
            ],
            style={
                'display': 'flex',
                'justifyContent': 'center',
                'alignItems': 'center',
                'padding': '20px'
            }
        ),
        html.Div(
            children='''Visualização da distribuição dos candidatos por Sexo e Cor/Raça no ENEM 2023''',
            style={
                'textAlign': 'center',
                'color': '#7F8C8D',
                'marginBottom': '30px'
            }
        ),
        # Dropdown para seleção do sexo
        html.Div(
            children=[
                html.Label(
                    'Selecione o Sexo:',
                    style={
                        'marginRight': '10px',
                        'fontWeight': 'bold',
                        'color': '#2C3E50'
                    }
                ),
                dcc.Dropdown(
                    id='sex-dropdown',
                    options=[
                        {'label': 'Todos', 'value': 'Todos'},
                        {'label': 'Masculino', 'value': 'Masculino'},
                        {'label': 'Feminino', 'value': 'Feminino'}
                    ],
                    value='Todos',
                    style={
                        'width': '200px'
                    }
                )
            ],
            style={
                'display': 'flex',
                'justifyContent': 'center',
                'alignItems': 'center',
                'marginBottom': '20px'
            }
        ),
        # Gráficos
        html.Div([
            dcc.Graph(
                id='grafico-sexo',
                figure=create_sex_graph(),
                style={'height': '500px'}
            ),
            dcc.Graph(
                id='grafico-raca',
                figure=create_race_graph(),
                style={'height': '500px'}
            )
        ])
    ],
    style={
        'padding': '20px',
        'backgroundColor': '#F8F9F9'
    }
)

# Callbacks para atualizar os gráficos quando o dropdown for alterado
@callback(
    [Output('grafico-sexo', 'figure'),
     Output('grafico-raca', 'figure')],
    Input('sex-dropdown', 'value')
)
def update_graphs(selected_sex):
    return create_sex_graph(selected_sex), create_race_graph(selected_sex)

# Configuração do servidor
server = app.server

if __name__ == '__main__':
    app.run_server(debug=False, host='0.0.0.0', port=8080)
