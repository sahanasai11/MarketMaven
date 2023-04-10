import pandas as pd


class DataLoader():
    def __init__(self, path) -> None:
        self.path = path 
        self.data = pd.read_csv(path)
        self.stock_dict = self.create_stock_dict()
    
    def create_stock_dict(self):
        stocks = set(self.data['Name'])
        stock_dict = {}
        for stock in stocks:
            stock_dict[stock] = []
        
        for i, row in self.data.iterrows():
            if '2018' in row['date']:
                stock_dict[row['Name']].append(dict(row))
        return stock_dict