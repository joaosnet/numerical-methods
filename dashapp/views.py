# Importando as bibliotecas necessárias
from dash import html, dcc, Input, Output, State
from dashapp import app, server, database, bcrypt
from dashapp.models import Usuario
from flask_login import login_required, login_user, logout_user, current_user
from flask import render_template, url_for, redirect, request
from dashapp.forms import FormLogin, FormCriarConta
from werkzeug.utils import secure_filename
import numpy as np
import pandas as pd
import joblib
from metodos import Bissecao


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
    if pathname == "/dash/":
        if current_user.is_authenticated:
            return layout_dashboard
        else:
            return dcc.Link(
                "Usuário não autenticado, faça login aqui", "/login", refresh=True
            )


@app.callback(Output("navbar", "children"), Input("url", "pathname"))
def exibir_navbar(pathname):
    if pathname != "/logout":
        if current_user.is_authenticated:
            if pathname == "/dash/":
                return html.Div([
                    dcc.Link(
                        "Logout", "/logout", className="button-link", refresh=True
                    ),
                    dcc.Link("Home", "/", className="button-link", refresh=True),
                ])
            else:
                return html.Div([
                    dcc.Link("Dashboard", "/dash/", className="button-link"),
                    dcc.Link(
                        "Logout", "/logout", className="button-link", refresh=True
                    ),
                    # dcc.Link("Nova Tela", "/nova_tela", className="button-link", refresh=True)
                ])
        else:
            return html.Div([
                dcc.Link("Login", "/login", className="button-link", refresh=True)
            ])


@app.callback(
    Output("homepage_url", "pathname"),
    Input("botao-criarconta", "n_clicks"),
    [State("email", "value"), State("senha", "value")],
)
def criar_conta(n_clicks, email, senha):
    if n_clicks:
        # vou criar a conta
        # verificar se já existe um usuário com essa conta
        usuario = Usuario.query.filter_by(email=email).first()  # finalizar
        if usuario:
            return "/login"
        else:
            # criar o usuário
            senha_criptografada = bcrypt.generate_password_hash(senha).decode("utf-8")
            usuario = Usuario(email=email, senha=senha_criptografada)  # 123456
            database.session.add(usuario)
            database.session.commit()
            login_user(usuario)
            return "/dash/"


@app.callback(
    Output("login_url", "pathname"),
    Input("botao-login", "n_clicks"),
    [State("email", "value"), State("senha", "value")],
)
def criar_conta(n_clicks, email, senha):
    if n_clicks:
        # vou criar a conta
        # verificar se já existe um usuário com essa conta
        usuario = Usuario.query.filter_by(email=email).first()  # finalizar
        if not usuario:
            return "/dash//"
        else:
            # criar o usuário
            if bcrypt.check_password_hash(usuario.senha.encode("utf-8"), senha):
                login_user(usuario)
                return "/dash/"
            else:
                return "/erro"


# Calculando a bisseção
@app.callback(
    Output("tabs", "children"),
    Input("calcular-bissecao", "n_clicks"),
    State("intervalo", "value"),
    State("funcao", "value"),
    State("interacoes", "value"),
)
def calcular_bissecao(n_clicks, intervalo, funcao, interacoes):
    # tratando a função que está em string para uma função que o python entenda
    Bissecao_obj = Bissecao(
        intervalo[0], intervalo[1], lambda x: eval(funcao), maxiter=interacoes
    )  # Aumenta o número máximo de iterações
    df = Bissecao_obj.get_df()  # Move a definição de df para fora do bloco try/except
    try:
        x = Bissecao_obj.bissecao()
        iteracoes = Bissecao_obj.get_iteracoes()
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
    # tratando a função que está em string para uma função que o python entenda
    x = np.linspace(intervalo[0], intervalo[1], 100)
    y = eval(funcao.replace("x", "x"))

    # Calcular a raiz usando o método da bisseção
    bissecao = Bissecao(
        intervalo[0], intervalo[1], lambda x: eval(funcao.replace("x", "x"))
    )
    raiz = bissecao.bissecao()

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


# ------------------------------------------------------------------------------------------------------
@server.route("/")
def homepage():
    return render_template("index.html")


# @server.route("/1")
# def homepage1():
#     return render_template('homepage1.html')


@server.route("/login", methods=["GET", "POST"])
def login():
    form_login = FormLogin()
    if form_login.validate_on_submit():
        usuario = Usuario.query.filter_by(email=form_login.email.data).first()
        if usuario and bcrypt.check_password_hash(
            usuario.senha.encode("utf-8"), form_login.senha.data
        ):
            login_user(usuario, remember=True)
            return redirect("/dash/")  # Redireciona para o dashboard
    return render_template("homepage.html", form=form_login)


