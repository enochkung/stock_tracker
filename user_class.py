## User Class

from yahoo_fin import stock_info

class User:

    def __init__(self,username,password):
        self.id = None
        self.username = username
        self.password = password
        self.portfolio = Portfolio()        

class Portfolio:

    def __init__(self):

        self.top_level_info = {"free_funds": 0.0, "portfolio": 0.0, "invested": 0.0, "returns": 0.0}
        self.num_stock_purchased_dict = {"AAPL": 0, "HSBC": 0}
        self.purchase_value_dict = {"AAPL": 0.0, "HSBC": 0.0}
        self.monitored_stock = []
        self.purchased_stock = dict()
        self.monitor_stock_price_dict = dict()
        self.total_value_dict = dict()

    def get_total_value_dict(self):
        """ obtain total value of each stock """
        for stock in self.num_stock_purchased_dict:
            price = stock_info.get_live_price(stock)
            self.total_value_dict[stock] = self.num_stock_purchased_dict[stock]*price
    
    def buy(self,stock,quantity=None,value_amount=None):
        """ Buy stock at either quantity or the most quantity that is priced to less than value_amount. 
            Add to num_stock_purchased_dict and then get_total_value_dict"""
        pass

    def sell(self,stock,quantity):
        """ Sell stock at quantity. Update num_stock_purchased_dict and total_value_dict.  """
        pass

    def add_free_funds(self,free_funds):
        """ add to free funds """
        self.top_level_info['free_funds'] += free_funds

    def update_portolio_free_funds(self,value):
        """ after buying or selling, update portfolio and free funds """
        self.top_level_info['portfolio'] += value
        self.top_level_info['invested'] += value
        self.top_level_info['free_funds'] -= value

    def get_returns(self):
        """ calculate returns, i.e., percentage growth from investment to current portfolio value """
        if self.top_level_info['invested']:
            self.top_level_info['returns'] = (self.top_level_info['portfolio']-self.top_level_info['invested'])/self.top_level_info['invested']
        else:
            self.top_level_info['returns'] = 0

class Stock:

    def __init__(self, name):
        self.name = name
        self.get_price()
        self.get_history()

    def get_price(self):
        pass

    def get_history(self):
        pass
        





