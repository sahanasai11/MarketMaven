from flask import Flask, render_template
from . import app
from . import networks


@app.route("/")
def index():
    curr_network = networks.Network("Basic", 5)
    curr_network.add_edges([(1, 2), (2,3), (3, 4), (1,3), (4,0)])
    path = "test.dot"
    src = curr_network.visualize_network(path)

    return render_template("index.html", network_source=src)