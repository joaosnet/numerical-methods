import pandas as pd
import numpy as np


class metodos_numericos:
    """
    Biblioteca de métodos numéricos para encontrar raízes de funções.

    Attributes:
        df (pandas.DataFrame): DataFrame que armazena os valores intermediários de `a`, `b`, `X0`, `Er`, e sinais.
        iteracoes (int): O número de iterações realizadas.

    Methods:
        bissecao(): Executa o método da bisseção para encontrar a raiz.
        get_df(): Retorna o DataFrame(Tabela) com os valores intermediários.
        get_iteracoes(): Retorna o número de iterações realizadas.
    """

    def __init__(self):
        self.df = pd.DataFrame(
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
        self.iteracoes = 0

    def bissecao(
        self,
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
        x = None
        x_anterior = None
        while abs(b - a) > tol:
            self.iteracoes += 1
            if self.iteracoes >= maxiter:
                if disp:
                    raise RuntimeError(
                        "Falha ao convergir após %d iterações, valor é %s"
                        % (maxiter, x)
                    )
                else:
                    return x
            fa = f(a, *args)
            fb = f(b, *args)
            x = (a + b) / 2
            fx = f(x, *args)
            
            if self.iteracoes != 1:
                erro = abs((x - x_anterior) / x) * 100
            else:
                erro = None
                
            self.df.loc[self.iteracoes] = [
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
        if full_output:
            return x, self.df
        else:
            return x
    
    def falsaposicao_modificada(self, xl, xu, f, es=0.0001, imax=50):
        iter = 0
        fl = f(xl)
        fu = f(xu)
        xr = xl
        ea = 100
        il = 0
        iu = 0

        while ea > es and iter < imax:
            xrold = xr
            xr = xu - fu * (xl - xu) / (fl - fu)
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
            self.iteracoes = iter
            self.df.loc[iter] = [
                xl,
                xu,
                xr,
                ea if ea is not None else "-",
                "positivo" if np.sign(fl) > 0 else "negativo",
                "positivo" if np.sign(fu) > 0 else "negativo",
                "positivo" if np.sign(fr) > 0 else "negativo",
            ]

        return xr

    def get_df(self):
        """
        Retorna o DataFrame com os valores intermediários.

        Returns:
            pandas.DataFrame: O DataFrame com os valores intermediários.
        """
        return self.df

    def get_iteracoes(self):
        """
        Retorna o número de iterações realizadas.

        Returns:
            int: O número de iterações realizadas.
        """
        return self.iteracoes

# Exemplo de uso da biblioteca de forma separada
if __name__ == "__main__":
    # inicializa a biblioteca
    mn = metodos_numericos()
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
            return np.cos(np.log(x**2+1))

    else:
        import math

        def f(x):
            return math.exp(-x) - x
        
        

    # ----------------------------------------
    print("Para a função {}".format(str(f)))
    raiz = mn.bissecao(0, 1, f)
    print("Raiz:", raiz)
    print("Iterações:", mn.get_iteracoes())
    print(mn.get_df())

    from scipy.optimize import bisect

    # Mmétodo da bisseção com scipy para encontrar a raiz da função no intervalo
    # [a, b]
    a = 0
    b = 1
    raiz1, converg = bisect(f, a, b, full_output=True)

    print("Verdadeira Raiz:", raiz1)
    # Comparação
    print("Diferença:", abs(raiz - raiz1))

    from pprint import pprint as pp

    pp(converg)
