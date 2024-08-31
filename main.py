import os
from dashapp import app, server  # noqa: F401


# Iniciando o aplicativo
if __name__ == "__main__":
    # Definir o modo a partir da variável de ambiente
    mode = os.getenv("DEBUG")
    if mode == "0":
        app.run(debug=True)
    elif mode == "1":
        app.run(debug=False, host="0.0.0.0")
    else:
        print("Variavel Ambiente DEBUG não definida.")
        app.run()
