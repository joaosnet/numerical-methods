import pandas as pd
import numpy as np
import sympy as sp


def bissecao(
    a,
    b,
    f,
    args=(),
    tol=1e-18,
    xtol=1e-12,
    rtol=1e-12,
    maxiter=100,
    full_output=False,
    disp=True,
):
    """
    Executa o método da bisseção para encontrar a raiz.

    Args:
    a (float): O limite inferior do intervalo.
    b (float): O limite superior do intervalo.
    f (function): A função para a qual se deseja encontrar a raiz.
    args (tuple, optional): Argumentos adicionais para a função `f`. Defaults to ().
    tol (float, optional): A tolerância para a diferença entre `a` e `b`. Defaults to 1e-18.
    xtol (float, optional): A tolerância para a diferença entre as raízes consecutivas. Defaults to 1e-12.
    rtol (float, optional): A tolerância para o valor absoluto da função. Defaults to 1e-12.
    maxiter (int, optional): O número máximo de iterações permitidas. Defaults to 100.
    full_output (bool, optional): Se True, retorna a raiz e um DataFrame com os valores intermediários.
        Se False, retorna apenas a raiz. Defaults to False.
    disp (bool, optional): Se True, exibe uma mensagem de erro se o método não convergir.
        Se False, retorna None se o método não convergir. Defaults to True.

    Returns:
        float: A raiz da função.
        pandas.DataFrame: O DataFrame com os valores intermediários, se `full_output` for True.
    Raises:
        RuntimeError: Se o método não convergir após o número máximo de iterações.
    """
    df = pd.DataFrame(
        columns=[
            "a",
            "b",
            "Aproximação da Raiz",
            "Erro Relativo (%)",
            "Sinal a",
            "Sinal b",
            "Sinal x",
        ]
    )
    iteracoes = 0
    x = None
    x_anterior = None
    while abs(b - a) > tol:
        iteracoes += 1

        fa = f(a, *args)
        fb = f(b, *args)
        x = (a + b) / 2
        fx = f(x, *args)

        if iteracoes != 1:
            erro = abs((x - x_anterior) / x) * 100
        else:
            erro = None

        df.loc[iteracoes] = [
            a,
            b,
            x,
            erro if erro is not None else "-",
            "positivo" if np.sign(fa) > 0 else "negativo",
            "positivo" if np.sign(fb) > 0 else "negativo",
            "positivo" if np.sign(fx) > 0 else "negativo",
        ]

        if abs(b - a) < xtol or abs(fx) < rtol:
            break
        if fa * fx < 0:
            b = x
        else:
            a = x
        x_anterior = x
        if iteracoes >= maxiter:
            if disp:
                raise RuntimeError(
                    "Falha ao convergir após %d iterações, valor é %s" % (maxiter, x)
                )
            else:
                if full_output:
                    return x, df, iteracoes
                else:
                    return x

    if full_output:
        return x, df, iteracoes
    else:
        return x


def falsaposicao_modificada(xl, xu, f, es=0.0001, imax=50, full_output=False):
    df = pd.DataFrame(
        columns=[
            "Iteração",
            "Início do Intervalo (xl)",
            "Final do Intervalo (xu)",
            "Aproximação da Raiz (xr)",
            "f(xl)",
            "f(xu)",
            "f(xr)",
            "Erro Relativo (%)",
        ]
    )
    iter = 0
    fl = f(xl)
    fu = f(xu)
    xr = xl
    ea = 100
    il = 0
    iu = 0

    while ea > es and iter < imax:
        xl_anterior = xl
        xu_anterior = xu
        fl_anterior = fl
        fu_anterior = fu
        xrold = xr

        dif_intervalos = fl - fu

        if dif_intervalos == 0:
            dif_intervalos = fu - fl

        xr = xu - fu * (xl - xu) / dif_intervalos
        fr = f(xr)
        iter += 1

        if xr != 0:
            ea = abs((xr - xrold) / xr) * 100

        test = fl * fr

        if test < 0:
            xu = xr
            fu = f(xu)
            iu = 0
            il += 1
            if il >= 2:
                fl /= 2
        elif test > 0:
            xl = xr
            fl = f(xl)
            il = 0
            iu += 1
            if iu >= 2:
                fu /= 2
        else:
            ea = 0

        df.loc[iter] = [
            iter,
            xl_anterior,
            xu_anterior,
            xr,
            fl_anterior,
            fu_anterior,
            fr,
            ea if ea is not None else "-",
        ]

    if full_output:
        return xr, df, iter
    else:
        return xr


# Método da Iteração Linear (Ponto Fixo)
def iteracao_linear(g, x0, tol=1e-6, maxiter=100, full_output=False):
    """
    Executa o método da Iteração Linear (Ponto Fixo) para encontrar a raiz.

    Args:
    g (function): A função de iteração.
    x0 (float): O valor inicial.
    tol (float, optional): A tolerância para o erro aproximado. Defaults to 1e-6.
    maxiter (int, optional): O número máximo de iterações permitidas. Defaults to 100.

    Returns:
        float: A raiz da função.
        pandas.DataFrame: O DataFrame com os valores intermediários.
    """
    df = pd.DataFrame(columns=["Iteração", "x", "Erro Aproximado (%)"])
    xr = x0
    iter = 0
    ea = 100

    while True:
        xrold = xr
        xr = g(xrold)
        iter += 1
        if xr != 0:
            ea = abs((xr - xrold) / xr) * 100
        df.loc[iter] = [iter, xr, ea]
        if ea < tol or iter >= maxiter:
            break

    if full_output:
        return xr, df, iter
    else:
        return df


