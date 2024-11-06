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

mapa_estado_civil = {
    0: 'Não informado',
    1: 'Solteiro(a)',
    2: 'Casado(a)/Mora com companheiro(a)',
    3: 'Divorciado(a)/Desquitado(a)/Separado(a)',
    4: 'Viúvo(a)'
}

# Converter os códigos para descrições
df['Sexo'] = df['TP_SEXO'].map(mapa_sexo)
df['Cor/Raça'] = df['TP_COR_RACA'].map(mapa_cor_raca)
df['Estado Civil'] = df['TP_ESTADO_CIVIL'].map(mapa_estado_civil)

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

# Função para criar o gráfico de cor/raça (modificada para pizza)
def create_race_graph(selected_sex='Todos'):
    if selected_sex == 'Todos':
        filtered_df = df
    else:
        filtered_df = df[df['Sexo'] == selected_sex]
    
    df_graph = filtered_df['Cor/Raça'].value_counts().reset_index()
    df_graph.columns = ['Cor/Raça', 'Quantidade']
    
    # Calcular percentuais
    total = df_graph['Quantidade'].sum()
    df_graph['Percentual'] = (df_graph['Quantidade'] / total * 100).round(2)
    
    color_map = {
        'Não declarado': '#808080',
        'Branca': '#E6E6E6',
        'Preta': '#2C3E50',
        'Parda': '#C4A484',
        'Amarela': '#FFD700',
        'Indígena': '#8B4513',
        'Não dispõe de informação': '#D3D3D3'
    }
    
    fig = px.pie(
        df_graph,
        values='Quantidade',
        names='Cor/Raça',
        title=f'Distribuição de Candidatos por Cor/Raça - ENEM 2023 ({selected_sex})',
        color='Cor/Raça',
        color_discrete_map=color_map,
        hover_data=['Percentual'],
        custom_data=['Quantidade', 'Percentual']
    )
    
    # Atualizar o texto mostrado no gráfico
    fig.update_traces(
        textposition='inside',
        textinfo='label+percent',
        hovertemplate="<b>%{label}</b><br>" +
                     "Quantidade: %{customdata[0]:,.0f}<br>" +
                     "Percentual: %{customdata[1]:.2f}%<br>"
    )
    
    fig.update_layout(
        showlegend=True,
        plot_bgcolor='white',
        paper_bgcolor='white',
        font=dict(size=12),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.2,
            xanchor="center",
            x=0.5
        ),
        margin=dict(t=80, b=120, l=60, r=60)
    )
    
    return fig

# Função para criar o gráfico de estado civil (modificada para barras)
def create_civil_status_graph(selected_sex='Todos'):
    if selected_sex == 'Todos':
        filtered_df = df
    else:
        filtered_df = df[df['Sexo'] == selected_sex]
    
    df_graph = filtered_df['Estado Civil'].value_counts().reset_index()
    df_graph.columns = ['Estado Civil', 'Quantidade']
    
    # Cores personalizadas para estado civil
    color_map = {
        'Não informado': '#808080',
        'Solteiro(a)': '#3498DB',
        'Casado(a)/Mora com companheiro(a)': '#2ECC71',
        'Divorciado(a)/Desquitado(a)/Separado(a)': '#E74C3C',
        'Viúvo(a)': '#9B59B6'
    }
    
    fig = px.bar(
        df_graph,
        x='Estado Civil',
        y='Quantidade',
        title=f'Distribuição de Candidatos por Estado Civil - ENEM 2023 ({selected_sex})',
        color='Estado Civil',
        color_discrete_map=color_map,
        text='Quantidade'
    )
    
    fig.update_traces(textposition='outside')
    fig.update_layout(
        xaxis_title="Estado Civil",
        yaxis_title="Número de Candidatos",
        showlegend=False,
        plot_bgcolor='white',
        paper_bgcolor='white',
        font=dict(size=12),
        xaxis={'tickangle': 45}
    )
    
    return fig

def create_age_histogram(selected_sex='Todos'):
    if selected_sex == 'Todos':
        filtered_df = df
    else:
        filtered_df = df[df['Sexo'] == selected_sex]

    # Criar os bins para as faixas etárias
    bins = [-1, 18, 21, 25, 30, 40, 50, 60, 70, float('inf')]
    labels = ['Menor de 18 anos', 'Menor de 18 anos', 'Entre 18 e 21 anos', 'Entre 22 e 25 anos',
              'Entre 26 e 30 anos', 'Entre 31 e 40 anos', 'Entre 41 e 50 anos', 'Entre 51 e 60 anos',
              'Entre 61 e 70 anos', 'Maior de 70 anos']

    # Aplicar a classificação por faixa etária
    filtered_df['Faixa Etária'] = pd.cut(filtered_df['TP_FAIXA_ETARIA'], bins=bins, labels=labels)

    # Contar a quantidade de candidatos por faixa etária
    age_counts = filtered_df['Faixa Etária'].value_counts().reset_index()
    age_counts.columns = ['Faixa Etária', 'Quantidade']

    # Criar o gráfico de histograma
    fig = px.bar(
        age_counts,
        x='Faixa Etária',
        y='Quantidade',
        title=f'Distribuição de Candidatos por Faixa Etária - ENEM 2023 ({selected_sex})',
        color='Faixa Etária',
        color_discrete_map={
            'Menor de 18 anos': '#3498DB',
            'Entre 18 e 21 anos': '#2ECC71',
            'Entre 22 e 25 anos': '#E74C3C',
            'Entre 26 e 30 anos': '#9B59B6',
            'Entre 31 e 40 anos': '#F1C40F',
            'Entre 41 e 50 anos': '#A569BD',
            'Entre 51 e 60 anos': '#5499C7',
            'Entre 61 e 70 anos': '#45B39D',
            'Maior de 70 anos': '#D35400'
        },
        text='Quantidade'
    )

    fig.update_traces(textposition='outside')
    fig.update_layout(
        xaxis_title="Faixa Etária",
        yaxis_title="Número de Candidatos",
        showlegend=False,
        plot_bgcolor='white',
        paper_bgcolor='white',
        font=dict(size=12)
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
            children='''Visualização da distribuição dos candidatos por Sexo, Cor/Raça e Estado Civil no ENEM 2023''',
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
            ),
            dcc.Graph(
                id='grafico-estado-civil',
                figure=create_civil_status_graph(),
                style={'height': '500px'}
            ),
           dcc.Graph(
                id='grafico-idade',
                figure=create_age_histogram(),
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
     Output('grafico-raca', 'figure'),
     Output('grafico-estado-civil', 'figure'),
     Output('grafico-idade', 'figure')],
    Input('sex-dropdown', 'value')
)
def update_graphs(selected_sex):
    return create_sex_graph(selected_sex), create_race_graph(selected_sex), create_civil_status_graph(selected_sex), create_age_histogram(selected_sex)

# Configuração do servidor
server = app.server

if __name__ == '__main__':
    app.run_server(debug=False, host='0.0.0.0', port=8080)
