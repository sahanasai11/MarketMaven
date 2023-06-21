import networkx as nx
import graphviz
from MarketMaven.schemas import * 
import pandas as pd

# need to import global data_list
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
        self.adj_matrix_path = "data/adj_matrix_" + exchange + ".csv"
        self.coeff_path = "data/coeffs_" + exchange + ".csv"
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
        print(path)
        nx.drawing.nx_agraph.write_dot(self.network, path)
        graphviz_source = graphviz.Source.from_file(path)
        graphviz_g = graphviz.Graph()
        
        source_lines = str(graphviz_source).splitlines()
        source_lines.pop(0)
        source_lines.pop(-1)
        graphviz_g.body += source_lines
        graphviz_g = self.add_attributes(graphviz_g, "Courier", self.name, "darkseagreen4", "coral4")

        return graphviz_g.source

    def create_correlation_network(self):
        A1 = pd.read_csv(self.adj_matrix_path, index_col='index')
        A2 = pd.DataFrame(A1.values, index=A1.columns, columns=A1.columns)
        g = nx.from_pandas_adjacency(A2)    
        return g
    

    def solve_optimization_problem(self):
        return 1/3  


    def find_average_centralities(self):
        average_centrailites = dict()
        scale_factor = self.solve_optimization_problem()
        graph = self.network
        
        degree_centrality = nx.degree_centrality(graph)
        closeness_centrality = nx.closeness_centrality(graph)
        betweenness_centrality = nx.betweenness_centrality(graph)
        for node in graph.nodes():
            average_centrailites[node] = scale_factor * (degree_centrality[node] + closeness_centrality[node] + betweenness_centrality[node])        
        return average_centrailites
    

    def calc_weights(self, group):
        total_size = group['size'].sum()
        num_stocks = group['size'].count()
        group['eq_weight'] = 1/float(num_stocks)
        group['val_weight'] = group['size']/total_size
        return group
    

    def get_month(self, row):
        return row[5:7]

    def get_year(self, row):
        return row[0:4]


    def get_portfolio(self, num_divisions):
        data = pd.read_csv('data/monthly_stock.csv')
        exch = pd.read_csv(self.coeff_path, index_col='index')
        exch_data = data.merge(exch, how='inner', on='permno')

        #at last date, find the long short portfolio 
        last_date = exch_data[exch_data['date'] == '2020-12-31']
        last_date['decile'] = pd.qcut(last_date['coeff'].rank(method='first'), num_divisions, labels=False)

        # long short stocks 
        long_stocks = list(last_date[last_date['decile'] == 9]['permno'].values)
        short_stocks = list(last_date[last_date['decile'] == 0]['permno'].values)

        exch_data['size'] = exch_data['shares_outstanding'] * exch_data['price']

        ## create two differenet data frames, one for short and one for long 
        exch_short = exch_data[exch_data['permno'].isin(short_stocks)]
        exch_short = exch_short.reset_index()
        exch_short = exch_short.drop('index', axis=1)

        exch_long = exch_data[exch_data['permno'].isin(long_stocks)]
        exch_long = exch_long.reset_index()
        exch_long = exch_long.drop('index', axis=1)


        ## find all weights and returns for both long, short portfolios
        exch_long = exch_long.groupby('date', group_keys=True).apply(self.calc_weights)
        exch_short = exch_short.groupby('date', group_keys=True).apply(self.calc_weights)

        exch_long['EQ'] = exch_long['eq_weight'] * exch_long['returns']
        exch_long['VAL'] = exch_long['val_weight'] * exch_long['returns']
        exch_short['EQ'] = exch_short['eq_weight'] * exch_short['returns']
        exch_short['VAL'] = exch_short['val_weight'] * exch_short['returns']


        ## Create a new returns table 
        returns_table = pd.DataFrame()
        returns_table['EQ_long'] = exch_long['EQ'].groupby('date').sum() * 100
        returns_table['EQ_short'] = exch_short['EQ'].groupby('date').sum() * 100
        returns_table['EQ'] = returns_table['EQ_long'] - returns_table['EQ_short'] 

        returns_table['VAL_long'] = exch_long['VAL'].groupby('date').sum() * 100
        returns_table['VAL_short'] = exch_short['VAL'].groupby('date').sum() * 100 
        returns_table['VAL'] = returns_table['VAL_long'] - returns_table['VAL_short'] 

        returns_table = returns_table.reset_index()


        returns_table['month'] = returns_table['date'].apply(self.get_month)
        returns_table['year'] = returns_table['date'].apply(self.get_year)

        ffm = pd.read_csv('data/monthly_stock_ffm.csv')
        ffm['month'] = ffm['date'].apply(self.get_month)
        ffm['year'] = ffm['date'].apply(self.get_year)


        merged_data = returns_table.merge(ffm, how='inner', on=['month', 'year'])
        merged_data = merged_data.drop(['date_x', 'year', 'month'], axis=1)
        merged_data = merged_data.rename(columns={'date_y': 'Date'})
        merged_data['EQ_RF'] = merged_data['EQ'] - merged_data['risk_free']

        return merged_data











