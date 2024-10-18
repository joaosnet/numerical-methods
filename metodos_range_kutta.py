import numpy as np  # Importa a biblioteca NumPy para operações numéricas
import pandas as pd  # Importa a biblioteca Pandas para manipulação de dados
import sympy as sp  # Importa a biblioteca SymPy para manipulação simbólica
import plotly.graph_objects as go  # Importa a biblioteca Plotly para criação de gráficos

# Método de Euler
def euler_method(f, t0, y0, t_end, h):
    t_values = np.arange(t0, t_end + h, h)  # Cria uma lista de valores de t de t0 até t_end com passo h
    y_values = np.zeros(len(t_values))  # Inicializa uma lista de valores de y com zeros
    y_values[0] = y0  # Define o valor inicial de y

    for i in range(1, len(t_values)):  # Itera sobre os valores de t
        y_values[i] = y_values[i-1] + h * f(t_values[i-1], y_values[i-1])  # Aplica o método de Euler

    return t_values, y_values  # Retorna os valores de t e y

# Método de Runge-Kutta de ordem 3
def rk3(f, x0, y0, xf, h):
    x_list = [x0]  # Inicializa a lista de valores de x
    y_list = [y0]  # Inicializa a lista de valores de y
    
    x = x0  # Define o valor inicial de x
    y = y0  # Define o valor inicial de y
    
    while x < xf:  # Itera até que x alcance xf
        if x + h > xf:  # Ajusta o passo h se ultrapassar xf
            h = xf - x
        
        k1 = f(x, y)  # Calcula k1
        k2 = f(x + h/2, y + h*k1/2)  # Calcula k2
        k3 = f(x + h, y - h*k1 + 2*h*k2)  # Calcula k3
        
        y += (h/6)*(k1 + 4*k2 + k3)  # Atualiza y
        x += h  # Atualiza x
        
        x_list.append(x)  # Adiciona x à lista
        y_list.append(y)  # Adiciona y à lista
    
    return x_list, y_list  # Retorna as listas de x e y

# Método de Runge-Kutta de ordem 4
def rk4(f, x0, y0, xf, h, full_output=False):
    x_list = [x0]  # Inicializa a lista de valores de x
    y_list = [y0]  # Inicializa a lista de valores de y
    
    x = x0  # Define o valor inicial de x
    y = y0  # Define o valor inicial de y
    
    while x < xf:  # Itera até que x alcance xf
        if x + h > xf:  # Ajusta o passo h se ultrapassar xf
            h = xf - x
        
        k1 = f(x, y)  # Calcula k1
        k2 = f(x + h/2, y + h*k1/2)  # Calcula k2
        k3 = f(x + h/2, y + h*k2/2)  # Calcula k3
        k4 = f(x + h, y + h*k3)  # Calcula k4
        
        y += (h/6)*(k1 + 2*k2 + 2*k3 + k4)  # Atualiza y
        x += h  # Atualiza x
        
        x_list.append(x)  # Adiciona x à lista
        y_list.append(y)  # Adiciona y à lista
    
    if full_output:  # Se full_output for True
        df = pd.DataFrame({'x': x_list, 'y': y_list})  # Cria um DataFrame com os resultados
        return df  # Retorna o DataFrame
    else:
        return x_list, y_list  # Retorna as listas de x e y

# Resolve uma equação diferencial ordinária (ODE)
def solve_ode(func_expr, x0, y0, xf, h_values):
    x = sp.Symbol('x')  # Define o símbolo x
    y = sp.Symbol('y')  # Define o símbolo y
    y_func = sp.Function('y')  # Define a função y(x)

    # Solução analítica
    eq = sp.Eq(y_func(x).diff(x), func_expr.subs(y, y_func(x)))  # Define a equação diferencial
    try:
        y_analytic = sp.dsolve(eq, y_func(x), ics={y_func(x0): y0})  # Tenta resolver a equação diferencial
        y_analytic_func = sp.lambdify(x, y_analytic.rhs, modules=['numpy'])  # Converte a solução analítica para uma função numérica
    except NotImplementedError:
        print("Não foi possível encontrar uma solução analítica. Usando solução numérica de alta precisão.")
        y_analytic_func = None

    # Criar função numérica
    f_num = sp.lambdify([x, y], func_expr, modules=['numpy'])  # Converte a expressão simbólica para uma função numérica

    results = {}  # Inicializa o dicionário de resultados

    for method, rk_func in [("Euler", euler_method), ("RK3", rk3), ("RK4", rk4)]:  # Itera sobre os métodos numéricos
        method_results = {}  # Inicializa o dicionário de resultados para o método atual
        for h in h_values:  # Itera sobre os valores de h
            x_list, y_list = rk_func(f_num, x0, y0, xf, h)  # Aplica o método numérico
            method_results[h] = {'x': x_list, 'y': y_list}  # Armazena os resultados
        results[method] = method_results  # Armazena os resultados do método atual

    # Solução analítica ou numérica de alta precisão
    x_analytic = np.linspace(x0, xf, 1000)  # Cria uma lista de valores de x para a solução analítica
    if y_analytic_func:
        y_analytic = y_analytic_func(x_analytic)  # Calcula a solução analítica
    else:
        # Usar RK4 com passo muito pequeno como aproximação da solução exata
        _, y_analytic = rk4(f_num, x0, y0, xf, (xf-x0)/10000)  # Calcula a solução numérica de alta precisão

    return results, x_analytic, y_analytic  # Retorna os resultados e a solução analítica

