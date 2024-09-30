import numpy as np
import pandas as pd
import sympy as sp
import plotly.graph_objects as go

def rk3(f, x0, y0, xf, h):
    x_list = [x0]
    y_list = [y0]
    
    x = x0
    y = y0
    
    while x < xf:
        if x + h > xf:
            h = xf - x
        
        k1 = f(x, y)
        k2 = f(x + h/2, y + h*k1/2)
        k3 = f(x + h, y - h*k1 + 2*h*k2)
        
        y += (h/6)*(k1 + 4*k2 + k3)
        x += h
        
        x_list.append(x)
        y_list.append(y)
    
    return x_list, y_list

def rk4(f, x0, y0, xf, h, full_output=False):
    x_list = [x0]
    y_list = [y0]
    
    x = x0
    y = y0
    
    while x < xf:
        if x + h > xf:
            h = xf - x
        
        k1 = f(x, y)
        k2 = f(x + h/2, y + h*k1/2)
        k3 = f(x + h/2, y + h*k2/2)
        k4 = f(x + h, y + h*k3)
        
        y += (h/6)*(k1 + 2*k2 + 2*k3 + k4)
        x += h
        
        x_list.append(x)
        y_list.append(y)
    
    if full_output:
        df = pd.DataFrame({'x': x_list, 'y': y_list})
        return df
    else:
        return x_list, y_list

def solve_ode(func_expr, x0, y0, xf, h_values):
    x = sp.Symbol('x')
    y = sp.Symbol('y')
    y_func = sp.Function('y')

    # Solução analítica
    eq = sp.Eq(y_func(x).diff(x), func_expr.subs(y, y_func(x)))
    try:
        y_analytic = sp.dsolve(eq, y_func(x), ics={y_func(x0): y0})
        y_analytic_func = sp.lambdify(x, y_analytic.rhs, modules=['numpy'])
    except NotImplementedError:
        print("Não foi possível encontrar uma solução analítica. Usando solução numérica de alta precisão.")
        y_analytic_func = None

    # Criar função numérica
    f_num = sp.lambdify([x, y], func_expr, modules=['numpy'])

    results = {}

    for method, rk_func in [("RK3", rk3), ("RK4", rk4)]:
        method_results = {}
        for h in h_values:
            x_list, y_list = rk_func(f_num, x0, y0, xf, h)
            method_results[h] = {'x': x_list, 'y': y_list}
        results[method] = method_results

    # Solução analítica ou numérica de alta precisão
    x_analytic = np.linspace(x0, xf, 1000)
    if y_analytic_func:
        y_analytic = y_analytic_func(x_analytic)
    else:
        # Usar RK4 com passo muito pequeno como aproximação da solução exata
        _, y_analytic = rk4(f_num, x0, y0, xf, (xf-x0)/10000)

    return results, x_analytic, y_analytic

def create_plots(results, x_analytic, y_analytic, func_str):
    
    fig_combined = go.Figure()
    
    for method in results:
        for h, data in results[method].items():
            fig_combined.add_trace(go.Scatter(
                x=data['x'],
                y=data['y'],
                mode='markers',
                name=f'{method}, h = {h}'
            ))
    
    fig_combined.add_trace(go.Scatter(
        x=x_analytic,
        y=y_analytic,
        mode='lines',
        name='Solução Analítica'
    ))
    
    fig_combined.update_layout(
        title=f'Resultados dos Métodos de Runge-Kutta para dy/dx = {func_str}',
        xaxis_title='x',
        yaxis_title='y',
        legend_title='Legenda'
    )
    
    return fig_combined

def create_table(results):
    df = pd.DataFrame()
    for method in results:
        for h, data in results[method].items():
            temp_df = pd.DataFrame({
                'x': data['x'],
                'y': data['y'],
                'Método': method,
                'h': h
            })
            df = pd.concat([df, temp_df], ignore_index=True)
    return df
    
def compare_rk_methods(func, x0, y0, xf, h_values, exact_solution):
    methods = {
        'RK3': rk3,
        'RK4': rk4,
    }
    
    results = {}
    
    for method_name, method_func in methods.items():
        method_results = []
        for h in h_values:
            x_list, y_list = method_func(func, x0, y0, xf, h)
            error = abs((y_list[-1] - exact_solution) / exact_solution) * 100
            computational_effort = len(x_list) - 1
            method_results.append({
                'h': h,
                'error': error,
                'effort': computational_effort
            })
        results[method_name] = method_results
    
    return results

