import pandas as pd

class Bissecao:
    def __init__(self, a, b, tol, f):
        self.a = a
        self.b = b
        self.tol = tol
        self.f = f
        self.df = pd.DataFrame(columns=["a", "b", "X0", "Er"])
        self.iteracoes = 0

    def bissecao(self):
        a = self.a
        b = self.b
        tol = self.tol
        f = self.f
        while True:
            self.iteracoes += 1
            fa = f(a)
            fb = f(b)
            x = (a + b) / 2
            fx = f(x)
            erro = abs(b - a) / 2
            self.df.loc[self.iteracoes] = [a, b, x, erro]
            if erro < tol:
                break
            if fa * fx < 0:
                b = x
            else:
                a = x
        return x

    def get_df(self):
        return self.df

    def get_iteracoes(self):
        return self.iteracoes
    
    if __name__ == "__main__":
        from metodos import Bissecao
        f = lambda x: 32*x**2 - 68*x + 21
        bissecao = Bissecao(0, 1, 0.01, f)
        raiz = bissecao.bissecao()
        print("Raiz:", raiz)
        print("Iterações:", bissecao.get_iteracoes())
        print(bissecao.get_df())