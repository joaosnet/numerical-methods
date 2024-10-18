# Importando as bibliotecas necessárias
from dash import html, dcc, Input, Output, State, dash_table
from dashapp import app
import dash_dangerously_set_inner_html
import numpy as np
import sympy as sp
from sympy.parsing.latex import parse_latex
from metodos import (
    bissecao,
    falsaposicao_modificada,
    iteracao_linear,
    newton_raphson,
    secant_method,
)
import dash_mantine_components as dmc
from dash_iconify import DashIconify
import plotly.graph_objects as go
from gaussian_elimination import gauss
import array_to_latex as a2l
import traceback
import pandas as pd
from metodos_range_kutta import solve_ode, create_plots, create_table
from dash_resizable_panels import Panel, PanelGroup, PanelResizeHandle

# Definindo o estilo da tabela de dados
DATA_TABLE_STYLE = {
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
    # className="four columns",
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
            id="tolerancia",
            type="number",
            value=1e-18,
            min=1e-18,
            max=100,
            step=0.0000001,
        ),
        html.Hr(),
        html.Br(),
        html.Button("Calcular", id="calcular-bissecao", n_clicks=0),
    ],  # Descrição do aplicativo
)

# Coluna Esquerda
right_column = html.Div(
    id="right-column",
    children=[
        dcc.Store(id="df-Bissec"),
        dcc.Store(id="df-Falsa"),
        dmc.Tabs(
            [
                dmc.TabsList(
                    [
                        dmc.TabsTab("Bisseção", value="bissecao"),
                        dmc.TabsTab("Falsa Posição", value="falsa_posicao"),
                        dmc.TabsTab("Comparações entre Métodos", value="comparacoes"),
                        dmc.TabsTab("Método da Iteração Linear (Ponto Fixo)", value="ponto_fixo"),
                        dmc.TabsTab("Método de Newton-Raphson", value="newton"),
                        dmc.TabsTab("Método da Secante", value="secante"),
                        dmc.TabsTab("Eliminação de Gauss", value="gauss"),
                        dmc.TabsTab("Método de Runge-Kutta de 3ª Ordem e 4ª Ordem", value="runge_kutta"),
                    ]
                ),
                dmc.TabsPanel(
                    children=[],
                    id="bissecao",
                    value="bissecao",
                ),
                dmc.TabsPanel(
                    children=[],
                    id="falsap-tab",
                    value="falsa_posicao",
                ),
                dmc.TabsPanel(
                    children=[
                        html.Div(id="tabela_bissec", children=[]),
                        html.Div(id="tabela_falsa", children=[]),
                    ],
                    value="comparacoes",
                ),
                dmc.TabsPanel(
                    children=[],
                    id="ponto_fixo",
                    value="ponto_fixo",
                ),
                dmc.TabsPanel(
                    children=[],
                    id="newton",
                    value="newton",
                ),
                dmc.TabsPanel(
                    children=[],
                    id="secant",
                    value="secante",
                ),
                dmc.TabsPanel(
                    children=[
                        html.Div(
                            id="gauss_controls",
                            children=[
                                dcc.Store(id="memory-matrix"),
                                html.Hr(),
                                html.Br(),
                                dcc.Input(
                                    id="matrix-input",
                                    type="text",
                                    value="[[2, 4, 3, 4, 8],[5, 8, 7, 8, 8],[9, 13, 11, 12, 7],[2, 3, 2, 5, 6],]",
                                ),
                                dcc.Markdown(id="matrix-preview", mathjax=True),
                                html.Hr(),
                                html.Br(),
                                html.Button(
                                    "Resolver Matriz", id="resolver_matriz", n_clicks=0
                                ),
                            ],
                            style={
                                "display": "flex",
                                "flex-direction": "column",
                                "align-items": "center",
                                "justify-content": "center",
                            },
                        ),
                        html.Div(
                            id="Markdown",
                            children=[],
                        ),
                    ],
                    value="gauss",
                ),
                dmc.TabsPanel(
                    children=[
                        PanelGroup(
                            direction="horizontal",
                            children=[
                                Panel(
                                    id="panel-1",
                                    style={"padding": "10px"},
                                    defaultSizePercentage=85,
                                    children=[
                                        html.Div(
                                            children=[
                                                html.Div(id="rk-output"),
                                            ],
                                        ),
                                    ],
                                ),
                                PanelResizeHandle(
                                    html.Div(
                                        style={
                                            "backgroundColor": "white",
                                            "height": "100%",
                                            "width": "5px",
                                        }
                                    )
                                ),
                                Panel(
                                    id="panel-2",
                                    children=[
                                        html.Div(
                                            children=[
                                                html.H1("Método de Runge-Kutta de 3ª Ordem e 4ª Ordem"),
                                                html.Label(
                                                    "Equação Diferencial (em termos de x e y):"
                                                ),
                                                html.Div(
                                                    [
                                                        dash_dangerously_set_inner_html.DangerouslySetInnerHTML(r"""
                                                    <math-field id="rk-mathlive-input" style="width: 100%;">4*exp(0.8*x) - 0.5*y</math-field>
                                                """),
                                                    ],
                                                    id="rk-mathlive-container",
                                                ),
                                                dcc.Input(
                                                    id="rk-equation",
                                                    type="text",
                                                    value="4*exp(0.8*x) - 0.5*y",
                                                    style={"width": "50%"},
                                                ),
                                                html.Br(),
                                                html.Label("Valor inicial de x:"),
                                                dcc.Input(
                                                    id="rk-x0", type="number", value=0
                                                ),
                                                html.Br(),
                                                html.Label("Valor inicial de y:"),
                                                dcc.Input(
                                                    id="rk-y0", type="number", value=2
                                                ),
                                                html.Br(),
                                                html.Label("Valor final de x:"),
                                                dcc.Input(
                                                    id="rk-xf", type="number", value=4
                                                ),
                                                html.Br(),
                                                html.Label(
                                                    "Tamanho dos passos h (separados por vírgula):"
                                                ),
                                                dcc.Input(
                                                    id="rk-h",
                                                    type="text",
                                                    value="1, 0.1, 0.01",
                                                ),
                                                html.Br(),
                                                html.Button(
                                                    "Calcular",
                                                    id="calcular-rk",
                                                    n_clicks=0,
                                                ),
                                            ],
                                        ),
                                    ],
                                ),
                            ],
                        )
                    ],
                    value="runge_kutta",
                ),
            ],
            id="tabs-methods",
            value="bissecao",
        ),
    ],
)

