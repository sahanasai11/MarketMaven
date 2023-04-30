import flask, csv
from flask_bootstrap import Bootstrap
from .config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import math 


app = flask.Flask(__name__)
bootstrap = Bootstrap(app)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
adj_list = []


def mean(permno_i_lst):
    mean = 0

    for item in permno_i_lst:
        mean += item[1]
    return mean/len(permno_i_lst)


def cross_correlation(permno_i, permno_j):
    numerator = 0
    denom_i = 0 
    denom_j = 0
    print(type(permno_i))
    permno_i_lst = db.session.query(MonthlyTransaction.date, MonthlyTransaction.returns).filter(MonthlyTransaction.permno == permno_i).all()
    permno_j_lst = db.session.query(MonthlyTransaction.date, MonthlyTransaction.returns).filter(MonthlyTransaction.permno == permno_j).all()
    ##### not getting list values 
    print(permno_i_lst)
    print(permno_j_lst)
    mean_i = mean(permno_i_lst)
    mean_j = mean(permno_j_lst)

    for item_i in permno_i_lst:
        for item_j in permno_j_lst:

            if item_i[0] == item_j[0]:
                numerator += (item_i[1] - mean_i) * (item_j[1] - mean_j)
                denom_i += (item_i[1] - mean_i)**2
                denom_j += (item_j[1] - mean_j)**2
                
    ## getting probelm of dividng by 0, so instead set the denominators to very small values of 1e-7
    if denom_i == 0:
        denom_i = 1e-7
    if denom_j == 0:
        denom_j = 1e-7
    return numerator/(math.sqrt(denom_i) * math.sqrt(denom_j))


def create_correlation_matrix(permnos):
    lst = []
    for i in permnos:
        sub_lst = []
        for j in permnos:
            sub_lst.append(cross_correlation(i, j))
        lst.append(sub_lst)
    return lst 


def adj_matrix(correlation_matrix, theta):
    lst = []
    for row_index in range(len(correlation_matrix)):
        sub_lst = []
        for col_index in range(len(correlation_matrix[row_index])):
            if row_index != col_index and abs(correlation_matrix[row_index][col_index]) > theta:
                sub_lst.append(1)
            else:
                sub_lst.append(0)
        lst.append(sub_lst)
    return lst


from MarketMaven.schemas import *
from datetime import datetime

### This is to intialize loading data when the app is intialized. The data is 
### ONLY updated if the app is restarted, not the webpage refreshed
# with app.app_context():
#     from views import set_data
#     set_data()

with app.app_context():

    # Populate MonthlyTransaction table if empty
    # if MonthlyTransaction.query.count() == 0:
    #     with open('data/monthly_stock.csv') as f:
    #         print('populating MonthlyTransaction table')
    #         reader = csv.reader(f)
    #         header = next(reader)

    #         for i in reader:
    #             kwargs = {col: value for col, value in zip(header, i)}
    #             kwargs['date'] = datetime.strptime(kwargs['date'], '%Y-%m-%d').date()
    #             entry = MonthlyTransaction(**kwargs)
    #             db.session.add(entry)

    #         print(header)
    #         db.session.commit()
    #     print('MonthlyTransaction table populated')
    #     print("Creating adjancecy list")
    #     permnos = db.session.query(MonthlyTransaction.permno).distinct().all()
    #     adj_list = adj_matrix(create_correlation_matrix(permnos),theta=.9) 
    print("Finished adjancecy list")



            

