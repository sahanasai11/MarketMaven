from flask import Flask, render_template
from . import app
from . import networks


@app.route("/")
def index():
    curr_network = networks.Network("Basic", 5)
    path = "test.dot"
    curr_network.visualize_network(path)

    return render_template("index.html", network_path=path)