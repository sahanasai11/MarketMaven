from flask import Flask, render_template
from . import app
from . import networks
from . import data_loader

global loader

def set_data():
    global loader
    loader = data_loader.DataLoader('../all_stocks_5yr.csv')

@app.route("/")
def index():
    curr_network = networks.Network("Basic", loader.stock_dict)
    best_stocks = curr_network.get_top_stocks(.05)
    path = "test.dot"
    src = curr_network.visualize_network(path)
    return render_template("index.html", network_source=src, best_stocks=best_stocks)