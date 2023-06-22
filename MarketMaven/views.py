from flask import Flask, render_template, request, jsonify
from . import app
from . import networks
from MarketMaven.financial_models import *

import os

DOTFILE_PATH = 'dot'

@app.route("/", methods=['GET', 'POST'])
def index():

    if request.method == 'GET':
        return render_template("index.html", 
                            network_source=None, 
                            exchange_name="Exchange")
    
    elif request.method == 'POST':
        
        sectors = request.form.getlist('sectors')
        exchange = request.form['exchange']
        print('EXCHANGE: ' + exchange)
        network_name = "industries network graph"

        print("starting creating network")

        curr_network = networks.Network(network_name, exchange)
        print("finished creating network")

        curr_portfolio = curr_network.get_portfolio()
        print("MEAN MONTHLY RETURNS")
        print(f"FF Equal Portfolio: {compute_monthly_average(curr_portfolio[curr_portfolio['Date'] > '1999-12-31']['EQ'])}")
        print()
        print("MONTHLY VOLATILITY")
        print(f"FF Equal Portfolio: {compute_monthly_volatility(curr_portfolio[curr_portfolio['Date'] > '1999-12-31']['EQ'])}")
        print()
        print("MONTHLY SHARPE RATIO")
        print(f"FF Equal Portfolio: {compute_monthly_sharpe_ratio(curr_portfolio[curr_portfolio['Date'] > '1999-12-31']['EQ'], curr_portfolio[curr_portfolio['Date'] > '1999-12-31']['RF'])}")
        print()

        path = os.path.join(DOTFILE_PATH, network_name) + ".dot"
        print("starting visualizing network")
        src = curr_network.visualize_network(path)
        print("finished visualizing network")  

        
        json_resp = {
            'network_source': src,
            'network_img' : 'static/img/' + exchange + '.png',
            'network_capm' :'static/img/' + exchange + '_capm.png',
            'exchange_name' : exchange,
            'FF Equal Portfolio' : {
                'Mean Monthly Returns' : compute_monthly_average(curr_portfolio[curr_portfolio['Date'] > '1999-12-31']['EQ']),
                'Monthly Volatility' : compute_monthly_volatility(curr_portfolio[curr_portfolio['Date'] > '1999-12-31']['EQ']),
                'Sharpe Ratio' : compute_monthly_sharpe_ratio(curr_portfolio[curr_portfolio['Date'] > '1999-12-31']['EQ'], curr_portfolio[curr_portfolio['Date'] > '1999-12-31']['RF'])
                }
            }        
        
        return jsonify(json_resp)
