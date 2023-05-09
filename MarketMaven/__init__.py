import flask, csv
from flask_bootstrap import Bootstrap
from .config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import datetime 
import math 
import operator
import numpy as np
import pandas as pd

app = flask.Flask(__name__)
bootstrap = Bootstrap(app)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
adj_list = pd.read_csv("adj_matrix.csv", index_col='index')

from MarketMaven.schemas import *

with app.app_context():

    # Populate Ticker table if empty
    if Ticker.query.count() == 0:
        with open('data/crsp_tickers.csv') as f:
            reader = csv.reader(f)
            header = next(reader)

            for i in reader:
                kwargs = {col: value for col, value in zip(header, i)}
                entry = Ticker(**kwargs)
                db.session.add(entry)

            db.session.commit()


            