# Layout do Dashboard Principal
layout_dashboard = html.Div(
    id="app-container",
    children=[
        # Coluna esquerda
        # left_column,
        # Coluna direita
        right_column,
    ],
)

theme_toggle = dmc.ActionIcon(
    [
        dmc.Paper(DashIconify(icon="radix-icons:sun", width=25), darkHidden=True),
        dmc.Paper(DashIconify(icon="radix-icons:moon", width=25), lightHidden=True),
    ],
    variant="transparent",
    color="yellow",
    id="color-scheme-toggle",
    size="lg",
    ms="auto",
)

# Cabecalho da aplicação
header = dmc.Group(
    [
        dmc.Burger(id="burger-button", opened=False, hiddenFrom="md"),
        html.Img(src=app.get_asset_url("fotos_site/logo.png"), width=40),
        dmc.Text(["DashBoard para Métodos Númericos"], size="xl", fw=700),
        theme_toggle,
    ],
    justify="flex-start",
)

navbar = (
    dmc.ScrollArea(
        [left_column],
        h="100%",
        w="100%",
        offsetScrollbars=True,
        type="scroll",
    ),
)

layout_pagina = html.Div(
    children=[
        dcc.Location(id="url", refresh=False),
        html.Div(id="conteudo_pagina"),
    ],
)

appshell = dmc.AppShell(
    [
        dmc.AppShellHeader(header, px=25),
        dmc.AppShellNavbar(navbar, p=24),
        # dmc.AppShellAside("Aside", withBorder=False),
        dmc.AppShellMain(layout_pagina),
        # dmc.AppShellFooter("Footer"),
    ],
    header={"height": 70},
    padding="xl",
    navbar={
        "width": 800,
        "breakpoint": "md",
        "collapsed": {"mobile": True},
    },
    # aside={
    #     "width": 300,
    #     "breakpoint": "xl",
    #     "collapsed": {"desktop": False, "mobile": False, "tablet": False},
    # },
    id="app-shell",
)

# Definindo o layout do aplicativo
app.layout = dmc.MantineProvider(
    [dcc.Store(id="theme-store", storage_type="local", data="light"), appshell],
    id="mantine-provider",
    forceColorScheme="light",
)


@app.callback(
    Output("rk-output", "children"),
    Input("calcular-rk", "n_clicks"),
    State("rk-equation", "value"),
    State("rk-x0", "value"),
    State("rk-y0", "value"),
    State("rk-xf", "value"),
    State("rk-h", "value"),
)
def calcular_runge_kutta(n_clicks, equation, x0, y0, xf, h_values):
    try:
        sp.Symbol("x")
        sp.Symbol("y")
        func_expr = sp.sympify(equation)
        h_values = [float(h.strip()) for h in h_values.split(",")]
        x0 = float(x0)
        y0 = float(y0)
        xf = float(xf)

        results, x_analytic, y_analytic = solve_ode(func_expr, x0, y0, xf, h_values)
        fig = create_plots(results, x_analytic, y_analytic, func_str=str(func_expr))

        # Criar tabela de resultados
        df = create_table(results)

        return [
            dcc.Graph(figure=fig),
            dash_table.DataTable(
                data=df.to_dict("records"),
                columns=[{"name": i, "id": i} for i in df.columns],
                style_table={"height": "300px", "overflowY": "auto"},
                page_size=20,
            ),
        ]
    except Exception as e:
        return html.Div(f"Erro: {str(e)}")


# Callback client-side para atualizar o valor do input rk-equation com o valor do rk-mathlive-input
app.clientside_callback(
    """
    function(children) {
        const mathField = document.getElementById('rk-mathlive-input');
        if (mathField) {
            mathField.addEventListener('input', () => {
                const input = document.getElementById('rk-equation');
                if (input) {
                    input.value = mathField.getValue('latex');
                }
            });
        }
        return children;
    }
    """,
    Output("rk-mathlive-container", "children"),
    Input("rk-mathlive-container", "children"),
)


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
        # Expressão em LaTeX
        expressao_latex = funcao

        if r"\exponentialE" in expressao_latex:
            expressao_latex = expressao_latex.replace(r"\exponentialE", r"\exp\left")
            # Corrigir os parênteses
            expressao_latex = expressao_latex.replace(r"^{-", r"(-")
            expressao_latex = expressao_latex.replace(r"}", r"\right)")

        # Convertendo a expressão LaTeX para uma expressão simbólicaS
        expressao_simbolica = parse_latex(expressao_latex)

        x = sp.symbols("x")
        # Convertendo a expressão simbólica para uma função lambda do Python
        funcao_lambda = sp.lambdify(x, expressao_simbolica, modules=["numpy"])
        # import inspect

        # print(inspect.getsource(funcao_lambda))
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


