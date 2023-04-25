import networkx as nx
import matplotlib.pyplot as plt
import graphviz
import math 
from . import db
from MarketMaven.schemas import * 

class Network():

    '''
    name: Name of network
    stock_dict: Dictionary representation of stock network where key is stock ticker symbol,
                value is list dictionaries where each dictionary signifies data for a day
                for a stock
    '''
    def __init__(self, name, exchange) -> None:
        self.name = name 
        self.exchange = exchange
        self.network= self.create_correlation_network()
    

    def get_network(self):
        return self.network 
    

    def get_name(self):
        return self.name 
    

    def add_edges(self, edges):
        for node_1, node_2 in edges:
            self.network.add_edge(node_1, node_2)
    
    def add_attributes(self, g, font_name, graph_label, node_color, edge_color):
        g.graph_attr['layout'] = "sfdp"
        g.graph_attr['overlap'] = "prism"
        g.graph_attr['fontname'] = font_name
        g.graph_attr['label'] = graph_label

        g.node_attr['fontname'] = font_name
        g.node_attr['color'] = node_color
        g.node_attr['style'] = "filled"

        g.edge_attr['fontname'] = font_name
        g.edge_attr['color'] = edge_color
        return g

    
    def visualize_network(self, path):
        nx.drawing.nx_agraph.write_dot(self.network, path)
        graphviz_source = graphviz.Source.from_file(path)
        graphviz_g = graphviz.Graph()
        
        source_lines = str(graphviz_source).splitlines()
        source_lines.pop(0)
        source_lines.pop(-1)
        graphviz_g.body += source_lines
        graphviz_g = self.add_attributes(graphviz_g, "Courier", self.name, "darkseagreen4", "coral4")

        return graphviz_g.source
    
    def mean(self, permno_i_lst):
        mean = 0

        for item in permno_i_lst:
            mean += item[1]
        return mean/len(permno_i_lst)
    
    def cross_correlation(self, permno_i, permno_j):
        cross_c = 0
        numerator = 0
        denom_i = 0 
        denom_j = 0

        permno_i_lst = db.session.query(MonthlyTransaction.date, MonthlyTransaction.returns).filter(MonthlyTransaction.permno == permno_i).all()
        permno_j_lst = db.session.query(MonthlyTransaction.date, MonthlyTransaction.returns).filter(MonthlyTransaction.permno == permno_j).all()
        mean_i = self.mean(permno_i, permno_i_lst)
        mean_j = self.mean(permno_j, permno_j_lst)

        for item_i in permno_i_lst:
            for item_j in permno_j_lst:

                if item_i[0] == item_j[0]:
                    numerator += (item_i[1] - mean_i) * (item_j[1] - mean_j)
                    denom_i += (item_i[1] - mean_i)**2
                    denom_j += (item_j[1] - mean_j)**2
                    

        return numerator/(math.sqrt(denom_i) * math.sqrt(denom_j))


    def create_correlation_matrix(self, permnos):
        lst = []
        for i in permnos:
            sub_lst = []
            for j in permnos:
                sub_lst.append(self.cross_correlation(i, j))
            lst.append(sub_lst)
        return lst 


    def adj_matrix(self, correlation_matrix, theta):
        lst = []
        for row_index in range(len(correlation_matrix)):
            sub_lst = []
            for col_index in range(len(correlation_matrix[row_index])):
                if row_index != col_index and abs(correlation_matrix[row_index][col_index]) > theta:
                    sub_lst.append(1)
                else:
                    sub_lst.append(0)
            lst.append(sub_lst)
        return lst


    def create_correlation_network(self):
        g = nx.Graph()
        
        permnos = db.session.query(MonthlyTransaction.permno).distinct().all()
        for i in range(len(permnos)):
            permnos[i] = permnos[i][0]
            g.add_node(permnos[i])
       
        adj_list = self.adj_matrix(self.create_correlation_matrix(permnos),theta=.9)

        for row_index in range(len(adj_list)):
            for col_index in range(len(adj_list[row_index])):
                if adj_list[row_index][col_index]:
                    g.add_edge(permnos[row_index], permnos[col_index])
        return g
    

    def solve_optimization_problem(self):
        return 1/3  

    def find_average_centralities(self):
        average_centrailites = dict()
        graph = self.network
        scale_factor = self.solve_optimization_problem()
        
        degree_centrality = nx.degree_centrality(graph)
        closeness_centrality = nx.closeness_centrality(graph)
        betweenness_centrality = nx.betweenness_centrality(graph)
        
        for node in graph.nodes():
            average_centrailites[node] = scale_factor * (degree_centrality[node] + closeness_centrality[node] + betweenness_centrality[node])
            
            
        return average_centrailites
    
    def get_stocks_by_percent(self, percent, reverse):
        graph = self.network
        c_avgs = self.find_average_centralities()
        sorted_c_avgs = sorted(c_avgs, key=c_avgs.get, reverse=reverse)
        num_stocks = math.floor(percent * len(c_avgs.keys()))
        return sorted_c_avgs[:num_stocks]




