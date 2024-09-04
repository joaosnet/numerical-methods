# Importando as bibliotecas necessárias
from dash import html, dcc, Input, Output, State, dash_table
from dashapp import app
import dash_dangerously_set_inner_html
import numpy as np
import sympy as sp
from sympy.parsing.latex import parse_latex
from metodos import bissecao, falsaposicao_modificada
import dash_mantine_components as dmc
from dash_iconify import DashIconify
import plotly.graph_objects as go

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
    # className="eight columns",
    children=[
        dcc.Tabs(
            id="tabs",
            children=[
                dcc.Tab(
                    label="Bisseção",
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
                ),
                dcc.Tab(
                    label="Falsa Posição",
                    children=[
                        html.Div(
                            children=[
                                html.Hr(),
                                dcc.Graph(id="graph_falsa", mathjax=True),
                            ],
                        ),
                        html.Div(
                            id="falsap-container",
                            children=[],
                        ),
                    ],
                ),
                dcc.Tab(
                    label="Comparações entre Métodos",
                    children=[
                        html.Div(
                            id="tabela_bissec",
                            children=[],
                        ),
                        html.Div(
                            id="tabela_falsa",
                            children=[],
                        ),
                    ],
                ),
            ],
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
    #     "collapsed": {"desktop": False, "mobile": True},
    # },
    id="app-shell",
)

# Definindo o layout do aplicativo
app.layout = dmc.MantineProvider(
    [dcc.Store(id="theme-store", storage_type="local", data="light"), appshell],
    id="mantine-provider",
    forceColorScheme="light",
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


# Função que retornar a tabela de iterações para o método da bisseção
def calcular_bissecao_tabela(intervalo, funcao, interacoes, tolerancia):
    funcao, funcao_simbolica = tratar_funcao(funcao)
    
    # tratando a função que está em string para uma função que o python entenda
    try:
        x, df, iteracoes = bissecao(
            intervalo[0],
            intervalo[1],
            funcao,
            maxiter=interacoes,
            tol=tolerancia,
            disp=False,
            full_output=True,
        )  # Aumenta o número máximo de iterações
        funcao_latex1 = funcao_latex(funcao_simbolica)
        resultado = f"A raiz da função ${funcao_latex1}$ no intervalo [{intervalo[0]}, {intervalo[1]}] é {x} com {iteracoes} iterações."

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

    except:
        resultado = f"O método da bisseção não convergiu após {interacoes} iterações."

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


# Função que retornar a tabela de iterações para o método da falsa posição
def calcular_falsa_posicao_tabela(intervalo, funcao, interacoes, tolerancia):
    funcao, funcao_simbolica = tratar_funcao(funcao)
    
    # tratando a função que está em string para uma função que o python entenda

    try:
        falsaposicao_raiz, df, iteracoes = falsaposicao_modificada(
            intervalo[0],
            intervalo[1],
            funcao,
            imax=interacoes,
            es=tolerancia,
            full_output=True,
        )  # Aumenta o número máximo de iterações
        funcao_latex1 = funcao_latex(funcao_simbolica)
        resultado = f"A raiz da função ${funcao_latex1}$ no intervalo [{intervalo[0]}, {intervalo[1]}] é {falsaposicao_raiz} com {iteracoes} iterações."

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
    except:  # noqa: E722
        resultado = (
            f"O método da falsa posição não convergiu após {interacoes} iterações."
        )

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


# pathname
@app.callback(Output("conteudo_pagina", "children"), Input("url", "pathname"))
def carregar_pagina(pathname):
    if pathname == "/":
        return layout_dashboard


# Chamada para colocar a tabela de iterações na aba de bisseção
@app.callback(
    Output("tabs", "children"),
    Input("calcular-bissecao", "n_clicks"),
    State("intervalo", "value"),
    State("funcao", "value"),
    State("interacoes", "value"),
    State("tolerancia", "value"),
)
def tab_bissecao_tabela(n_clicks, intervalo, funcao, interacoes, tolerancia):
    return calcular_bissecao_tabela(intervalo, funcao, interacoes, tolerancia)


# Chamada para colocar a tabela de iterações na aba de falsa posição
@app.callback(
    Output("falsap-container", "children"),
    Input("calcular-bissecao", "n_clicks"),
    State("intervalo", "value"),
    State("funcao", "value"),
    State("interacoes", "value"),
    State("tolerancia", "value"),
)
def tab_falsa_tabela(n_clicks, intervalo, funcao, interacoes, tolerancia):
    return calcular_falsa_posicao_tabela(intervalo, funcao, interacoes, tolerancia)


def grafico_animado(intervalo, funcao, interacoes, saida):
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
    fig_dict["layout"]["xaxis"] = {"range": [intervalo[0], intervalo[1]], "title": "x"}
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
            x=[intervalo[0], intervalo[1]], y=[0,0], mode="markers", name="Intervalo [a, b]"
        )
    )
    fig_dict["data"].append(
        go.Scatter(x=[0], y=[0], mode="markers", name="Aproximação da Raiz")
    )
    fig_dict["data"].append(go.Scatter(x=x, y=y, mode="lines", name="Função"))

    # Calcular as iterações e adicionar os frames
    if saida == "Bisseção":
        x1, df, iter = bissecao(
            intervalo[0],
            intervalo[1],
            funcao,
            maxiter=interacoes,
            disp=False,
            full_output=True,
        )

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
        x1, df, iter = falsaposicao_modificada(  # noqa: F841
            intervalo[0], intervalo[1], funcao, imax=interacoes, full_output=True
        )

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

    fig_dict["layout"]["sliders"] = [sliders_dict]

    fig = go.Figure(fig_dict)
    return fig


