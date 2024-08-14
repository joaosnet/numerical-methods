import pandas as pd


class metodos_numericos:
    """
    Biblioteca de métodos numéricos para encontrar raízes de funções.

    Attributes:
        df (pandas.DataFrame): DataFrame que armazena os valores intermediários de `a`, `b`, `X0` e `Er`.
        iteracoes (int): O número de iterações realizadas.

    Methods:
        bissecao(): Executa o método da bisseção para encontrar a raiz.
        get_df(): Retorna o DataFrame com os valores intermediários.
        get_iteracoes(): Retorna o número de iterações realizadas.
    """  # noqa: E501

    def __init__(  # noqa: PLR0913, PLR0917
        self,
    ):
        self.df = pd.DataFrame(
            columns=["a", "b", "Aproximação da Raiz", "Erro Relativo (%)"]
        )
        self.iteracoes = 0

    def bissecao(
        self,
        a,
        b,
        f,
        args=(),
        tol=0.00000000000000001,
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
        tol (float, optional): A tolerância para a diferença entre `a` e `b`. Defaults to 0.00000000000000001.
        xtol (float, optional): A tolerância para a diferença entre as raízes consecutivas. Defaults to 1e-12.
        rtol (float, optional): A tolerância para o valor absoluto da função. Defaults to 1e-12.
        maxiter (int, optional): O número máximo de iterações permitidas. Defaults to 100.
        full_output (bool, optional): Se True, retorna a raiz e um DataFrame com os valores intermediários.
            Se False, retorna apenas a raiz. Defaults to False.
        disp (bool, optional): Se True, exibe uma mensagem de erro se o método não convergir.
            Se False, retorna None se o método não convergir. Defaults to True.
            
        Attributes:
        x_anterior (float): O valor da raiz na iteração anterior.

        Returns:
            float: A raiz da função.
            pandas.DataFrame: O DataFrame com os valores intermediários, se `full_output` for True.
        Raises:
            RuntimeError: Se o método não convergir após o número máximo de iterações.
        """  # noqa: E501
        x = None
        a = a
        b = b
        f = f
        x_anterior = None
        while abs(b - a) > tol:
            self.iteracoes += 1
            if self.iteracoes > maxiter:
                if disp:
                    raise RuntimeError(
                        "Falha ao convergir após %d iterações, valor é %s"
                        % (maxiter, x)
                    )
                else:
                    return x
            fa = f(a, *args)
            # fb = f(b, *args)
            x = (a + b) / 2
            fx = f(x, *args)
            if self.iteracoes != 1:
                erro = abs((x - x_anterior) / x) * 100
            else:
                erro = None
            self.df.loc[self.iteracoes] = [a, b, x, erro]
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


if __name__ == "__main__":
    # import math
    # import numpy as np

    def f(x):
        return 32 * x**2 - 68 * x + 21

    # f = lambda x: math.exp(-x) - x
    mn = metodos_numericos()
    raiz = mn.bissecao(0, 1, f)
    print("Raiz:", raiz)
    print("Iterações:", mn.get_iteracoes())
    print(mn.get_df())

    from scipy.optimize import bisect

    # Use o método da bisseção para encontrar a raiz da função no intervalo
    # [a, b]
    a = 0
    b = 1
    raiz1 = bisect(f, a, b)

    print("Verdadeira Raiz:", raiz1)
    # Comparação
    print("Diferença:", abs(raiz - raiz1))
