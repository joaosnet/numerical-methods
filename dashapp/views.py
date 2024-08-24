# Importando as bibliotecas necessárias
from dash import html, dcc, Input, Output, State, dash_table
from dashapp import app
import dash_dangerously_set_inner_html
import numpy as np
import sympy as sp
from sympy.parsing.latex import parse_latex
from metodos import metodos_numericos

# Definindo o estilo da tabela de dados
DATA_TABLE_STYLE = {
    "style_data_conditional": [
        {
            "if": {"filter_query": "{Sinal a} = negativo", "column_id": "a"},
            "backgroundColor": "#800000",
            "color": "white",
        },
        {
            "if": {"filter_query": "{Sinal a} = positivo", "column_id": "a"},
            "backgroundColor": "#ADD8E6",  # Azul claro
            "color": "black",
        },
        {
            "if": {"filter_query": "{Sinal b} = negativo", "column_id": "b"},
            "backgroundColor": "#800000",
            "color": "white",
        },
        {
            "if": {"filter_query": "{Sinal b} = positivo", "column_id": "b"},
            "backgroundColor": "#ADD8E6",  # Azul claro
            "color": "black",
        },
        {
            "if": {
                "filter_query": "{Sinal x} = negativo",
                "column_id": "Aproximação da Raiz",
            },
            "backgroundColor": "#800000",
            "color": "white",
        },
        {
            "if": {
                "filter_query": "{Sinal x} = positivo",
                "column_id": "Aproximação da Raiz",
            },
            "backgroundColor": "#ADD8E6",  # Azul claro
            "color": "black",
        },
    ],
    "style_header": {
        "color": "white",
        "backgroundColor": "#799DBF",
        "fontWeight": "bold",
    },
    "css": [
        {
            "selector": ".Select-value",
            "rule": "padding-right: 22px",
        },  # makes space for the dropdown caret
        {"selector": ".dropdown", "rule": "position: static"},  # makes dropdown visible
    ],
}

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
        html.Div(
            children=[
                html.Label("Intervalo:"),
            ]
        ),
        html.Br(),
        html.Div(
            [
                html.Br(),
                dcc.Input(id="min-value", type="number", value=-2),
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
                    allowCross=False,
                ),
                dcc.Input(id="max-value", type="number", value=5),
                # html.Br(),
            ],
            style={
                "display": "grid",
                "grid-template-columns": r"10% 10% 60% 10%",
                "align-items": "center",
            },
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
        dcc.Input(id="interacoes", type="number", value=100, min=3, max=100, step=1),
        html.Hr(),
        html.Br(),
        html.Label("Tolerância:"),
        dcc.Input(
            id="tolerancia", type="number", value=1e-18, min=1e-18, max=100, step=1
        ),
        html.Hr(),
        html.Br(),
        html.Button("Calcular", id="calcular-bissecao", n_clicks=0),
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
        html.Div(
            id="falsap-container",
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


# Callback para atualizar o RangeSlider com base nos inputs
@app.callback(
    Output("intervalo", "min"),
    Output("intervalo", "max"),
    Input("min-value", "value"),
    Input("max-value", "value"),
)
def update_rangeslider(min_value, max_value):
    return min_value, max_value


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
        disp=False,
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
        html.H5(
            children="Tabela de interções usando Método da Bisseção"
        ),  # Título do método
        dcc.Markdown(
            "{resultado}".format(resultado=resultado),
            mathjax=True,
            style={"font-size": "14pt"},
        ),
        html.Hr(),
        html.Div(children="Tabela de Iterações:"),
        dash_table.DataTable(
            df.to_dict("records"),
            [{"name": i, "id": i, "hideable": True} for i in df.columns],
            hidden_columns=["Sinal a", "Sinal b", "Sinal x"],
            id="table",
            sort_action="native",
            style_table={"height": "300px", "overflowY": "auto"},
            editable=False,
            dropdown={
                "Resource": {
                    "clearable": False,
                    "options": [{"label": i, "value": i} for i in ["A", "B", "C", "D"]],
                },
            },
            css=DATA_TABLE_STYLE.get("css"),
            page_size=10,
            row_deletable=True,
            style_data_conditional=DATA_TABLE_STYLE.get("style_data_conditional"),
            style_header=DATA_TABLE_STYLE.get("style_header"),
        ),
    ]


# Chamada para calcular o Método da Falsa Posição
@app.callback(
    Output("falsap-container", "children"),
    Input("calcular-bissecao", "n_clicks"),
    State("intervalo", "value"),
    State("funcao", "value"),
    State("interacoes", "value"),
    State("tolerancia", "value"),
)
def calcular_false_position(n_clicks, intervalo, funcao, interacoes, tolerancia):
    funcao, funcao_simbolica = tratar_funcao(funcao)
    # inicializando a classe metodos_numericos
    mn = metodos_numericos()
    # tratando a função que está em string para uma função que o python entenda
    falsaposicao_obj = mn.falsaposicao_modificada(
        intervalo[0],
        intervalo[1],
        funcao,
        imax=interacoes,
        es=tolerancia,
    )  # Aumenta o número máximo de iterações
    df = mn.get_df()  # Move a definição de df para fora do bloco try/except
    funcao_latex1 = funcao_latex(funcao_simbolica)
    try:
        x = falsaposicao_obj
        iteracoes = mn.get_iteracoes()
        resultado = f"A raiz da função ${funcao_latex1}$ no intervalo [{intervalo[0]}, {intervalo[1]}] é {x} com {iteracoes} iterações."
    except RuntimeError as e:
        resultado = f"O método da falsa posição não convergiu após {interacoes} iterações. Erro: {e}"

    return [
        html.H5(
            children="Tabela de interções usando Método da falsa posição ou interpolação"
        ),  # Título do método
        dcc.Markdown(
            "{resultado}".format(resultado=resultado),
            mathjax=True,
            style={"font-size": "14pt"},
        ),
        html.Hr(),
        html.Div(children="Tabela de Iterações:"),
        dash_table.DataTable(
            df.to_dict("records"),
            [{"name": i, "id": i, "hideable": True} for i in df.columns],
            hidden_columns=["Sinal a", "Sinal b", "Sinal x"],
            id="table",
            sort_action="native",
            style_table={"height": "300px", "overflowY": "auto"},
            editable=False,
            dropdown={
                "Resource": {
                    "clearable": False,
                    "options": [{"label": i, "value": i} for i in ["A", "B", "C", "D"]],
                },
            },
            css=DATA_TABLE_STYLE.get("css"),
            page_size=10,
            row_deletable=True,
            style_data_conditional=DATA_TABLE_STYLE.get("style_data_conditional"),
            style_header=DATA_TABLE_STYLE.get("style_header"),
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
    bissecao = mn.bissecao(
        intervalo[0],
        intervalo[1],
        funcao,
        maxiter=interacoes,
        disp=False,
    )
    raiz = bissecao
    falsa_posicao_raiz = mn.falsaposicao_modificada(
        intervalo[0], intervalo[1], funcao, imax=interacoes
    )
    funcao_latex1 = funcao_latex(funcao_simbolica)
    return {
        "data": [
            {"x": x, "y": y, "type": "scatter", "name": "Função"},
            {
                "x": [raiz],
                "y": [0],
                "mode": "markers",
                "name": "Raiz Bisseção",
                "marker": {"size": 10, "color": "red"},
            },
            {
                "x": [falsa_posicao_raiz],
                "y": [0],
                "mode": "markers",
                "name": "Raiz Falsa Posição",
                "marker": {"size": 10, "color": "green"},
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