# Callback para atualizar o gráfico com base nos inputs
@app.callback(
    Output("graph", "figure"),
    Input("calcular-bissecao", "n_clicks"),
    State("intervalo", "value"),
    State("funcao", "value"),
    State("interacoes", "value"),
)
def atualizar_grafico(n_clicks, intervalo, funcao, interacoes):
    saida = "Bisseção"
    return grafico_animado(intervalo, funcao, interacoes, saida)


# Callback para atualizar o gráfico do Método da Falsa posicao com base nos inputs
@app.callback(
    Output("graph_falsa", "figure"),
    Input("calcular-bissecao", "n_clicks"),
    State("intervalo", "value"),
    State("funcao", "value"),
    State("interacoes", "value"),
)
def atualizar_grafico2(n_clicks, intervalo, funcao, interacoes):
    saida = "Falsa Posição"
    return grafico_animado(intervalo, funcao, interacoes, saida)


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


# TODO: Chamando os callbacks para animar
@app.callback(
    Output("app-shell", "navbar"),
    Input("burger-button", "opened"),
    State("app-shell", "navbar"),
)
def navbar_is_open(opened, navbar):
    navbar["collapsed"] = {"mobile": not opened}
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
    Input("calcular-bissecao", "n_clicks"),
    State("intervalo", "value"),
    State("funcao", "value"),
    State("interacoes", "value"),
    State("tolerancia", "value"),
)
def tab_comp_bissecao_tabela(n_clicks, intervalo, funcao, interacoes, tolerancia):
    return calcular_bissecao_tabela(intervalo, funcao, interacoes, tolerancia)


# Chamada para colocar a tabela de iterações na aba de falsa posição
@app.callback(
    Output("tabela_falsa", "children"),
    Input("calcular-bissecao", "n_clicks"),
    State("intervalo", "value"),
    State("funcao", "value"),
    State("interacoes", "value"),
    State("tolerancia", "value"),
)
def tab_comp_falsa_tabela(n_clicks, intervalo, funcao, interacoes, tolerancia):
    return calcular_falsa_posicao_tabela(intervalo, funcao, interacoes, tolerancia)
