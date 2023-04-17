import networkx as nx
import matplotlib.pyplot as plt
import graphviz
import math 


class Network():
    def __init__(self, name, stock_dict={}) -> None:
        self.name = name 
        self.stock_dict = stock_dict
        self.network= self.create_correlation_network()
        
    
    def get_network(self):
        return self.network 
    
    def get_name(self):
        return self.name 
    
    def add_edges(self, edges):
        for node_1, node_2 in edges:
            self.network.add_edge(node_1, node_2)
    
    def visualize_network(self, path):
        nx.drawing.nx_agraph.write_dot(self.network, path)
        graphviz_source = graphviz.Source.from_file(path)
        graphviz_g = graphviz.Graph()
        source_lines = str(graphviz_source).splitlines()
        source_lines.pop(0)
        source_lines.pop(-1)
        graphviz_g.body += source_lines

        graphviz_g.graph_attr['layout'] = "sfdp"
        graphviz_g.graph_attr['overlap'] = "prism"

        return graphviz_g.source
    
    def mean(self, stock_i):
        mean = 0
        for item in self.stock_dict[stock_i]:
            mean += item['close']
        return mean/len(self.stock_dict[stock_i])
    
    def cross_correlation(self, stock_i, stock_j):
        cross_c = 0
        numerator = 0
        denom_i = 0 
        denom_j = 0
        mean_i = self.mean(stock_i)
        mean_j = self.mean(stock_j)

        for item_i in self.stock_dict[stock_i]:
            for item_j in self.stock_dict[stock_j]:
                if item_i['date'] == item_j['date']:
                    numerator += (item_i['close'] - mean_i) * (item_j['close'] - mean_j)
                    denom_i += (item_i['close'] - mean_i)**2
                    denom_j += (item_j['close'] - mean_j)**2
                    

        return numerator/(math.sqrt(denom_i) * math.sqrt(denom_j))

    def create_correlation_matrix(self):
        lst = []
        for i in self.stock_dict.keys():
            sub_lst = []
            for j in self.stock_dict.keys():
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
        for key in self.stock_dict.keys():
            g.add_node(key)
            
        adj_list = self.adj_matrix(self.create_correlation_matrix(),theta=.9)
        dict_keys = list(self.stock_dict.keys())
        
        for row_index in range(len(adj_list)):
            for col_index in range(len(adj_list[row_index])):
                if adj_list[row_index][col_index]:
                    g.add_edge(dict_keys[row_index], dict_keys[col_index])
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
    
    def get_top_stocks(self, top_percent):
        graph = self.network
        c_avgs = self.find_average_centralities()
        sorted_c_avgs = sorted(c_avgs, key=c_avgs.get, reverse=True)
        num_stocks = math.floor(top_percent * len(c_avgs.keys()))
        return sorted_c_avgs[:num_stocks]




