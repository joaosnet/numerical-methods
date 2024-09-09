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
        for i in range(j + 1, m):
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
        A[j] = A[j] / A[j, j]
        for i in range(j - 1, -1, -1):
            A[i] = A[i] - A[j] * A[i, j]
            # Armazenando uma cópia independente da matriz no DataFrame
            df = df._append({"Matriz": A.copy()}, ignore_index=True)
    df = df._append({"Matriz": A.copy()}, ignore_index=True)

    if full_output:
        return A, df
    else:
        return A


if __name__ == "__main__":
    from pprint import pprint as pp
    
    A = [
        [2, 4, 3, 4, 8],
        [5, 8, 7, 8, 8],
        [9, 13, 11, 12, 7],
        [2, 3, 2, 5, 6],
    ]
    mat = [
        [3.0, 2.0, -4.0, 3.0],
        [2.0, 3.0, 3.0, 15.0],
        [5.0, -3, 1.0, 14.0],
    ]

    # A, df = matriz_tringular_superior(A, full_output=True)
    # print("Matriz triangular superior:")
    # pp(A)
    # # mostrando apenas os arrays na coluna matriz de df
    # pp(df["Matriz"].values)

    # print("Forma final da matriz:")
    # A, df = matriz_forma_final(A, full_output=True)
    # pp(A)
    # display(df)
    # pp(df["Matriz"].values)

    # mat, df = matriz_tringular_superior(mat, full_output=True)
    # pp(mat)

    print("Forma final da matriz:")
    mat, df = matriz_forma_final(mat, full_output=True)
    pp(df["Matriz"].values)