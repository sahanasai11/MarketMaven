from flask import Flask, render_template, request
from . import app
from . import networks
from . import db
from MarketMaven import schemas
from MarketMaven.financial_models import *

import os


# For flask shell
@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'Ticker': schemas.Ticker}

@app.route("/", methods=['GET', 'POST'])
def index():

    tickers = db.session.query(schemas.Ticker.ticker_symbol).distinct().all()

    if request.method == 'GET':
        return render_template("index.html", 
                            network_source=None, 
                            best_stocks=None,
                            exchange_name="Exchange",
                            tickers=tickers)
    
    elif request.method == 'POST':

        print(request.form)

        #starting_amount = request.form['starting-amount']
        #years_to_grow = request.form['years-to-grow']
        #sectors = request.form.getlist('sectors')
        #stocks = request.form.getlist('stocks')
        exchange = request.form['exchange']
        network_name = exchange + "_network_graph"
        print("starting creating network")
        print(exchange)

        
        curr_network = networks.Network(network_name, exchange)
        print("finished creating network")
        curr_portfolio = curr_network.get_portfolio(10)

        print("MEAN MONTHLY RETURNS")
        print(f"FF Equal Portfolio: {compute_monthly_average(curr_portfolio['EQ'])}")
        print()
        print("MONTHLY VOLATILITY")
        print(f"FF Equal Portfolio: {compute_monthly_volatility(curr_portfolio['EQ'])}")
        print()
        print("MONTHLY SHARPE RATIO")
        print(f"FF Equal Portfolio: {compute_monthly_sharpe_ratio(curr_portfolio['EQ'], curr_portfolio['risk_free'])}")
        print()

        path = os.path.join(network_name) + ".dot"
        print("starting visualizing network")
        src = curr_network.visualize_network(path)
        print("finished visualizing network")
        #print(src)
        

        return render_template("index.html", 
                            network_source=src, 
                            network_img='static/img/' + exchange + '.png',
                            network_capm='static/img/' + exchange + '_capm.png',
                            top_decile_stocks='', # parse through later 
                            bottom_decile_stocks='', # parse through later 
                            exchange_name=exchange,
                            tickers=tickers)

