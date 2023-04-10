from flask import Flask, render_template
from . import app
from . import networks
from . import data_loader


@app.route("/")
def index():

    loader = data_loader.DataLoader('../all_stocks_5yr.csv')

    curr_network = networks.Network("Basic", loader.stock_dict)
    path = "test.dot"
    src = curr_network.visualize_network(path)
    return render_template("index.html", network_source=src)