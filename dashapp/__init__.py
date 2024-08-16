from dash import Dash
from segredos import SECRET_KEY

# Inicializando o aplicativo Dash
app = Dash(__name__, url_base_pathname='/')
server = app.server
app.config.suppress_callback_exceptions = True

server.config.update(
    SQLALCHEMY_DATABASE_URI='sqlite:///db.sqlite3',
    SECRET_KEY= SECRET_KEY,
    SQLALCHEMY_TRACK_MODIFICATIONS=False
)



from dashapp import views  # noqa: E402, F401
