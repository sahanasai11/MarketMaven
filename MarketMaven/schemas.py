from . import db

# Schemas

# Ticker symbols to permno mappings
class Ticker(db.Model):
    permno = db.Column(db.Integer, primary_key=True)
    ticker_symbol = db.Column(db.String, index=True)

    def __repr__(self):
        return '<Ticker = {}, permno = {}'.format(self.ticker, self.permno)
    

class MonthlyTransaction(db.Model):
    monthly_transaction_id = db.Column(db.Integer, primary_key=True)
    # unique identifier for a traded asset (unique to a company)
    permno = db.Column(db.Integer, db.ForeignKey('ticker.permno'), index=True)
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
        return '<Monthly_Transaction: ID = {}, permno = {}, date = {}, exchange = {}>'.format(self.monthly_transaction_id, self.permno, self.date, self.exchange)
    

# TODO: RUN FLASK DB MIGRATE AND FLASK DB UPGRADE SINCE THIS TABLE
# DOESNT EXIST IN SCRIPTS YET. WANT TO CHECK W HELEN FIRST
class MonthlyTransactionFFM(db.Model):
    monthly_transaction_ffm_id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, index=True)
    market_minus_risk_free = db.Column(db.Float, index=True)
    small_minus_big = db.Column(db.Float, index=True)
    high_minus_low = db.Column(db.Float, index=True)
    risk_free = db.Column(db.Float, index=True)
    market_rate = db.Column(db.Float, index=True)

    def __repr__(self):
        return '<Monthly_Transaction_FFM ID = {}, date = {}>'.format(self.monthly_transaction_ffm_id, self.date)