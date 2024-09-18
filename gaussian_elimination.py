import numpy as np
import pandas as pd


def matriz_tringular_superior(A, full_output=False):
    # Criando um data frame para armazenar cada interação do algoritmo
    df = pd.DataFrame(columns=["Matriz"])
    # Convertendo a matriz para um array NumPy
    A = np.array(A, dtype=float)

    # verificando o tamanho da matriz
    m, _n = A.shape

    for j in range(m - 1):
        # Atualizando as linhas abaixo da linha j
        for i in range(j + 1, m):
            # Verificando se o elemento da diagonal é zero
            if A[j, j] == 0:
                raise ValueError("Divisão por zero detectada!")
            # Atualizando a linha A[i]
            A[i] = A[j, j] * A[i] - A[i, j] * A[j]
            # Armazenando uma cópia independente da matriz no DataFrame
            df = df._append({"Matriz": A.copy()}, ignore_index=True)

    if full_output:
        return A, df
    else:
        return A


def matriz_forma_final(A, full_output=False):
    # Obtendo a matriz triangular superior
    A, df = matriz_tringular_superior(A, full_output=True)
    # Como a matriz já é um array NumPy
    m, _n = A.shape
    # fazemos agora a resolucao de baixo para cima
    for j in range(m - 1, -1, -1):
        # Normalizando a linha j
        A[j] = A[j] / A[j, j]
        # Atualizando as linhas acima da linha j
        for i in range(j - 1, -1, -1):
            A[i] = A[i] - A[j] * A[i, j]
            # Armazenando uma cópia independente da matriz no DataFrame
            df = df._append({"Matriz": A.copy()}, ignore_index=True)
    # Adicionando a matriz identidade ao DataFrame
    df = df._append({"Matriz": A.copy()}, ignore_index=True)

    if full_output:
        return A, df
    else:
        return df


# --------------------------------------------------------------------------------------------


def pivot(a, b, s, n, k):
    p = k
    big = abs(a[k, k] / s[k])
    for ii in range(k + 1, n):
        dummy = abs(a[ii, k] / s[ii])
        if dummy > big:
            big = dummy
            p = ii
    if p != k:
        for jj in range(k, n):
            a[p, jj], a[k, jj] = a[k, jj], a[p, jj]
        b[p], b[k] = b[k], b[p]
        s[p], s[k] = s[k], s[p]
    return a, b, s

def substitute(a, n, b, x, df):
    # transformando a e b em arrays NumPy
    mat = np.hstack((a, b.reshape(-1, 1)))
    x[n-1] = b[n-1] / a[n-1, n-1]
    mat[n-1, n] = b[n-1] / a[n-1, n-1]
    for i in range(n - 2, -1, -1):
        sum_ = 0
        for j in range(i + 1, n):
            sum_ += a[i, j] * x[j]
        x[i] = (b[i] - sum_) / a[i, i]
        mat[i, n] = (b[i] - sum_) / a[i, i]
        df = df._append(
            {"Matriz": mat.copy()}, ignore_index=True
        )
    return x, df

def eliminate(a, s, n, b, tol, er, df):
    for k in range(n - 1):
        a, b, s = pivot(a, b, s, n, k)
        if abs(a[k, k] / s[k]) < tol:
            er = -1
            break
        for i in range(k + 1, n):
            factor = a[i, k] / a[k, k]
            for j in range(k, n):
                a[i, j] -= factor * a[k, j]
            b[i] -= factor * b[k]
        df = df._append(
            {"Matriz": np.hstack((a, b.reshape(-1, 1))).copy()}, ignore_index=True
        )
    if abs(a[n-1, n-1] / s[n-1]) < tol:
        er = -1
    return a, b, er, df

def gauss(mat, tol=1.0e-12, full_output=False):
    mat = np.array(mat, dtype=float)
    a, b = np.hsplit(mat, [len(mat)])
    n = len(b)
    x = np.zeros(n)
    s = np.zeros(n)
    er = 0
    df1 = pd.DataFrame(columns=["Matriz"])

    for i in range(n):
        s[i] = abs(a[i, 0])
        for j in range(1, n):
            if abs(a[i, j]) > s[i]:
                s[i] = abs(a[i, j])

    a, b, er, df1 = eliminate(a, s, n, b, tol, er, df1)
    if er != -1:
        x, df = substitute(a, n, b, x, df1)

    if full_output:
        return x, df
    else:
        return df


if __name__ == "__main__":
    from pprint import pprint as pp

    # A = [
    #     [2, 4, 3, 4, 8],
    #     [5, 8, 7, 8, 8],
    #     [9, 13, 11, 12, 7],
    #     [2, 3, 2, 5, 6],
    # ]
    # mat = [
    #     [3.0, 2.0, -4.0, 3.0],
    #     [2.0, 3.0, 3.0, 15.0],
    #     [5.0, -3, 1.0, 14.0],
    # ]

    # mat = [
    #     [2, 100.000, 100.000],
    #     [1, 1, 2],
    # ]

    # mat = [
    #     [70, 1, 0, 636],
    #     [60, -1, 1, 518],
    #     [40, 0, -1, 307],
    # ]

    # mat = [
    #     [3, -0.1, -0.2, 7.85],
    #     [0.1, 7, -0.3, -19.3],
    #     [0.3, -0.2, 10, 71.4],
    # ]
    
    # mat = [
    #     [70, 1, 0, 636],
    #     [60, -1, 1, 518],
    #     [40, 0, -1, 307],
    # ]
    
    mat = [
        [0, 2, 3, 8],
        [4, 6, 7, -3],
        [2, 1, 6, 5],
    ]

    # A, df = matriz_tringular_superior(A, full_output=True)
    # print("Matriz triangular superior:")
    # pp(A)
    # # mostrando apenas os arrays na coluna matriz de df
    # pp(df["Matriz"].values)

    # print("Forma final da matriz:")
    # A, df = gauss(A, full_output=True)
    # pp(A)
    # display(df)
    # pp(df["Matriz"].values)

    mat, df = matriz_tringular_superior(mat, full_output=True)
    pp(mat)

    print("Forma final da matriz:")
    df = gauss(mat)
    pp(df["Matriz"].values)

    print("Gauss")
    x, df = gauss(mat, full_output=True)
    pp(df["Matriz"].values)
    pp(x)
