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
    p = k  # Inicializa p como k, que é o índice da linha atual
    big = abs(a[k, k] / s[k])  # Calcula o maior valor relativo para a linha k
    for ii in range(k + 1, n):  # Itera sobre as linhas abaixo da linha k
        dummy = abs(a[ii, k] / s[ii])  # Calcula o valor relativo para a linha ii
        if dummy > big:  # Se o valor relativo for maior que o atual maior valor
            big = dummy  # Atualiza o maior valor
            p = ii  # Atualiza o índice da linha com o maior valor
    if p != k:  # Se a linha com o maior valor não for a linha k
        for jj in range(k, n):  # Itera sobre as colunas a partir da coluna k
            a[p, jj], a[k, jj] = a[k, jj], a[p, jj]  # Troca as linhas p e k na matriz a
        b[p], b[k] = b[k], b[p]  # Troca as linhas p e k no vetor b
        s[p], s[k] = s[k], s[p]  # Troca as linhas p e k no vetor s
    return a, b, s  # Retorna as matrizes e vetores atualizados

def substitute(a, n, b, x, df):
    mat = np.hstack((a, b.reshape(-1, 1)))  # Combina a matriz a e o vetor b em uma matriz
    x[n-1] = b[n-1] / a[n-1, n-1]  # Calcula o valor de x para a última linha
    mat[n-1, n] = b[n-1] / a[n-1, n-1]  # Atualiza a matriz combinada com o valor de x calculado
    for i in range(n - 2, -1, -1):  # Itera de baixo para cima, excluindo a última linha
        sum_ = 0  # Inicializa a soma
        for j in range(i + 1, n):  # Itera sobre as colunas à direita da diagonal
            sum_ += a[i, j] * x[j]  # Calcula a soma dos produtos dos elementos da linha i e x
        x[i] = (b[i] - sum_) / a[i, i]  # Calcula o valor de x para a linha i
        mat[i, n] = (b[i] - sum_) / a[i, i]  # Atualiza a matriz combinada com o valor de x calculado
        df = df._append({"Matriz": mat.copy()}, ignore_index=True)  # Armazena uma cópia da matriz no DataFrame
    return x, df  # Retorna o vetor x e o DataFrame atualizado

def eliminate(a, s, n, b, tol, er, df):
    for k in range(n - 1):  # Itera sobre as colunas, exceto a última
        a, b, s = pivot(a, b, s, n, k)  # Realiza a pivotação parcial
        if abs(a[k, k] / s[k]) < tol:  # Verifica se o elemento da diagonal é menor que a tolerância
            er = -1  # Define o erro como -1
            break  # Sai do loop
        for i in range(k + 1, n):  # Itera sobre as linhas abaixo da linha k
            factor = a[i, k] / a[k, k]  # Calcula o fator de eliminação
            for j in range(k, n):  # Itera sobre as colunas a partir da coluna k
                a[i, j] -= factor * a[k, j]  # Atualiza a linha i subtraindo o fator vezes a linha k
            b[i] -= factor * b[k]  # Atualiza o vetor b
        df = df._append({"Matriz": np.hstack((a, b.reshape(-1, 1))).copy()}, ignore_index=True)  # Armazena uma cópia da matriz no DataFrame
    if abs(a[n-1, n-1] / s[n-1]) < tol:  # Verifica se o último elemento da diagonal é menor que a tolerância
        er = -1  # Define o erro como -1
    return a, b, er, df  # Retorna as matrizes, o vetor b, o erro e o DataFrame atualizado

def gauss(mat, tol=1.0e-12, full_output=False):
    mat = np.array(mat, dtype=float)  # Converte a matriz para um array NumPy
    a, b = np.hsplit(mat, [len(mat)])  # Separa a matriz a e o vetor b
    n = len(b)  # Obtém o tamanho do vetor b
    x = np.zeros(n)  # Inicializa o vetor x com zeros
    s = np.zeros(n)  # Inicializa o vetor s com zeros
    er = 0  # Inicializa o erro como 0
    df1 = pd.DataFrame(columns=["Matriz"])  # Cria um DataFrame para armazenar as matrizes

    for i in range(n):  # Itera sobre as linhas
        s[i] = abs(a[i, 0])  # Inicializa o vetor s com o valor absoluto do primeiro elemento da linha
        for j in range(1, n):  # Itera sobre as colunas a partir da segunda coluna
            if abs(a[i, j]) > s[i]:  # Se o valor absoluto do elemento for maior que o valor atual em s
                s[i] = abs(a[i, j])  # Atualiza o valor em s

    a, b, er, df1 = eliminate(a, s, n, b, tol, er, df1)  # Realiza a eliminação gaussiana
    if er != -1:  # Se não houve erro
        x, df = substitute(a, n, b, x, df1)  # Realiza a substituição para encontrar o vetor x

    if full_output:  # Se full_output for True
        return x, df  # Retorna o vetor x e o DataFrame
    else:
        return df  # Retorna apenas o DataFrame


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

    # mat, df = matriz_tringular_superior(mat, full_output=True)
    # pp(mat)

    print("Forma final da matriz:")
    df = gauss(mat)
    pp(df["Matriz"].values)

    print("Gauss")
    x, df = gauss(mat, full_output=True)
    pp(df["Matriz"].values)
    pp(x)
