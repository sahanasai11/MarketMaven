from flask import Flask, render_template, request
from . import app
from . import networks
from . import data_loader

import os

global loader

def set_data():
    global loader
    loader = data_loader.DataLoader('../all_stocks_5yr.csv')

@app.route("/", methods=['GET', 'POST'])
def index():

    if request.method == 'GET':
        return render_template("index.html", 
                            network_source=None, 
                            best_stocks=None,
                            exchange_name="Exchange")
    
    elif request.method == 'POST':

        print(request.form)

        starting_amount = request.form['starting-amount']
        years_to_grow = request.form['years-to-grow']
        sectors = request.form['sectors']
        stocks = request.form['stocks']
        exchange = request.form['exchange']

        network_name = exchange + "_network_graph"
        curr_network = networks.Network(network_name, loader.stock_dict)
        best_stocks = curr_network.get_top_stocks(.05)
        path = os.path.join(network_name) + ".dot"
        src = curr_network.visualize_network(path)

        return render_template("index.html", 
                            network_source=src, 
                            best_stocks=best_stocks,
                            exchange_name=exchange)