def newton_raphson(func_expr, x0, tol=1e-6, max_iter=100, full_output=False):
    x = sp.Symbol("x")
    f = sp.sympify(func_expr)
    f_prime = sp.diff(f, x)

    f_lambdified = sp.lambdify(x, f, "numpy")
    f_prime_lambdified = sp.lambdify(x, f_prime, "numpy")

    df = pd.DataFrame(
        columns=["Iteração", "Aproximação da Raiz (x_i)", "f(x_i)", "Erro Relativo (%)"]
    )
    xi = x0
    erro = None

    for i in range(max_iter):
        f_xi = f_lambdified(xi)
        f_prime_xi = f_prime_lambdified(xi)

        if f_prime_xi == 0:
            print(f"Derivada nula na iteração {i}. O método foi interrompido.")
            break

        df.loc[i] = [i, xi, f_xi, erro if erro is not None else "-"]

        x_next = xi - f_xi / f_prime_xi

        if i != 0:
            erro = abs((xi - x_next) / xi) * 100

        if abs(x_next - xi) < tol:
            df.loc[i + 1] = [
                i + 1,
                x_next,
                f_lambdified(x_next),
                abs((x_next - xi) / x_next) * 100,
            ]
            break

        xi = x_next

    if full_output:
        return xi, df, len(df)
    else:
        return df


def secant_method(func_expr, x0, x1, tol=1e-6, max_iter=100, full_output=False):
    x = sp.Symbol("x")
    f = sp.sympify(func_expr)
    f_lambdified = sp.lambdify(x, f, "numpy")

    df = pd.DataFrame(
        columns=["Iteração", "Aproximação da Raiz (x_i)", "f(x_i)", "Erro Relativo (%)"]
    )
    xi_1, xi = x0, x1
    erro = None

    for i in range(max_iter):
        f_xi_1 = f_lambdified(xi_1)
        f_xi = f_lambdified(xi)

        if f_xi - f_xi_1 == 0:
            print(f"Erro: Divisão por zero na iteração {i}.")
            break

        x_next = xi - f_xi * (xi - xi_1) / (f_xi - f_xi_1)

        if i != 0:
            erro = abs((xi - x_next) / xi) * 100

        df.loc[i] = [i, xi, f_xi, erro if erro is not None else "-"]

        if abs(x_next - xi) < tol:
            df.loc[i + 1] = [
                i + 1,
                x_next,
                f_lambdified(x_next),
                abs((x_next - xi) / x_next) * 100,
            ]
            break

        xi_1, xi = xi, x_next

    if full_output:
        return xi, df, len(df)
    else:
        return df


# Exemplo de uso da biblioteca de forma separada
if __name__ == "__main__":
    # inicializa a biblioteca
    import random

    # seleciona aleatoriamente qual dos dois tipos de funções para testar o
    # método da bisseção
    var = random.randint(0, 4)
    if var == 0:

        def f(x):
            return 32 * x**2 - 68 * x + 21

    elif var == 1:

        def f(x):
            return x**2 - x + (6 / 49)

    elif var == 2:

        def f(x):
            return np.sin(x) - 0.5

    elif var == 3:

        def f(x):
            return np.cos(np.log(x**2 + 1))

    else:

        def f(x):
            return np.exp(-x)  # - x

    # # ----------------------------------------
    # import inspect

    # # Obtém o código-fonte da função f
    # func_source = inspect.getsource(f)
    # print(f"Para a função:\n{func_source}")
    # raiz, df, iter = bissecao(0, 1, f, full_output=True)
    # print("Raiz:", raiz)
    # print("Iterações:", iter)
    # print(df)

    # from scipy.optimize import bisect

    # # Mmétodo da bisseção com scipy para encontrar a raiz da função no intervalo
    # # [a, b]
    # a = 0
    # b = 1
    # raiz1, converg = bisect(f, a, b, full_output=True)

    # print("Verdadeira Raiz:", raiz1)
    # # Comparação
    # print("Diferença:", abs(raiz - raiz1))

    # from pprint import pprint as pp

    # pp(converg)

    # TESTE do ponto fixo

    # print(iteracao_linear(f, 0))

    import plotly.express as px

    def func1(x):
        return 2 * x**3 - 11

    def func2(x):
        return 7 * x**2 + 17

    def func3(x):
        return 7 * x - 5

    functions = [func1, func2, func3]

    for i, f in enumerate(functions):
        fig = px.line(
            x=np.linspace(-10, 10, 1000),
            y=[f(x) for x in np.linspace(-10, 10, 1000)],
            labels={"x": "x", "y": "f(x)"},
            title=f"Função {i + 1}",
        )
        fig.show()
