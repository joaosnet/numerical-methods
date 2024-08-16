# Importando as bibliotecas necessárias
from dash import html, dcc, Input, Output, State
from dashapp import app

# from werkzeug.utils import secure_filename
import numpy as np
from metodos import metodos_numericos

# Definindo a coluna esquerda
left_column = html.Div(
    id="left-column",
    className="four columns",
    children=[
        html.H5(children="Métodos Numéricos"),  # Título do aplicativo
        html.Div(
            children="""Seja bem-vindo ao aplicativo de métodos numéricos! Aqui você poderá visualizar os métodos numéricos implementados e o gráfico."""
        ),
        html.Hr(),
        html.Div(
            children="""Adicione um intervalo e uma função para visualizar o método da bisseção:"""
        ),
        html.Div([
            html.Label("Intervalo:"),
            html.Br(),
            dcc.RangeSlider(
                id="intervalo",
                min=-2,
                max=2,
                step=0.5,
                value=[0, 1],
                marks={i: str(i) for i in range(-10, 11)},
            ),
            html.Br(),
            html.Label("Função:"),
            dcc.Input(id="funcao", type="text", value="32*x**2 - 68*x + 21"),
            html.Hr(),
            html.Br(),
            html.Label("Interações:"),
            dcc.Input(id="interacoes", type="number", value=3, min=3, max=100, step=1),
            html.Hr(),
            html.Br(),
            html.Button("Calcular", id="calcular-bissecao", n_clicks=0),
        ]),
    ],  # Descrição do aplicativo
)

right_column = html.Div(
    id="right-column",
    className="eight columns",
    children=[
        html.Div(
            children=[
                html.Hr(),
                dcc.Graph(id="graph"),
            ],
        ),
        html.Div(
            id="tabs",
            children=[],
        ),
    ],
)

# Layout do Dashboard Principal
layout_dashboard = html.Div(
    id="app-container",
    children=[
        # Coluna esquerda
        left_column,
        # Coluna direita
        right_column,
    ],
)

# Definindo o layout do aplicativo
app.layout = html.Div([
    dcc.Location(id="url", refresh=False),
    # Banner
    html.Div(
        id="banner",
        children=[
            html.Img(src=app.get_asset_url("fotos_site/logo.png")),
            # html.H1("Dashapp"),
            html.Div(id="navbar"),
        ],
        className="banner",
    ),
    html.Div(id="conteudo_pagina"),
])


# pathname
@app.callback(Output("conteudo_pagina", "children"), Input("url", "pathname"))
def carregar_pagina(pathname):
    if pathname == "/":
        if True:
            return layout_dashboard
        else:
            return dcc.Link(
                "Usuário não autenticado, faça login aqui", "/login", refresh=True
            )


# Calculando a bisseção
@app.callback(
    Output("tabs", "children"),
    Input("calcular-bissecao", "n_clicks"),
    State("intervalo", "value"),
    State("funcao", "value"),
    State("interacoes", "value"),
)
def calcular_bissecao(n_clicks, intervalo, funcao, interacoes):
    # inicializando a classe metodos_numericos
    mn = metodos_numericos()
    # tratando a função que está em string para uma função que o python entenda
    Bissecao_obj = mn.bissecao(
        intervalo[0], intervalo[1], lambda x: eval(funcao), maxiter=interacoes
    )  # Aumenta o número máximo de iterações
    df = mn.get_df()  # Move a definição de df para fora do bloco try/except
    try:
        x = Bissecao_obj
        iteracoes = mn.get_iteracoes()
        resultado = f"A raiz da função {funcao} no intervalo [{intervalo[0]}, {intervalo[1]}] é {x} com {iteracoes} iterações."
    except RuntimeError as e:
        resultado = (
            f"O método da bisseção não convergiu após {interacoes} iterações. Erro: {e}"
        )

    return [
        html.H5(children="Método da Bisseção"),  # Título do método
        html.Div(children=resultado),  # Resultado do método
        html.Hr(),
        html.Div(children="Tabela de Iterações:"),
        html.Table([
            html.Thead([html.Tr([html.Th(col) for col in df.columns])]),
            html.Tbody([
                html.Tr([html.Td(df.iloc[i][col]) for col in df.columns])
                for i in range(len(df))
            ]),
        ]),
    ]


# Atualizando o gráfico
@app.callback(
    Output("graph", "figure"),
    Input("calcular-bissecao", "n_clicks"),
    State("intervalo", "value"),
    State("funcao", "value"),
    State("interacoes", "value"),
)
def atualizar_grafico(n_clicks, intervalo, funcao, interacoes):
    # inicializando a classe metodos_numericos
    mn = metodos_numericos()
    # tratando a função que está em string para uma função que o python entenda
    x = np.linspace(intervalo[0], intervalo[1], 100)
    y = eval(funcao.replace("x", "x"))

    # Calcular a raiz usando o método da bisseção
    bissecao = mn.bissecao(
        intervalo[0], intervalo[1], lambda x: eval(funcao.replace("x", "x"))
    )
    raiz = bissecao

    return {
        "data": [
            {"x": x, "y": y, "type": "scatter", "name": "Função"},
            {
                "x": [raiz],
                "y": [0],
                "mode": "markers",
                "name": "Raiz",
                "marker": {"size": 10, "color": "red"},
            },
        ],
        "layout": {
            "title": f"Gráfico da função {funcao}",
            "xaxis": {"title": "x"},
            "yaxis": {"title": "f(x)"},
        },
    }
