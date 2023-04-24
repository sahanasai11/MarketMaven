from flask import Flask, render_template, request
from . import app
from . import networks
from . import data_loader
from . import db
from MarketMaven import schemas

import os

global loader

def set_data():
    global loader
    loader = data_loader.DataLoader('../data/all_stocks_5yr.csv')

# For flask shell
@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'MonthlyTransaction': schemas.MonthlyTransaction}

@app.route("/", methods=['GET', 'POST'])
def index():

    if request.method == 'GET':
        return render_template("index.html", 
                            network_source=None, 
                            best_stocks=None,
                            exchange_name="Exchange")
    
    elif request.method == 'POST':

        ### TODO:
        # 1. change stock dictionary to be compatiable with new data and use price at the end of the month 
        #

        print(request.form)

        starting_amount = request.form['starting-amount']
        years_to_grow = request.form['years-to-grow']
        sectors = request.form['sectors']
        stocks = request.form['stocks']
        exchange = request.form['exchange']

        network_name = exchange + "_network_graph"
        curr_network = networks.Network(network_name, loader.stock_dict)
        top_decile_stocks = curr_network.get_stocks_by_percent(.10, True)
        bottom_decile_stocks = curr_network.get_stocks_by_percent(.10, False)
        path = os.path.join(network_name) + ".dot"
        src = curr_network.visualize_network(path)
        print(src)

        return render_template("index.html", 
                            network_source=src, 
                            top_decile_stocks=top_decile_stocks,
                            bottom_decile_stocks=bottom_decile_stocks,
                            exchange_name=exchange)

