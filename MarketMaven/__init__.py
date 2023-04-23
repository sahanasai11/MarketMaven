import flask
from flask_bootstrap import Bootstrap
from MarketMaven.config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = flask.Flask(__name__)
bootstrap = Bootstrap(app)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

### This is to intialize loading data when the app is intialized. The data is 
### ONLY updated if the app is restarted, not the webpage refreshed
with app.app_context():
    from MarketMaven.views import set_data
    set_data()


# Schemas
class Monthly_Transaction(db.Model):

    monthly_transaction_id = db.Column(db.Integer, primary_key=True)
    # unique identifier for a traded asset (unique to a company)
    permno = db.Column(db.Integer, index=True)
    # date that the asset is traded;
    date = db.Column(db.Date, index=True)
    # type of security (we only have 10 (ordinary shares) 11 (common shares))
    share_type = db.Column(db.String, index=True)
    # Name of exchange
    exchange = db.Column(db.String, index=True)
    # end of month asset price 
    price = db.Column(db.Float, index=True)
    # returns of security after a month
    returns = db.Column(db.Float, index=True)
    # number of shares involved in transaction
    shares_outstanding = db.Column(db.Float, index=True)

    # for every month, the data has a unique permno
    permno_date_constraint = db.UniqueConstraint(permno, date)

    def __repr__(self):
        return '<Monthly_Transaction {}>'.format(self.monthly_transaction_id, self.permno, self.date, self.exchange)