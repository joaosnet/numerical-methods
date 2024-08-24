# Importando as bibliotecas necessárias
from dash import html, dcc, Input, Output, State, dash_table
from dashapp import app
import dash_dangerously_set_inner_html
import numpy as np
import sympy as sp
from sympy.parsing.latex import parse_latex
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
                step=0.1,
                value=[0, 1],
                marks={i: str(i) for i in range(-10, 11)},
                tooltip={"placement": "top", "always_visible": True},
                pushable=True,
                # definindo o tamanho do slider
                updatemode="drag",
            ),
            html.Br(),
            html.Label("Função:"),
            html.Div(
                [
                    dash_dangerously_set_inner_html.DangerouslySetInnerHTML(r"""
                        <math-field id="mathlive-input" placeholder="e.g. x^2 - 2">\exponentialE^{-x}-x</math-field>
                    """),
                ],
                id="mathlive-container",
            ),
            html.Label("Confirme abaixo se a função está correta apertando espaço:"),
            dcc.Input(
                id="funcao",
                type="text",
                value=r"\exponentialE^{-x}-x",
            ),
            html.Hr(),
            html.Br(),
            html.Label("Interações:"),
            dcc.Input(
                id="interacoes", type="number", value=100, min=3, max=100, step=1
            ),
            html.Hr(),
            html.Br(),
            html.Label("Tolerância:"),
            dcc.Input(
                id="tolerancia", type="number", value=1e-18, min=1e-18, max=100, step=1
            ),
            html.Hr(),
            html.Br(),
            html.Button("Calcular", id="calcular-bissecao", n_clicks=0),
        ]),
    ],  # Descrição do aplicativo
)

# Coluna Esquerda
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


# Função para tratar da funcao recebida do math-input
def tratar_funcao(funcao):
    try:
        x = sp.symbols("x")

        # Expressão em LaTeX
        expressao_latex = funcao

        if r"\exponentialE" in expressao_latex:
            expressao_latex = expressao_latex.replace(r"\exponentialE", r"\exp\left")
            # Corrigir os parênteses
            expressao_latex = expressao_latex.replace(r"^{-", r"(-")
            expressao_latex = expressao_latex.replace(r"}", r"\right)")

        # Convertendo a expressão LaTeX para uma expressão simbólicaS
        expressao_simbolica = parse_latex(expressao_latex)

        # Convertendo a expressão simbólica para uma função lambda do Python
        funcao_lambda = sp.lambdify(x, expressao_simbolica, "numpy")
        return funcao_lambda, expressao_simbolica
    except Exception as e:
        print(f"Erro ao tratar a função: {e}")
        return lambda x: eval(funcao)


def funcao_latex(expressao_simbolica):
    try:
        funcao_latex = sp.latex(expressao_simbolica)
    except Exception as e:
        print(f"Erro ao converter para LaTeX: {e}")
        funcao_latex = str(expressao_simbolica)
    return funcao_latex


# pathname
@app.callback(Output("conteudo_pagina", "children"), Input("url", "pathname"))
def carregar_pagina(pathname):
    if pathname == "/":
        return layout_dashboard


# Calculando a bisseção
@app.callback(
    Output("tabs", "children"),
    Input("calcular-bissecao", "n_clicks"),
    State("intervalo", "value"),
    State("funcao", "value"),
    State("interacoes", "value"),
    State("tolerancia", "value"),
)
def calcular_bissecao(n_clicks, intervalo, funcao, interacoes, tolerancia):
    funcao, funcao_simbolica = tratar_funcao(funcao)
    # inicializando a classe metodos_numericos
    mn = metodos_numericos()
    # tratando a função que está em string para uma função que o python entenda
    Bissecao_obj = mn.bissecao(
        intervalo[0],
        intervalo[1],
        funcao,
        maxiter=interacoes,
        tol=tolerancia,
    )  # Aumenta o número máximo de iterações
    df = mn.get_df()  # Move a definição de df para fora do bloco try/except
    funcao_latex1 = funcao_latex(funcao_simbolica)
    try:
        x = Bissecao_obj
        iteracoes = mn.get_iteracoes()
        resultado = f"A raiz da função ${funcao_latex1}$ no intervalo [{intervalo[0]}, {intervalo[1]}] é {x} com {iteracoes} iterações."
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
    funcao, funcao_simbolica = tratar_funcao(funcao)
    # inicializando a classe metodos_numericos
    mn = metodos_numericos()
    # tratando a função que está em string para uma função que o python entenda
    x = np.linspace(intervalo[0], intervalo[1], 100)
    y = funcao(x)

    # Calcular a raiz usando o método da bisseção
    bissecao = mn.bissecao(intervalo[0], intervalo[1], funcao)
    raiz = bissecao
    funcao_latex1 = funcao_latex(funcao_simbolica)
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
            "title": "Gráfico da função ${}$".format(funcao_latex1),
            "xaxis": {"title": "x"},
            "yaxis": {"title": "f(x)"},
        },
    }


# Callback client-side para atualizar o valor do input 'funcao' com o valor do 'math-field'
app.clientside_callback(
    """
    function(children) {
        const mathField = document.getElementById('mathlive-input');
        if (mathField) {
            mathField.addEventListener('input', () => {
                const input = document.getElementById('funcao');
                if (input) {
                    input.value = mathField.getValue('latex');
                }
            });
        }
        return children;
    }
    """,
    Output("mathlive-container", "children"),
    Input("mathlive-container", "children"),
)
