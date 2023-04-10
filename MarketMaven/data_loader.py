import pandas as pd


class DataLoader():
    def __init__(self, path) -> None:
        self.path = path 
        print("Loading Data")
        self.data = pd.read_csv(path)
        print("Data Loaded")
        self.stock_dict = self.create_stock_dict()
    
    def create_stock_dict(self):
        stocks = set(self.data['Name'])
        stock_dict = {}
        for stock in stocks:
            stock_dict[stock] = []
        print("Creating Stock Dictionary")
        for i, row in self.data.iterrows():
            if '2018' in row['date']:
                stock_dict[row['Name']].append(dict(row))
        print("Done Creating Stock Dictionary")
        return stock_dict