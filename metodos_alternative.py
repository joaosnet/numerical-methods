import numpy as np
import pandas as pd

def bissecao(f, a, b, tol=1e-6, maxiter=100):
    """
    Método da bisseção para encontrar uma raiz da função f no intervalo [a, b].

    Args:
        f (function): Função cuja raiz está sendo buscada.
        a (float): Limite inferior do intervalo.
        b (float): Limite superior do intervalo.
        tol (float): Tolerância para o critério de parada.
        maxiter (int): Número máximo de iterações.

    Returns:
        float: A raiz aproximada da função f no intervalo [a, b].
        float: O valor da aproximação final.
    """
    fa = f(a)
    fb = f(b)
    
    if fa * fb >= 0:
        return None, None  # Retorna None se não há mudança de sinal

    iteracoes = 0
    while (b - a) / 2 > tol and iteracoes < maxiter:
        c = (a + b) / 2
        fc = f(c)
        if fc == 0 or (b - a) / 2 < tol:
            return c, (b - a) / 2
        iteracoes += 1
        if fa * fc < 0:
            b = c
        else:
            a = c
            fa = fc
    return (a + b) / 2, (b - a) / 2

def encontrar_raizes_intervalo(f, intervalo_inicio, intervalo_fim, incremento, tol):
    """
    Encontra as raízes de uma função f em um intervalo, dividindo-o em subintervalos.

    Args:
        f (function): Função cuja raiz está sendo buscada.
        intervalo_inicio (float): Limite inferior do intervalo total.
        intervalo_fim (float): Limite superior do intervalo total.
        incremento (float): Tamanho do incremento para definir os subintervalos.
        tol (float): Tolerância para o critério de parada da bisseção.

    Returns:
        pandas.DataFrame: DataFrame contendo as raízes, sinais e aproximações para cada subintervalo.
    """
    atual = intervalo_inicio
    resultados = []

    while atual < intervalo_fim:
        proximo = min(atual + incremento, intervalo_fim)
        raiz, aproximacao = bissecao(f, atual, proximo, tol)
        if raiz is not None:
            sinal = np.sign(f(raiz + 1e-6))  # Checa o sinal um pouco à direita da raiz
            resultados.append({
                'Intervalo [a, b]': f"[{atual}, {proximo}]",
                'Raiz': raiz,
                'Sinal': 'positivo' if sinal > 0 else 'negativo',
                'Aproximação': aproximacao
            })
        else:
            resultados.append({
                'Intervalo [a, b]': f"[{atual}, {proximo}]",
                'Raiz': 'Nenhuma raiz',
                'Sinal': 'N/A',
                'Aproximação': 'N/A'
            })
        atual = proximo

    df_resultados = pd.DataFrame(resultados)
    return df_resultados

# Exemplo de uso
if __name__ == "__main__":
    # Define uma função exemplo
    def f(x):
        return np.sin(x) - 0.5

    # Solicita ao usuário o intervalo, o incremento e a tolerância
    intervalo_inicio = float(input("Digite o limite inferior do intervalo: "))
    intervalo_fim = float(input("Digite o limite superior do intervalo: "))
    incremento = float(input("Digite o valor do incremento: "))
    tol = float(input("Digite a tolerância (aproximação máxima): "))

    # Encontra as raízes no intervalo definido
    df_raizes = encontrar_raizes_intervalo(f, intervalo_inicio, intervalo_fim, incremento, tol)

    # Exibe o DataFrame com as informações das raízes
    print("\nDataFrame com as informações das raízes:")
    print(df_raizes)