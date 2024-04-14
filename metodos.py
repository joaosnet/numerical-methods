import pandas as pd
import numpy as np

class Bissecao:
    """
    Implementa o método da bisseção para encontrar a raiz de uma função.

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
        df (pandas.DataFrame): DataFrame que armazena os valores intermediários de `a`, `b`, `X0` e `Er`.
        iteracoes (int): O número de iterações realizadas.
        x_anterior (float): O valor da raiz na iteração anterior.

    Methods:
        bissecao(): Executa o método da bisseção para encontrar a raiz.
        get_df(): Retorna o DataFrame com os valores intermediários.
        get_iteracoes(): Retorna o número de iterações realizadas.
    """
    def __init__(self, a, b, f, args=(), tol=0.00000000000000001, xtol=1e-12, rtol=1e-12, maxiter=100, full_output=False, disp=True):
        self.a = a
        self.b = b
        self.tol = tol
        self.f = f
        self.args = args
        self.xtol = xtol
        self.rtol = rtol
        self.maxiter = maxiter
        self.full_output = full_output
        self.disp = disp
        self.df = pd.DataFrame(columns=["a", "b", "Aproximação da Raiz", "Erro Relativo (%)"])
        self.iteracoes = 0
        self.x_anterior = None


    def bissecao(self):
        """
        Executa o método da bisseção para encontrar a raiz.

        Returns:
            float: A raiz da função.
            pandas.DataFrame: O DataFrame com os valores intermediários, se `full_output` for True.
        Raises:
            RuntimeError: Se o método não convergir após o número máximo de iterações.
        """
        a = self.a
        b = self.b
        tol = self.tol
        f = self.f
        args = self.args
        while abs(b - a) > tol:
            self.iteracoes += 1
            if self.iteracoes > self.maxiter:
                if self.disp:
                    raise RuntimeError("Falha ao convergir após %d iterações, valor é %s" % (self.maxiter, x))
                else:
                    return x
            fa = f(a, *args)
            fb = f(b, *args)
            x = (a + b) / 2
            fx = f(x, *args)
            if self.iteracoes != 1:
                erro = abs((x - self.x_anterior) / x) * 100
            else:
                erro = None
            self.df.loc[self.iteracoes] = [a, b, x, erro]
            if abs(b - a) < self.xtol or abs(fx) < self.rtol:
                break
            if fa * fx < 0:
                b = x
            else:
                a = x
            self.x_anterior = x
        if self.full_output:
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
    import math
    f = lambda x: 32*x**2 - 68*x + 21
    # f = lambda x: math.exp(-x) - x
    bissecao = Bissecao(0, 1, f)
    raiz = bissecao.bissecao()
    print("Raiz:", raiz)
    print("Iterações:", bissecao.get_iteracoes())
    print(bissecao.get_df())

    from scipy.optimize import bisect

    # Use o método da bisseção para encontrar a raiz da função no intervalo [a, b]
    a = 0
    b = 1
    raiz1 = bisect(f, a, b)

    print("Verdadeira Raiz:", raiz1)
 # Comparação
    print("Diferença:", abs(raiz - raiz1))