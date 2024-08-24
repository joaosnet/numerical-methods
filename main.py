import os
from dashapp import app


# Iniciando o aplicativo
if __name__ == "__main__":
    # Definir o modo a partir da variável de ambiente
    mode = os.getenv("DEBUG")
    if mode == 0:
        app.run_server(debug=True)
    elif mode == 1:
        app.run_server(debug=False, host="0.0.0.0")
    else:
        app.run_server(debug=True)
