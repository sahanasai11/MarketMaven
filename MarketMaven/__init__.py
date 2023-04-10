import flask
from flask_bootstrap import Bootstrap

app = flask.Flask(__name__)
bootstrap = Bootstrap(app)

### This is to intialize loading data when the app is intialized. The data is 
### ONLY updated if the app is restarted, not the webpage refreshed
with app.app_context():
    from MarketMaven.views import set_data
    set_data()