# Chamada para calcular o metodo da bisseção e armazenar o dataframe
@app.callback(
    Output("df-Bissec", "data"),
    Input("calcular-bissecao", "n_clicks"),
    State("intervalo", "value"),
    State("funcao", "value"),
    State("interacoes", "value"),
    State("tolerancia", "value"),
)
def calcular_bissecao(n_clicks, intervalo, funcao, interacoes, tolerancia):
    funcao, _funcao_simbolica = tratar_funcao(funcao)

    try:
        df = bissecao(
            intervalo[0],
            intervalo[1],
            funcao,
            maxiter=interacoes,
            tol=tolerancia,
            disp=False,
        )  # Aumenta o número máximo de iterações
        return df.to_dict("records")
    except Exception as e:
        return [f"Erro ao calcular a bisseção.{e}"]


# Chamada para colocar a tabela de iterações na aba de bisseção
@app.callback(
    Output("bissecao", "children"),
    Input("df-Bissec", "data"),
    State("intervalo", "value"),
    State("funcao", "value"),
)
def tab_bissecao(df, intervalo, funcao):
    _, funcao_simbolica = tratar_funcao(funcao)
    df = pd.DataFrame(df)
    x = df["Aproximação da Raiz"].iloc[-1]
    iteracoes = len(df)
    # tratando a função que está em string para uma função que o python entenda
    try:
        funcao_latex1 = funcao_latex(funcao_simbolica)
        resultado = f"A raiz da função ${funcao_latex1}$ no intervalo [{intervalo[0]}, {intervalo[1]}] é {x} com {iteracoes} iterações."
        fig = grafico_animado(intervalo, funcao, df, "Bisseção")
        # renomeando os cabeçalhos das colunas
        df = df.rename(
            columns={
                "a": "Limite Inferior (xl)",
                "b": "Limite Superior (xu)",
                "Aproximação da Raiz": "Aproximação da Raiz (xr)",
                "Erro Relativo (%)": "Erro Relativo (%)",
                "Sinal a": "Sinal a",
                "Sinal b": "Sinal b",
                "Sinal x": "Sinal x",
            }
        )

        # adicionando a coluna da iteração como a primeira coluna
        df.insert(0, "Iteração", range(1, len(df) + 1))

        return html.Div(
            children=[
                html.Div(
                    children=[
                        html.Hr(),
                        dcc.Graph(figure=fig, id="graph", mathjax=True),
                    ],
                ),
                html.Div(
                    children=[
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
                            [
                                {"name": i, "id": i, "hideable": True}
                                for i in df.columns
                            ],
                            hidden_columns=["Sinal a", "Sinal b", "Sinal x"],
                            id="table",
                            sort_action="native",
                            style_table={"height": "300px", "overflowY": "auto"},
                            editable=False,
                            dropdown={
                                "Resource": {
                                    "clearable": False,
                                    "options": [
                                        {"label": i, "value": i}
                                        for i in ["A", "B", "C", "D"]
                                    ],
                                },
                            },
                            css=DATA_TABLE_STYLE.get("css"),
                            page_size=10,
                            row_deletable=True,
                            style_data_conditional=[
                                {
                                    "if": {
                                        "filter_query": "{Sinal a} = negativo",
                                        "column_id": "Limite Inferior (xl)",
                                    },
                                    "backgroundColor": "#800000",
                                    "color": "white",
                                },
                                {
                                    "if": {
                                        "filter_query": "{Sinal a} = positivo",
                                        "column_id": "Limite Inferior (xl)",
                                    },
                                    "backgroundColor": "#ADD8E6",  # Azul claro
                                    "color": "black",
                                },
                                {
                                    "if": {
                                        "filter_query": "{Sinal b} = negativo",
                                        "column_id": "Limite Superior (xu)",
                                    },
                                    "backgroundColor": "#800000",
                                    "color": "white",
                                },
                                {
                                    "if": {
                                        "filter_query": "{Sinal b} = positivo",
                                        "column_id": "Limite Superior (xu)",
                                    },
                                    "backgroundColor": "#ADD8E6",  # Azul claro
                                    "color": "black",
                                },
                                {
                                    "if": {
                                        "filter_query": "{Sinal x} = negativo",
                                        "column_id": "Aproximação da Raiz (xr)",
                                    },
                                    "backgroundColor": "#800000",
                                    "color": "white",
                                },
                                {
                                    "if": {
                                        "filter_query": "{Sinal x} = positivo",
                                        "column_id": "Aproximação da Raiz (xr)",
                                    },
                                    "backgroundColor": "#ADD8E6",  # Azul claro
                                    "color": "black",
                                },
                            ],
                            style_header=DATA_TABLE_STYLE.get("style_header"),
                        ),
                    ],
                ),
            ]
        )
    except Exception as e:
        # traceback.print_exc()
        resultado = f"O método da bisseção não convergiu após {iteracoes} iterações. Por que {e}"

        return html.Div(
            [
                html.H5(
                    children="Tabela de interções usando Método da Bisseção"
                ),  # Título do método
                dcc.Markdown(
                    "{resultado}".format(resultado=resultado),
                    mathjax=True,
                    style={"font-size": "14pt"},
                ),
            ]
        )


# Chamada para calcular o metodo da falsa posição e armazenar o dataframe
@app.callback(
    Output("df-Falsa", "data"),
    Input("calcular-bissecao", "n_clicks"),
    State("intervalo", "value"),
    State("funcao", "value"),
    State("interacoes", "value"),
    State("tolerancia", "value"),
)
def calcular_falsa(_clicks, intervalo, funcao, interacoes, tolerancia):
    funcao, _funcao_simbolica = tratar_funcao(funcao)

    try:
        df = falsaposicao_modificada(
            intervalo[0],
            intervalo[1],
            funcao,
            imax=interacoes,
            es=tolerancia,
        )  # Aumenta o número máximo de iterações
        return df.to_dict("records")
    except Exception as e:
        return [f"Erro ao calcular a falsa posição.{e}"]


