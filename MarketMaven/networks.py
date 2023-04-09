import networkx as nx
import matplotlib.pyplot as plt
import graphviz


class Network():
    def __init__(self, name, num_nodes=1, edges=[]) -> None:
        self.name = name 
        self.network= nx.Graph()
        for i in range(num_nodes):
            self.network.add_node(i)
    
    def get_network(self):
        return self.network 
    
    def get_name(self):
        return self.name 
    
    def add_edges(self, edges):
        for node_1, node_2 in edges:
            self.network.add_edge(node_1, node_2)
    
    def visualize_network(self, path):
        nx.drawing.nx_agraph.write_dot(self.network, path)
        return graphviz.Source.from_file(path).source