def plot_error_vs_effort(results):
    fig = go.Figure()
    
    for method, data in results.items():
        errors = [point['error'] for point in data]
        efforts = [point['effort'] for point in data]
        
        fig.add_trace(go.Scatter(
            x=efforts,
            y=errors,
            mode='lines+markers',
            name=method
        ))
    
    fig.update_layout(
        title='Erro Relativo Percentual vs. Esforço Computacional',
        xaxis_title='Esforço Computacional (Número de Passos)',
        yaxis_title='Erro Relativo Percentual',
        yaxis_type="log",
        xaxis_type="log",
        yaxis=dict(range=[-6, 2])  # Ajusta a escala do eixo y de 10^-6 a 10^2
    )
    
    return fig

def main():
    # Exemplo de uso
    # Definindo a equação diferencial: dy/dx = 4*e^(0.8*x) - 0.5*y
    x = sp.Symbol('x')
    y = sp.Symbol('y')

    func_expr = 4*sp.exp(0.8*x) - 0.5*y
    
    x0 = 0
    y0 = 2
    xf = 4
    h_values = [1, 0.1, 0.01]

    results, x_analytic, y_analytic = solve_ode(func_expr, x0, y0, xf, h_values)
    fig = create_plots(results, x_analytic, y_analytic, func_str=str(func_expr))
    fig.show()
    
    # Criar tabela de resultados
    df = create_table(results)
    print(df.head())

    exact_solution = 75.33896

    # Criar função numérica
    f_num = sp.lambdify([x, y], func_expr, modules=['numpy'])

    comparison_results = compare_rk_methods(f_num, x0, y0, xf, h_values, exact_solution)
    fig2 = plot_error_vs_effort(comparison_results)
    fig2.show()

     # Equação 1: dy/dx = y*x^2 - 1.1*y
    func_expr1 = y*x**2 - 1.1*y
    
    x0 = 0
    y0 = 1
    xf = 2
    h_values = [0.5, 0.25]

    results1, x_analytic1, y_analytic1 = solve_ode(func_expr1, x0, y0, xf, h_values)
    fig1 = create_plots(results1, x_analytic1, y_analytic1, func_str=str(func_expr1))
    fig1.update_layout(title="Problema 25.1: dy/dx = y*x^2 - 1.1*y")
    fig1.show()
    
    # Criar tabela de resultados
    df1 = create_table(results1)
    print("Resultados para o Problema 25.1:")
    print(df1)

    # Problema 25.4 e 25.5 estão incluídos nos resultados acima

    # Problema 25.6
    # Equação 2: dy/dx = (1 + 2x)*sqrt(y)
    func_expr2 = (1 + 2*x)*sp.sqrt(y)
    
    x0 = 0
    y0 = 1
    xf = 1
    h_values = [0.5, 0.25]

    results2, x_analytic2, y_analytic2 = solve_ode(func_expr2, x0, y0, xf, h_values)
    fig2 = create_plots(results2, x_analytic2, y_analytic2, func_str=str(func_expr2))
    fig2.update_layout(title="Problema 25.6: dy/dx = (1 + 2x)*sqrt(y)")
    fig2.show()
    
    # Criar tabela de resultados
    df2 = create_table(results2)
    print("\nResultados para o Problema 25.6:")
    print(df2)

    # Comparação de erros e esforço computacional
    f_num1 = sp.lambdify([x, y], func_expr1, modules=['numpy'])
    f_num2 = sp.lambdify([x, y], func_expr2, modules=['numpy'])

    # Você precisará calcular ou fornecer os valores exatos para y(2) e y(1) respectivamente
    exact_solution1 = y_analytic1[-1]  # Valor de y quando x = 2 para o problema 25.1
    exact_solution2 = y_analytic2[-1]  # Valor de y quando x = 1 para o problema 25.6

    comparison_results1 = compare_rk_methods(f_num1, 0, 1, 2, h_values, exact_solution1)
    comparison_results2 = compare_rk_methods(f_num2, 0, 1, 1, h_values, exact_solution2)

    fig_error1 = plot_error_vs_effort(comparison_results1)
    fig_error1.update_layout(title="Erro vs. Esforço para o Problema 25.1")
    fig_error1.show()

    fig_error2 = plot_error_vs_effort(comparison_results2)
    fig_error2.update_layout(title="Erro vs. Esforço para o Problema 25.6")
    fig_error2.show()

if __name__ == "__main__":
    main()