# Chamada para colocar a tabela de iterações na aba de Falsa Posição
@app.callback(
    Output("falsap-tab", "children"),
    Input("df-Falsa", "data"),
    State("intervalo", "value"),
    State("funcao", "value"),
)
def tab_falsaposicao(df, intervalo, funcao):
    _, funcao_simbolica = tratar_funcao(funcao)
    df = pd.DataFrame(df)
    x = df["Aproximação da Raiz (xr)"].iloc[-1]
    iteracoes = len(df)
    # tratando a função que está em string para uma função que o python entenda
    try:
        funcao_latex1 = funcao_latex(funcao_simbolica)
        resultado = f"A raiz da função ${funcao_latex1}$ no intervalo [{intervalo[0]}, {intervalo[1]}] é {x} com {iteracoes} iterações."

        fig = grafico_animado(intervalo, funcao, df, "Falsa Posição")

        return html.Div(
            children=[
                html.Div(
                    children=[
                        html.Hr(),
                        dcc.Graph(figure=fig, mathjax=True),
                    ],
                ),
                html.Div(
                    children=[
                        html.H5(
                            children="Tabela de interções usando Método da Falsa Posição"
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
                            [
                                {"name": i, "id": i, "hideable": True}
                                for i in df.columns
                            ],
                            id="table",
                            sort_action="native",
                            style_table={"height": "300px", "overflowY": "auto"},
                            editable=False,
                            dropdown={
                                "Resource": {
                                    "clearable": False,
                                    "options": [
                                        {"label": i, "value": i}
                                        for i in ["A", "B", "C", "D"]
                                    ],
                                },
                            },
                            css=DATA_TABLE_STYLE.get("css"),
                            page_size=10,
                            row_deletable=True,
                            style_header=DATA_TABLE_STYLE.get("style_header"),
                        ),
                    ],
                ),
            ]
        )
    except Exception as e:
        # traceback.print_exc()
        resultado = f"O método da Falsa Posição não convergiu após {iteracoes} iterações. Por que {e}"

        return html.Div(
            [
                html.H5(
                    children="Tabela de interções usando Método da Falsa Posição"
                ),  # Título do método
                dcc.Markdown(
                    "{resultado}".format(resultado=resultado),
                    mathjax=True,
                    style={"font-size": "14pt"},
                ),
            ]
        )


