from dash import Dash, _dash_renderer
from segredos import SECRET_KEY
import dash_mantine_components as dmc

_dash_renderer._set_react_version("18.2.0")

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
app = Dash(
    __name__,
    title="DashBoard de Métodos Númericos",
    url_base_pathname="/",
    external_scripts=external_scripts,
    external_stylesheets=dmc.styles.ALL
)
server = app.server
app.config.suppress_callback_exceptions = True

server.config.update(
    SQLALCHEMY_DATABASE_URI="sqlite:///db.sqlite3",
    SECRET_KEY=SECRET_KEY,
    SQLALCHEMY_TRACK_MODIFICATIONS=False,
)


from dashapp import views  # noqa: E402, F401
