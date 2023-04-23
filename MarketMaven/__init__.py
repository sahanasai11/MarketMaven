import flask
from flask_bootstrap import Bootstrap
from .config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = flask.Flask(__name__)
bootstrap = Bootstrap(app)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

### This is to intialize loading data when the app is intialized. The data is 
### ONLY updated if the app is restarted, not the webpage refreshed
# with app.app_context():
#     from views import set_data
#     set_data()