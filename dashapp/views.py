# Importando as bibliotecas necessárias
from dash import html, dcc, Input, Output, State, dash_table
from dashapp import app

import numpy as np
import sympy as sp
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
                max=5,
                step=0.5,
                value=[0, 1],
                marks={i: str(i) for i in range(-10, 11)},
                tooltip={"placement": "top", "always_visible": True},
                pushable=True,
                # definindo o tamanho do slider
                updatemode="drag",
            ),
            html.Br(),
            html.Label("Função:"),
            dcc.Input(id="funcao", type="text", value="np.sin(x) - 0.5"),
            html.Hr(),
            html.Br(),
            html.Label("Interações:"),
            dcc.Input(id="interacoes", type="number", value=100, min=3, max=100, step=1),
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
                dcc.Graph(id="graph", mathjax=True),
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
        funcao_sym = sp.sympify(funcao)
        funcao_latex = sp.latex(funcao_sym)
    except:  # noqa: E722
        funcao_latex = funcao
    try:
        x = Bissecao_obj
        iteracoes = mn.get_iteracoes()
        resultado = f"A raiz da função ${funcao_latex}$ no intervalo [{intervalo[0]}, {intervalo[1]}] é {x} com {iteracoes} iterações."
    except RuntimeError as e:
        resultado = (
            f"O método da bisseção não convergiu após {interacoes} iterações. Erro: {e}"
        )

    return [
        html.H5(children="Método da Bisseção"),  # Título do método
        dcc.Markdown(
            "{resultado}".format(resultado=resultado),
            mathjax=True,
            style={"font-size": "14pt"},
        ),
        html.Hr(),
        html.Div(children="Tabela de Iterações:"),
        dash_table.DataTable(
            df.to_dict("records"),
            [{"name": i, "id": i} for i in df.columns],
            id="table",
            page_size=10,
        ),
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
    try:
        funcao_sym = sp.sympify(funcao)
        funcao_latex = sp.latex(funcao_sym)
    except:  # noqa: E722
        funcao_latex = funcao
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
            "title": "Gráfico da função ${}$".format(funcao_latex),
            "xaxis": {"title": "x"},
            "yaxis": {"title": "f(x)"},
        },
    }