def grafico_animado(intervalo, funcao, df, saida):
    try:
        funcao, funcao_simbolica = tratar_funcao(funcao)
        funcao_latex1 = funcao_latex(funcao_simbolica)

        x = np.linspace(intervalo[0], intervalo[1], 100)
        y = funcao(x)

        # Criar a figura inicial
        fig_dict = {"data": [], "layout": {}, "frames": []}

        # Configurar o layout
        # adicionado o título do gráfico
        fig_dict["layout"]["title"] = (
            "$\\text{Método da " + saida + " para a função} " + funcao_latex1 + "$"
        )
        fig_dict["layout"]["xaxis"] = {
            "range": [intervalo[0], intervalo[1]],
            "title": "x",
        }
        fig_dict["layout"]["yaxis"] = {"title": "f(x)"}
        fig_dict["layout"]["hovermode"] = "closest"
        # tornando a legenda flutuante
        fig_dict["layout"]["legend"] = {
            "x": 1,
            "y": 1,
            "xanchor": "right",
            "yanchor": "top",
        }
        fig_dict["layout"]["updatemenus"] = [
            {
                "buttons": [
                    {
                        "args": [
                            None,
                            {
                                "frame": {"duration": 500, "redraw": False},
                                "fromcurrent": True,
                                "transition": {
                                    "duration": 300,
                                    "easing": "quadratic-in-out",
                                },
                            },
                        ],
                        "label": "Play",
                        "method": "animate",
                    },
                    {
                        "args": [
                            [None],
                            {
                                "frame": {"duration": 0, "redraw": False},
                                "mode": "immediate",
                                "transition": {"duration": 0},
                            },
                        ],
                        "label": "Pause",
                        "method": "animate",
                    },
                ],
                "direction": "left",
                "pad": {"r": 10, "t": 87},
                "showactive": False,
                "type": "buttons",
                "x": 0.1,
                "xanchor": "right",
                "y": 0,
                "yanchor": "top",
            }
        ]

        sliders_dict = {
            "active": 0,
            "yanchor": "top",
            "xanchor": "left",
            "currentvalue": {
                "font": {"size": 20},
                "prefix": "Iteração:",
                "visible": True,
                "xanchor": "right",
            },
            "transition": {"duration": 300, "easing": "cubic-in-out"},
            "pad": {"b": 10, "t": 50},
            "len": 0.9,
            "x": 0.1,
            "y": 0,
            "steps": [],
        }

        # Adicionar a função ao gráfico inicial
        fig_dict["data"].append(
            go.Scatter(
                x=[intervalo[0], intervalo[1]],
                y=[0, 0],
                mode="markers",
                name="Intervalo [a, b]",
            )
        )
        fig_dict["data"].append(
            go.Scatter(x=[0], y=[0], mode="markers", name="Aproximação da Raiz")
        )
        fig_dict["data"].append(go.Scatter(x=x, y=y, mode="lines", name="Função"))

        # Calcular as iterações e adicionar os frames
        if saida == "Bisseção":
            for i, row in df.iterrows():
                frame = {"data": [], "name": str(i)}
                frame["data"].append(
                    go.Scatter(
                        x=[row["a"], row["b"]],
                        y=[0, 0],
                        mode="markers",
                        name="Intervalo [a, b]",
                    )
                )
                frame["data"].append(
                    go.Scatter(
                        x=[row["Aproximação da Raiz"]],
                        y=[0],
                        mode="markers",
                        name="Aproximação da Raiz",
                        marker=dict(color="red", size=10),
                    )
                )
                # Adicionar linhas verticais para os intervalos [a, b] e a aproximação da raiz
                frame["layout"] = {
                    "shapes": [
                        dict(
                            type="line",
                            x0=row["a"],
                            y0=min(y),
                            x1=row["a"],
                            y1=max(y),
                            line=dict(color="blue", width=2),
                            line_dash="dash",
                            line_width=3,
                        ),
                        dict(
                            type="line",
                            x0=row["b"],
                            y0=min(y),
                            x1=row["b"],
                            y1=max(y),
                            line=dict(color="blue", width=2),
                            line_dash="dash",
                            line_width=3,
                        ),
                    ]
                }
                fig_dict["frames"].append(frame)
                slider_step = {
                    "args": [
                        [i],
                        {
                            "frame": {"duration": 300, "redraw": False},
                            "mode": "immediate",
                            "transition": {"duration": 300},
                        },
                    ],
                    "label": i,
                    "method": "animate",
                }
                sliders_dict["steps"].append(slider_step)

        elif saida == "Falsa Posição":
            for i, row in df.iterrows():
                frame = {"data": [], "name": str(i)}
                # Reta da Falsa Posição
                frame["data"].append(
                    go.Scatter(
                        x=[
                            row["Início do Intervalo (xl)"],
                            row["Final do Intervalo (xu)"],
                        ],
                        y=[row["f(xl)"], row["f(xu)"]],
                        mode="lines",
                        name="Intervalo [a, b]",
                    )
                )

                frame["data"].append(
                    go.Scatter(
                        x=[row["Aproximação da Raiz (xr)"]],
                        y=[0],
                        mode="markers",
                        name="Aproximação da Raiz",
                        marker=dict(color="red", size=10),
                    )
                )

                fig_dict["frames"].append(frame)
                slider_step = {
                    "args": [
                        [i],
                        {
                            "frame": {"duration": 300, "redraw": False},
                            "mode": "immediate",
                            "transition": {"duration": 300},
                        },
                    ],
                    "label": i,
                    "method": "animate",
                }
                sliders_dict["steps"].append(slider_step)

        elif saida == "Ponto Fixo":
            #proximo frame
            for i, row in df.iterrows():
                frame = {"data": [], "name": str(i)}
                frame["data"].append(
                    go.Scatter(
                        x=[row["x"]],
                        y=[funcao(row["x"])],
                        mode="markers",
                        name="Aproximação da Raiz",
                        marker=dict(color="red", size=10),
                    )
                )
                frame["data"].append(
                    go.Scatter(
                        x=[row["x"], row["x"]],
                        y=[0, funcao(row["x"])],
                        mode="lines",
                        name="Linha de Convergência",
                        line=dict(color="green", width=2),
                    )
                )
                fig_dict["frames"].append(frame)
                slider_step = {
                    "args": [
                        [i],
                        {
                            "frame": {"duration": 300, "redraw": False},
                            "mode": "immediate",
                            "transition": {"duration": 300},
                        },
                    ],
                    "label": i,
                    "method": "animate",
                }
                sliders_dict["steps"].append(slider_step)
        elif saida == "Newton-Raphson":
            for i, row in df.iterrows():
                frame = {"data": [], "name": str(i)}
                x_i = row["Aproximação da Raiz (x_i)"]
                y_i = funcao(x_i)
                
                # Ponto da iteração atual
                frame["data"].append(
                    go.Scatter(
                        x=[x_i],
                        y=[y_i],
                        mode="markers",
                        name=f"Iteração {i}",
                        marker=dict(color="red", size=10),
                    )
                )
                
                # Linha tangente
                if i < len(df) - 1:
                    x_next = df.loc[i+1, "Aproximação da Raiz (x_i)"]
                    slope = (funcao(x_next) - y_i) / (x_next - x_i)
                    x_tangent = np.linspace(x_i - 0.5, x_i + 0.5, 100)
                    y_tangent = slope * (x_tangent - x_i) + y_i
                    frame["data"].append(
                        go.Scatter(
                            x=x_tangent,
                            y=y_tangent,
                            mode="lines",
                            name="Tangente",
                            line=dict(color="green", width=2, dash="dash"),
                        )
                    )
                
                fig_dict["frames"].append(frame)
                slider_step = {
                    "args": [
                        [i],
                        {
                            "frame": {"duration": 300, "redraw": False},
                            "mode": "immediate",
                            "transition": {"duration": 300},
                        },
                    ],
                    "label": i,
                    "method": "animate",
                }
                sliders_dict["steps"].append(slider_step)

        elif saida == "Secante":
            for i, row in df.iterrows():
                frame = {"data": [], "name": str(i)}
                x_i = row["Aproximação da Raiz (x_i)"]
                y_i = funcao(x_i)
                
                # Ponto da iteração atual
                frame["data"].append(
                    go.Scatter(
                        x=[x_i],
                        y=[y_i],
                        mode="markers",
                        name=f"Iteração {i}",
                        marker=dict(color="red", size=10),
                    )
                )
                
                # Linha secante
                if i < len(df) - 1:
                    x_next = df.loc[i+1, "Aproximação da Raiz (x_i)"]
                    y_next = funcao(x_next)
                    frame["data"].append(
                        go.Scatter(
                            x=[x_i, x_next],
                            y=[y_i, y_next],
                            mode="lines",
                            name="Secante",
                            line=dict(color="purple", width=2, dash="dash"),
                        )
                    )
                
                fig_dict["frames"].append(frame)
                slider_step = {
                    "args": [
                        [i],
                        {
                            "frame": {"duration": 300, "redraw": False},
                            "mode": "immediate",
                            "transition": {"duration": 300},
                        },
                    ],
                    "label": i,
                    "method": "animate",
                }
                sliders_dict["steps"].append(slider_step)

        fig_dict["layout"]["sliders"] = [sliders_dict]

        fig = go.Figure(fig_dict)
        return fig
    except Exception as e:
        # removendo o gráfico e retornando nada
        if "Não há raiz no intervalo fornecido." in str(e):
            traceback.print_exc()
            return Exception
        elif (
            "Não há mudança de sinal no intervalo fornecido. O método da falsa posição requer que f(xl) e f(xu) tenham sinais opostos."
            in str(e)
        ):
            traceback.print_exc()
            return Exception
        else:
            traceback.print_exc()
            return Exception


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


