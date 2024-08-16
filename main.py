from dashapp import app

# Iniciando o aplicativo
if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)
    # modo de produção
    # app.run_server(debug=False, host='0.0.0.0')