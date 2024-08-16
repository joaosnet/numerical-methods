from dash import Dash
from segredos import SECRET_KEY

# script externo para adicionar o keyboard mathlive
MATHLIVE = """
https://unpkg.com/mathlive"""

external_scripts = [
    {
        "type": "text/javascript",
        "id": "MathLive-script",
        "src": MATHLIVE,
    },
]

# Inicializando o aplicativo Dash
app = Dash(__name__, url_base_pathname="/", external_scripts=external_scripts)
server = app.server
app.config.suppress_callback_exceptions = True

server.config.update(
    SQLALCHEMY_DATABASE_URI="sqlite:///db.sqlite3",
    SECRET_KEY=SECRET_KEY,
    SQLALCHEMY_TRACK_MODIFICATIONS=False,
)


from dashapp import views  # noqa: E402, F401
