import flask, csv
from flask_bootstrap import Bootstrap
from .config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = flask.Flask(__name__)
bootstrap = Bootstrap(app)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from MarketMaven.schemas import *

from datetime import datetime

### This is to intialize loading data when the app is intialized. The data is 
### ONLY updated if the app is restarted, not the webpage refreshed
# with app.app_context():
#     from views import set_data
#     set_data()

with app.app_context():

    # Populate MonthlyTransaction table if empty
    if MonthlyTransaction.query.count() == 0:
        with open('data/monthly_stock.csv') as f:
            print('populating MonthlyTransaction table')
            reader = csv.reader(f)
            header = next(reader)

            for i in reader:
                kwargs = {col: value for col, value in zip(header, i)}
                kwargs['date'] = datetime.strptime(kwargs['date'], '%Y-%m-%d').date()
                entry = MonthlyTransaction(**kwargs)
                db.session.add(entry)

            print(header)
            db.session.commit()

            

    print('MonthlyTransaction table populated')