# Cria gráficos dos resultados
def create_plots(results, x_analytic, y_analytic, func_str):
    
    fig_combined = go.Figure()  # Cria uma figura vazia
    
    for method in results:  # Itera sobre os métodos
        for h, data in results[method].items():  # Itera sobre os valores de h
            fig_combined.add_trace(go.Scatter(
                x=data['x'],
                y=data['y'],
                mode='markers',
                name=f'{method}, h = {h}'
            ))  # Adiciona os resultados ao gráfico
    
    fig_combined.add_trace(go.Scatter(
        x=x_analytic,
        y=y_analytic,
        mode='lines',
        name='Solução Analítica'
    ))  # Adiciona a solução analítica ao gráfico
    
    fig_combined.update_layout(
        title=f'Resultados dos Métodos de Runge-Kutta para dy/dx = {func_str}',
        xaxis_title='x',
        yaxis_title='y',
        legend_title='Legenda'
    )  # Atualiza o layout do gráfico
    
    return fig_combined  # Retorna o gráfico

# Cria uma tabela com os resultados
def create_table(results):
    df = pd.DataFrame()  # Cria um DataFrame vazio
    for method in results:  # Itera sobre os métodos
        for h, data in results[method].items():  # Itera sobre os valores de h
            temp_df = pd.DataFrame({
                'x': data['x'],
                'y': data['y'],
                'Método': method,
                'h': h
            })  # Cria um DataFrame temporário com os resultados
            df = pd.concat([df, temp_df], ignore_index=True)  # Concatena o DataFrame temporário ao DataFrame principal
    return df  # Retorna o DataFrame

# Compara os métodos de Runge-Kutta
def compare_rk_methods(func, x0, y0, xf, h_values, exact_solution):
    methods = {
        'Euler': euler_method,
        'RK3': rk3,
        'RK4': rk4,
    }  # Define os métodos numéricos
    
    results = {}  # Inicializa o dicionário de resultados
    
    for method_name, method_func in methods.items():  # Itera sobre os métodos
        method_results = []  # Inicializa a lista de resultados para o método atual
        for h in h_values:  # Itera sobre os valores de h
            x_list, y_list = method_func(func, x0, y0, xf, h)  # Aplica o método numérico
            error = abs((y_list[-1] - exact_solution) / exact_solution) * 100  # Calcula o erro relativo percentual
            computational_effort = len(x_list) - 1  # Calcula o esforço computacional
            method_results.append({
                'h': h,
                'error': error,
                'effort': computational_effort
            })  # Armazena os resultados
        results[method_name] = method_results  # Armazena os resultados do método atual
    
    return results  # Retorna os resultados

# Cria um gráfico de erro vs. esforço computacional
def plot_error_vs_effort(results):
    fig = go.Figure()  # Cria uma figura vazia
    
    for method, data in results.items():  # Itera sobre os métodos
        errors = [point['error'] for point in data]  # Extrai os erros
        efforts = [point['effort'] for point in data]  # Extrai os esforços computacionais
        
        fig.add_trace(go.Scatter(
            x=efforts,
            y=errors,
            mode='lines+markers',
            name=method
        ))  # Adiciona os resultados ao gráfico
    
    fig.update_layout(
        title='Erro Relativo Percentual vs. Esforço Computacional',
        xaxis_title='Esforço Computacional (Número de Passos)',
        yaxis_title='Erro Relativo Percentual',
        yaxis_type="log",
        xaxis_type="log",
        yaxis=dict(range=[-6, 2])  # Ajusta a escala do eixo y de 10^-6 a 10^2
    )  # Atualiza o layout do gráfico
    
    return fig  # Retorna o gráfico