# TODO: Chamando os callbacks abrir a navbar
@app.callback(
    Output("app-shell", "navbar"),
    Input("burger-button", "opened"),
    State("app-shell", "navbar"),
)
def navbar_is_open(opened, navbar):
    navbar["collapsed"] = {"mobile": not opened}
    return navbar


@app.callback(
    Output("app-shell", "navbar", allow_duplicate=True),
    Input("tabs-methods", "value"),
    State("app-shell", "navbar"),
    prevent_initial_call=True,
)
def navbar_is_closed(tab, navbar):
    if tab == "gaus":
        navbar["collapsed"] = {"desktop": True, "mobile": True}
    elif tab == "runge_kutta":
        navbar["collapsed"] = {"desktop": True, "mobile": True}
    else:
        navbar["collapsed"] = {"desktop": False, "mobile": True}
    return navbar


@app.callback(
    Output("mantine-provider", "forceColorScheme"),
    Input("color-scheme-toggle", "n_clicks"),
    State("mantine-provider", "forceColorScheme"),
    prevent_initial_call=True,
)
def switch_theme(_, theme):
    return "dark" if theme == "light" else "light"


# TODO: Chamando os callbacks novamente para a comparação entre os métodos
# Chamada para colocar a tabela de iterações na aba de bisseção
@app.callback(
    Output("tabela_bissec", "children"),
    Input("df-Bissec", "data"),
    State("intervalo", "value"),
    State("funcao", "value"),
    State("interacoes", "value"),
    State("tolerancia", "value"),
)
def tab_comp_bissecao_tabela(df, intervalo, funcao, interacoes, tolerancia):
    df = pd.DataFrame(df)
    _, funcao_simbolica = tratar_funcao(funcao)
    f = funcao_latex(funcao_simbolica)
    resultado = f"A raiz da função ${f}$ no intervalo [{intervalo[0]}, {intervalo[1]}] é {df['Aproximação da Raiz'].iloc[-1]} com {len(df)} iterações."
    return (
        html.Div(
            children=[
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
                            "options": [
                                {"label": i, "value": i} for i in ["A", "B", "C", "D"]
                            ],
                        },
                    },
                    css=DATA_TABLE_STYLE.get("css"),
                    page_size=10,
                    row_deletable=True,
                    style_data_conditional=[
                        {
                            "if": {
                                "filter_query": "{Sinal a} = negativo",
                                "column_id": "Limite Inferior (xl)",
                            },
                            "backgroundColor": "#800000",
                            "color": "white",
                        },
                        {
                            "if": {
                                "filter_query": "{Sinal a} = positivo",
                                "column_id": "Limite Inferior (xl)",
                            },
                            "backgroundColor": "#ADD8E6",  # Azul claro
                            "color": "black",
                        },
                        {
                            "if": {
                                "filter_query": "{Sinal b} = negativo",
                                "column_id": "Limite Superior (xu)",
                            },
                            "backgroundColor": "#800000",
                            "color": "white",
                        },
                        {
                            "if": {
                                "filter_query": "{Sinal b} = positivo",
                                "column_id": "Limite Superior (xu)",
                            },
                            "backgroundColor": "#ADD8E6",  # Azul claro
                            "color": "black",
                        },
                        {
                            "if": {
                                "filter_query": "{Sinal x} = negativo",
                                "column_id": "Aproximação da Raiz (xr)",
                            },
                            "backgroundColor": "#800000",
                            "color": "white",
                        },
                        {
                            "if": {
                                "filter_query": "{Sinal x} = positivo",
                                "column_id": "Aproximação da Raiz (xr)",
                            },
                            "backgroundColor": "#ADD8E6",  # Azul claro
                            "color": "black",
                        },
                    ],
                    style_header=DATA_TABLE_STYLE.get("style_header"),
                ),
            ],
        ),
    )


