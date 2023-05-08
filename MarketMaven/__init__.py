import flask, csv
from flask_bootstrap import Bootstrap
from .config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import datetime 
import math 
import operator
import numpy as np

app = flask.Flask(__name__)
bootstrap = Bootstrap(app)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
adj_list = # load csv 


from MarketMaven.schemas import *


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