# Função principal
def main():
    # Exemplo de uso
    # Definindo a equação diferencial: dy/dx = 4*e^(0.8*x) - 0.5*y
    x = sp.Symbol('x')  # Define o símbolo x
    y = sp.Symbol('y')  # Define o símbolo y

    func_expr = 4*sp.exp(0.8*x) - 0.5*y  # Define a expressão da equação diferencial
    
    x0 = 0  # Define o valor inicial de x
    y0 = 2  # Define o valor inicial de y
    xf = 4  # Define o valor final de x
    h_values = [1, 0.1, 0.01]  # Define os valores de h

    results, x_analytic, y_analytic = solve_ode(func_expr, x0, y0, xf, h_values)  # Resolve a equação diferencial
    fig = create_plots(results, x_analytic, y_analytic, func_str=str(func_expr))  # Cria os gráficos
    fig.show()  # Mostra os gráficos
    
    # Criar tabela de resultados
    df = create_table(results)  # Cria a tabela de resultados
    print(df.head())  # Imprime as primeiras linhas da tabela

    exact_solution = 75.33896  # Define a solução exata

    # Criar função numérica
    f_num = sp.lambdify([x, y], func_expr, modules=['numpy'])  # Converte a expressão simbólica para uma função numérica

    comparison_results = compare_rk_methods(f_num, x0, y0, xf, h_values, exact_solution)  # Compara os métodos numéricos
    fig2 = plot_error_vs_effort(comparison_results)  # Cria o gráfico de erro vs. esforço computacional
    fig2.show()  # Mostra o gráfico

    # Equação 1: dy/dx = y*x^2 - 1.1*y
    func_expr1 = y*x**2 - 1.1*y  # Define a expressão da equação diferencial
    
    x0 = 0  # Define o valor inicial de x
    y0 = 1  # Define o valor inicial de y
    xf = 2  # Define o valor final de x
    h_values = [0.5, 0.25]  # Define os valores de h

    results1, x_analytic1, y_analytic1 = solve_ode(func_expr1, x0, y0, xf, h_values)  # Resolve a equação diferencial
    fig1 = create_plots(results1, x_analytic1, y_analytic1, func_str=str(func_expr1))  # Cria os gráficos
    fig1.update_layout(title="Problema 25.1: dy/dx = y*x^2 - 1.1*y")  # Atualiza o título do gráfico
    fig1.show()  # Mostra o gráfico
    
    # Criar tabela de resultados
    df1 = create_table(results1)  # Cria a tabela de resultados
    print("Resultados para o Problema 25.1:")  # Imprime uma mensagem
    print(df1)  # Imprime a tabela de resultados

    # Problema 25.4 e 25.5 estão incluídos nos resultados acima

    # Problema 25.6
    # Equação 2: dy/dx = (1 + 2x)*sqrt(y)
    func_expr2 = (1 + 2*x)*sp.sqrt(y)  # Define a expressão da equação diferencial
    
    x0 = 0  # Define o valor inicial de x
    y0 = 1  # Define o valor inicial de y
    xf = 1  # Define o valor final de x
    h_values = [0.5, 0.25]  # Define os valores de h

    results2, x_analytic2, y_analytic2 = solve_ode(func_expr2, x0, y0, xf, h_values)  # Resolve a equação diferencial
    fig2 = create_plots(results2, x_analytic2, y_analytic2, func_str=str(func_expr2))  # Cria os gráficos
    fig2.update_layout(title="Problema 25.6: dy/dx = (1 + 2x)*sqrt(y)")  # Atualiza o título do gráfico
    fig2.show()  # Mostra o gráfico
    
    # Criar tabela de resultados
    df2 = create_table(results2)  # Cria a tabela de resultados
    print("\nResultados para o Problema 25.6:")  # Imprime uma mensagem
    print(df2)  # Imprime a tabela de resultados

    # Comparação de erros e esforço computacional
    f_num1 = sp.lambdify([x, y], func_expr1, modules=['numpy'])  # Converte a expressão simbólica para uma função numérica
    f_num2 = sp.lambdify([x, y], func_expr2, modules=['numpy'])  # Converte a expressão simbólica para uma função numérica

    # Você precisará calcular ou fornecer os valores exatos para y(2) e y(1) respectivamente
    exact_solution1 = y_analytic1[-1]  # Valor de y quando x = 2 para o problema 25.1
    exact_solution2 = y_analytic2[-1]  # Valor de y quando x = 1 para o problema 25.6

    comparison_results1 = compare_rk_methods(f_num1, 0, 1, 2, h_values, exact_solution1)  # Compara os métodos numéricos
    comparison_results2 = compare_rk_methods(f_num2, 0, 1, 1, h_values, exact_solution2)  # Compara os métodos numéricos

    fig_error1 = plot_error_vs_effort(comparison_results1)  # Cria o gráfico de erro vs. esforço computacional
    fig_error1.update_layout(title="Erro vs. Esforço para o Problema 25.1")  # Atualiza o título do gráfico
    fig_error1.show()  # Mostra o gráfico

    fig_error2 = plot_error_vs_effort(comparison_results2)  # Cria o gráfico de erro vs. esforço computacional
    fig_error2.update_layout(title="Erro vs. Esforço para o Problema 25.6")  # Atualiza o título do gráfico
    fig_error2.show()  # Mostra o gráfico

if __name__ == "__main__":
    main()  # Executa a função principal