# Chamada para colocar a tabela de iterações na aba de falsa posição
@app.callback(
    Output("tabela_falsa", "children"),
    Input("df-Falsa", "data"),
    State("intervalo", "value"),
    State("funcao", "value"),
    State("interacoes", "value"),
    State("tolerancia", "value"),
)
def tab_comp_falsa_tabela(df, intervalo, funcao, interacoes, tolerancia):
    funcao, funcao_simbolica = tratar_funcao(funcao)

    # tratando a função que está em string para uma função que o python entenda

    try:
        df = pd.DataFrame(df)
        funcao_latex1 = funcao_latex(funcao_simbolica)
        resultado = f"A raiz da função ${funcao_latex1}$ no intervalo [{intervalo[0]}, {intervalo[1]}] é {df['Aproximação da Raiz (xr)'].iloc[-1]} com {len(df)} iterações."
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
                hidden_columns=["f(xl)", "f(xu)", "Erro Relativo (%)"],
                id="table",
                sort_action="native",
                style_table={"height": "300px", "overflowY": "auto"},
                editable=False,
                dropdown={
                    "Resource": {
                        "clearable": False,
                        "options": [
                            {"label": i, "value": i} for i in ["A", "B", "C", "D"]
                        ],
                    },
                },
                css=DATA_TABLE_STYLE.get("css"),
                page_size=10,
                row_deletable=True,
                style_data_conditional=[
                    {
                        "if": {
                            "filter_query": "{Sinal a} = negativo",
                            "column_id": "Limite Inferior (xl)",
                        },
                        "backgroundColor": "#800000",
                        "color": "white",
                    },
                    {
                        "if": {
                            "filter_query": "{Sinal a} = positivo",
                            "column_id": "Limite Inferior (xl)",
                        },
                        "backgroundColor": "#ADD8E6",  # Azul claro
                        "color": "black",
                    },
                    {
                        "if": {
                            "filter_query": "{Sinal b} = negativo",
                            "column_id": "Limite Superior (xu)",
                        },
                        "backgroundColor": "#800000",
                        "color": "white",
                    },
                    {
                        "if": {
                            "filter_query": "{Sinal b} = positivo",
                            "column_id": "Limite Superior (xu)",
                        },
                        "backgroundColor": "#ADD8E6",  # Azul claro
                        "color": "black",
                    },
                    {
                        "if": {
                            "filter_query": "{Sinal x} = negativo",
                            "column_id": "Aproximação da Raiz (xr)",
                        },
                        "backgroundColor": "#800000",
                        "color": "white",
                    },
                    {
                        "if": {
                            "filter_query": "{Sinal x} = positivo",
                            "column_id": "Aproximação da Raiz (xr)",
                        },
                        "backgroundColor": "#ADD8E6",  # Azul claro
                        "color": "black",
                    },
                ],
                style_header=DATA_TABLE_STYLE.get("style_header"),
            ),
        ]
    except Exception as e:
        resultado = f"O método da falsa posição não convergiu após {interacoes} iterações. Por que {e}"

        return [
            html.H5(
                children="Tabela de interções usando Método da falsa posição ou interpolação"
            ),  # Título do método
            dcc.Markdown(
                "{resultado}".format(resultado=resultado),
                mathjax=True,
                style={"font-size": "14pt"},
            ),
        ]


# callback para previsualizar a matriz
@app.callback(
    Output("matrix-preview", "children"),
    Input("matrix-input", "value"),
)
def matriz_preview(mat):
    try:
        # convertendo a string para uma matriz
        mat = eval(mat)
        # convertendo a matriz para um np.array
        mat = np.array(mat)
        # convertendo a matriz para latex

        latex_code = a2l.to_ltx(
            mat, frmt="{:6.2f}", arraytype="pmatrix", mathform=True, print_out=False
        )
        texto = f"""#### Resolver para a Matriz:\n\n$${latex_code}$$\n\n"""
        return texto
    except Exception as e:
        return f"Erro ao converter a matriz: {e}\n\n Exemplo de formato correto:[[[2, 4, 3, 4, 8],[5, 8, 7, 8, 8],[9, 13, 11, 12, 7],[2, 3, 2, 5, 6],]] "


# callback para retornar um markdown a iterções do metodo de eliminação Gaussiana
@app.callback(
    Output("Markdown", "children"),
    Input("resolver_matriz", "n_clicks"),
    State("matrix-input", "value"),
    prevent_initial_call=True,
)
def markdown(n_clicks, mat):
    # convertendo a string para uma matriz
    mat = eval(mat)
    _matfinal, df = gauss(mat, full_output=True)

    texto = """"""

    # para cada iteração vamos pegar apenas a matriz passar para dentro de um np.array e vamos converter em latex e depois adicionar ao markdown
    for i, matriz in enumerate(df["Matriz"].values):
        matriz = np.array(matriz)
        latex_code = a2l.to_ltx(
            matriz, frmt="{:6.2f}", arraytype="pmatrix", mathform=True, print_out=False
        )
        texto += f"""#### Iteração {i + 1}\n\n$${latex_code}$$\n\n"""

    return dcc.Markdown(texto, mathjax=True)


# Método da Iteração Linear (Ponto Fixo)
@app.callback(
    Output("ponto_fixo", "children"),
    Input("calcular-bissecao", "n_clicks"),
    State("intervalo", "value"),
    State("funcao", "value"),
    State("interacoes", "value"),
    State("tolerancia", "value"),
)
def ponto_fixo(n_clicks, intervalo, funcao, interacoes, tolerancia):
    try:
        funcao1, funcao_simbolica = tratar_funcao(funcao)
        funcao_simbolica = funcao_latex(funcao_simbolica)
        x, tabela, iteracoes, mensagem_erro = iteracao_linear(
            funcao1, intervalo[0], maxiter=interacoes, tol=tolerancia, full_output=True
        )
        fig = grafico_animado(intervalo, funcao, tabela, "Ponto Fixo")
        resultado = f"A raiz da função ${funcao_simbolica}$ no intervalo [{intervalo[0]}, {intervalo[1]}] é {x} com {iteracoes} iterações."
        return [
            html.Div(
                children=[
                    html.Hr(),
                    dcc.Graph(figure=fig, mathjax=True),
                ],
            ),
            html.Div(
                children=[
                    html.H5(children="Mensagem de erro:"),
                    dcc.Markdown(
                        "{mensagem_erro}".format(mensagem_erro=mensagem_erro),
                        mathjax=True,
                        style={"font-size": "14pt"},
                    ),
                    html.H5(
                        children="Tabela de interções usando Método da Iteração Linear"
                    ),  # Título do método
                    dcc.Markdown(
                        "{resultado}".format(resultado=resultado),
                        mathjax=True,
                        style={"font-size": "14pt"},
                    ),
                    html.Hr(),
                    html.Div(children="Tabela de Iterações:"),
                    dash_table.DataTable(
                        tabela.to_dict("records"),
                        [
                            {"name": i, "id": i, "hideable": True}
                            for i in tabela.columns
                        ],
                        id="table",
                        sort_action="native",
                        style_table={"height": "300px", "overflowY": "auto"},
                        editable=False,
                        css=DATA_TABLE_STYLE.get("css"),
                        page_size=10,
                        row_deletable=True,
                        style_header=DATA_TABLE_STYLE.get("style_header"),
                    ),
                ],
            ),
        ]
    except Exception as e:
        tb = traceback.format_exc()
        resultado = f"Erro ao calcular o método da iteração linear: {e}"
        return html.Div(
            children=[
                html.H5(children=f"{resultado}"),  # Título do método
                dcc.Markdown(
                    "{}".format(tb),
                    style={"font-size": "14pt"},
                ),
            ]
        )


