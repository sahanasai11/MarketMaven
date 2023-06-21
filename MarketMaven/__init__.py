import flask, csv
from flask_bootstrap import Bootstrap
from .config import Config

app = flask.Flask(__name__)
bootstrap = Bootstrap(app)
app.config.from_object(Config)





            

