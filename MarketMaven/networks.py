import networkx as nx
import graphviz
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
        self.data_path = 'data/industry_equal_data.csv'
        self.coeff_path = 'data/industry_equal.csv'
        self.ffm_path = 'data/ffm_industry.csv'
        ## here is where we would account for selected sectors
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


    def add_correlation_edges(self, graph, sectors, theta, data):
        # data here is previous 12 months 
        for i in sectors:
            for j in sectors:
                curr_corr = data[i].corr(data[j])
                if i != j and abs(curr_corr) > theta:
                    graph.add_edge(i, j)
        return graph
    

    def create_graph(self, data, sectors): 
        g = nx.Graph()
        g.add_nodes_from(sectors)
        g = self.add_correlation_edges(g , list(g.nodes), .55, data)
        return g


    def create_correlation_network(self):
        ## this is for all years  
        data = pd.read_csv(self.data_path)
        data = data.drop('index', axis=1)
        columns = (list(data.columns))[1:]
        g = self.create_graph(data, columns)
        return g
    
    ## This is already called 
    def solve_optimization_problem(self):
        return 1/3  

    ## This is already called 
    def find_average_centralities(self, graph):
        average_centrailites = dict()
        scale_factor = self.solve_optimization_problem()
        
        degree_centrality = nx.degree_centrality(graph)
        closeness_centrality = nx.closeness_centrality(graph)
        betweenness_centrality = nx.betweenness_centrality(graph)
        for node in graph.nodes():
            average_centrailites[node] = scale_factor * (degree_centrality[node]) + scale_factor *(closeness_centrality[node]) + scale_factor *(betweenness_centrality[node])       
        return average_centrailites
    

    ## This is already called 
    def find_monthly_graph(self, equal, data, start_date, end_date, max_date):
        ## for each date, find previous 11 months and find the graph (using data_equal) 
        columns = (list(data.columns))[1:]
        while end_date <= max_date:
            # find graph for that data 
            curr_data = data[(data['Date'] >= start_date) & (data['Date'] <= end_date)]
            curr_graph = self.create_graph(curr_data, columns)
            
            # find coefficents and add into the table
            average_centralities = self.find_average_centralities(curr_graph)
            
            for key in average_centralities.keys():
                equal.loc[(equal['Date'] == end_date) & (equal['Industry'] == key), 'Coeff'] = average_centralities[key]            
            
            # update date 
            start_date = start_date + pd.DateOffset(months=1) + pd.offsets.MonthEnd(0)
            end_date = end_date + pd.DateOffset(months=1) + pd.offsets.MonthEnd(0)



    def find_deciles(self, group):
        group['Decile'] = pd.qcut(group['SZE'].rank(method='first'), 10, labels=False)
        return group
    
    def find_weights(self, group):
        total_size = group['SZE'].sum()
        num_stocks = group['SZE'].count()
        group['EQ_weight'] = 1/float(num_stocks)
        group['VAL_weight'] = group['SZE']/total_size
        return group


    def get_portfolio(self):
        # this is the already dataframe where all monthly graphs have already been created as of now 
        data = pd.read_csv(self.coeff_path)
        ffm_data = pd.read_csv(self.ffm_path)

        ## sort data into deciles 
        data = data.groupby('Date').apply(self.find_deciles)
        data_short = data[data['Decile'] == 9]
        data_long = data[data['Decile'] == 0]

        ## find long and short returns 
        data_short = data_short.groupby('Date').apply(self.find_weights)
        data_short['EQ'] = data_short['Return'] * data_short['EQ_weight']
        data_short['VAL'] = data_short['Return'] * data_short['VAL_weight']
        data_short = data_short.reset_index()
        data_short = data_short.drop('index', axis=1)

        data_long = data_long.groupby('Date').apply(self.find_weights)
        data_long['EQ'] = data_long['Return'] * data_long['EQ_weight']
        data_long['VAL'] = data_long['Return'] * data_long['VAL_weight']
        data_long = data_long.reset_index()
        data_long = data_long.drop('index', axis=1)


        ## for each date, find the overall short and long portfolio which is just a sum 
        new_data = pd.DataFrame(columns=['Date', 'EQ', 'VAL'])
        new_data['Date'] = data_long['Date'].unique()


        ## find sum of industry returns depending on portfolio 
        eq_grouped_long = data_long.groupby('Date')['EQ'].sum().reset_index()
        eq_grouped_short = data_short.groupby('Date')['EQ'].sum().reset_index()
        new_data['EQ'] = eq_grouped_long['EQ'] - eq_grouped_short['EQ']
        val_grouped_long = data_long.groupby('Date')['VAL'].sum().reset_index()
        val_grouped_short = data_short.groupby('Date')['VAL'].sum().reset_index()
        new_data['VAL'] = val_grouped_long['VAL'] - val_grouped_short['VAL']

        ## Clean and merge data 
        ffm_data = ffm_data.rename(columns={'Mkt-RF': 'Mkt_RF'})
        ffm_data['Mkt'] = ffm_data.Mkt_RF + ffm_data.RF

        merged_data = pd.merge(new_data, ffm_data, how='inner', on=['Date'])
        merged_data['EQ_RF'] = merged_data['EQ'] - merged_data['RF']
        merged_data['VAL_RF'] = merged_data['VAL'] - merged_data['RF']

        return merged_data

