@app.callback(
    Output("newton", "children"),
    Input("calcular-bissecao", "n_clicks"),
    State("intervalo", "value"),
    State("funcao", "value"),
    State("interacoes", "value"),
    State("tolerancia", "value"),
)
def newton(n_clicks, intervalo, funcao, interacoes, tolerancia):
    try:
        _, funcao1 = tratar_funcao(funcao)
        funcao_simbolica = funcao_latex(funcao1)
        x, tabela, iteracoes = newton_raphson(
            funcao1, intervalo[0], max_iter=interacoes, tol=tolerancia, full_output=True
        )
        fig = grafico_animado(intervalo, funcao, tabela, "Newton-Raphson")
        resultado = f"A raiz da função ${funcao_simbolica}$ no intervalo [{intervalo[0]}, {intervalo[1]}] é {x} com {iteracoes} iterações."
        return [
            html.Div(
                children=[
                    html.Hr(),
                    dcc.Graph(figure=fig, mathjax=True),
                ],
            ),
            html.Div(
                children=[
                    html.H5(
                        children="Tabela de interções usando Método de Newton-Raphson"
                    ),  # Título do método
                    dcc.Markdown(
                        "{resultado}".format(resultado=resultado),
                        mathjax=True,
                        style={"font-size": "14pt"},
                    ),
                    html.Hr(),
                    html.Div(children="Tabela de Iterações:"),
                    dash_table.DataTable(
                        tabela.to_dict("records"),
                        [
                            {"name": i, "id": i, "hideable": True}
                            for i in tabela.columns
                        ],
                        id="table",
                        sort_action="native",
                        style_table={"height": "300px", "overflowY": "auto"},
                        editable=False,
                        css=DATA_TABLE_STYLE.get("css"),
                        page_size=10,
                        row_deletable=True,
                        style_header=DATA_TABLE_STYLE.get("style_header"),
                    ),
                ],
            ),
        ]
    except Exception as e:
        tb = traceback.format_exc()
        resultado = f"Erro ao calcular o Método de Newton-Raphson : {e}"
        return html.Div(
            children=[
                html.H5(children=f"{resultado}"),  # Título do método
                dcc.Markdown(
                    "{}".format(tb),
                    style={"font-size": "14pt"},
                ),
            ]
        )


@app.callback(
    Output("secant", "children"),
    Input("calcular-bissecao", "n_clicks"),
    State("intervalo", "value"),
    State("funcao", "value"),
    State("interacoes", "value"),
    State("tolerancia", "value"),
)
def secante(n_clicks, intervalo, funcao, interacoes, tolerancia):
    try:
        _, funcao1 = tratar_funcao(funcao)
        funcao_simbolica = funcao_latex(funcao1)
        x, tabela, iteracoes = secant_method(
            funcao1,
            intervalo[0],
            intervalo[1],
            max_iter=interacoes,
            tol=tolerancia,
            full_output=True,
        )
        fig = grafico_animado(intervalo, funcao, tabela, "Secante")
        resultado = f"A raiz da função ${funcao_simbolica}$ no intervalo [{intervalo[0]}, {intervalo[1]}] é {x} com {iteracoes} iterações."
        return [
            html.Div(
                children=[
                    html.Hr(),
                    dcc.Graph(figure=fig, mathjax=True),
                ],
            ),
            html.Div(
                children=[
                    html.H5(
                        children="Tabela de interções usando Método da Secante"
                    ),  # Título do método
                    dcc.Markdown(
                        "{resultado}".format(resultado=resultado),
                        mathjax=True,
                        style={"font-size": "14pt"},
                    ),
                    html.Hr(),
                    html.Div(children="Tabela de Iterações:"),
                    dash_table.DataTable(
                        tabela.to_dict("records"),
                        [
                            {"name": i, "id": i, "hideable": True}
                            for i in tabela.columns
                        ],
                        id="table",
                        sort_action="native",
                        style_table={"height": "300px", "overflowY": "auto"},
                        editable=False,
                        css=DATA_TABLE_STYLE.get("css"),
                        page_size=10,
                        row_deletable=True,
                        style_header=DATA_TABLE_STYLE.get("style_header"),
                    ),
                ],
            ),
        ]
    except Exception as e:
        tb = traceback.format_exc()
        resultado = f"Erro ao calcular o Método da Secante : {e}"
        return html.Div(
            children=[
                html.H5(children=f"{resultado}"),  # Título do método
                dcc.Markdown(
                    "{}".format(tb),
                    style={"font-size": "14pt"},
                ),
            ]
        )
