import flask, csv
from flask_bootstrap import Bootstrap
from .config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = flask.Flask(__name__)
bootstrap = Bootstrap(app)
app.config.from_object(Config)





            