@server.route("/criarconta", methods=["GET", "POST"])
def criarconta():
    form_criarconta = FormCriarConta()
    if form_criarconta.validate_on_submit():
        senha = bcrypt.generate_password_hash(form_criarconta.senha.data).decode(
            "utf-8"
        )
        usuario = Usuario(
            username=form_criarconta.username.data,
            email=form_criarconta.email.data,
            senha=senha,
        )
        database.session.add(usuario)
        database.session.commit()
        login_user(usuario, remember=True)
        return redirect("/dash/")  # Redireciona para o dashboard
    return render_template("criarconta.html", form=form_criarconta)


@server.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))


@server.route("/previsao", methods=["GET", "POST"])
def previsao():
    from pprint import pprint as pp

    dicionario = {}
    if request.method == "POST":
        # Obtém os dados do formulário
        data = request.form

        # verifica se todos os campos foram preenchidos
        # x_numericos = {'latitude': 0, 'longitude': 0, 'accommodates': 0, 'bathrooms': 0, 'bedrooms': 0, 'beds': 0, 'extra_people': 0,
        #        'minimum_nights': 0, 'ano': 0, 'mes': 0, 'n_amenities': 0, 'host_listings_count': 0}

        # x_tf = {'host_is_superhost': 0, 'instant_bookable': 0}

        # x_listas = {'property_type': ['Apartment', 'Bed and breakfast', 'Condominium', 'Guest suite', 'Guesthouse', 'Hostel', 'House', 'Loft', 'Outros', 'Serviced apartment'],
        #             'room_type': ['Entire home/apt', 'Hotel room', 'Private room', 'Shared room'],
        #             'cancellation_policy': ['flexible', 'moderate', 'strict', 'strict_14_with_grace_period']
        #             }
        # for item in x_listas:  # Para cada item nas listas de x_listas
        #     for valor in x_listas[item]:  # Para cada valor no item atual
        #         dicionario[f'{item}_{valor}'] = 0  # Adiciona uma chave-valor ao dicionário

        # for item in x_numericos:  # Para cada item nos valores numéricos
        #     if item == 'latitude' or item == 'longitude':  # Se o item for latitude ou longitude
        #         valor = st.number_input(f'{item}', step=0.00001, value=0.0, format="%.5f")  # Lê um número de entrada do usuário
        #     elif item == 'extra_people':  # Se o item for extra_people
        #         valor = st.number_input(f'{item}', step=0.01, value=0.0)  # Lê um número de entrada do usuário
        #     else:
        #         valor = st.number_input(f'{item}', step=1, value=0)  # Lê um número de entrada do usuário
        #     x_numericos[item] = valor  # Atualiza o valor no dicionário x_numericos

        # for item in x_tf:  # Para cada item nos valores booleanos
        #     valor = st.selectbox(f'{item}', ('Sim', 'Não'))  # Lê uma opção de seleção do usuário
        #     if valor == "Sim":  # Se o valor for "Sim"
        #         x_tf[item] = 1  # Atualiza o valor no dicionário x_tf para 1
        #     else:
        #         x_tf[item] = 0  # Atualiza o valor no dicionário x_tf para 0

        # for item in x_listas:  # Para cada item nas listas de x_listas
        #     valor = st.selectbox(f'{item}', x_listas[item])  # Lê uma opção de seleção do usuário
        #     dicionario[f'{item}_{valor}'] = 1  # Atualiza o valor no dicionário dicionario para 1

        # Atualiza o dicionário com os valores do formulário
        for key, value in data.items():
            try:
                dicionario[key] = float(value)
            except ValueError:
                dicionario[key] = value

        # Atualiza o dicionário com os valores do formulário
        # dicionario.update({key: float(value) for key, value in data.items()})

        # Cria um DataFrame a partir do dicionário
        valores_x = pd.DataFrame(dicionario, index=[0])

        # Carrega o modelo de aprendizado de máquina pré-treinado
        modelo = joblib.load(
            r"C:\Users\joaod\Documents\GitHub\Data-Science-Project\modelo.joblib"
        )

        # Faz a previsão do valor da propriedade com base nos valores de entrada fornecidos pelo usuário
        try:
            valor_predito = modelo.predict(valores_x)[
                0
            ]  # Faz a previsão do valor da propriedade
            return render_template(
                "previsao.html",
                valor_predito=f"O valor previsto da propriedade é R$ {valor_predito:.2f}",
            )  # Exibe o valor previsto com duas casas decimais
        except Exception as e:
            return render_template(
                "previsao.html",
                error=f"Ocorreu um erro ao prever o valor da propriedade: {e}",
            )  # Exibe uma mensagem de erro se ocorrer algum problema
    else:
        return render_template("previsao.html")
