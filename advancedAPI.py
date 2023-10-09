import requests
import pandas as pd

base_url = "https://yahoo-finance127.p.rapidapi.com/"

headers = {
	"X-RapidAPI-Key": "380394e003msh093fbd9d9478c11p19ea7ajsn745a00e7cf1d",
	"X-RapidAPI-Host": "yahoo-finance127.p.rapidapi.com"
}

response = requests.get(base_url, headers=headers)

def fetch_balance_sheet(ticker):
    balance_sheet_url = f"https://yahoo-finance127.p.rapidapi.com/balance-sheet/{ticker}"
    response = requests.get(balance_sheet_url, headers=headers)
    return response.json()

#balance sheet method to grab url
"""
balance_sheet_url = f"https://yahoo-finance127.p.rapidapi.com/balance-sheet/{ticker}"
balance_sheet_response = requests.get(balance_sheet_url, headers=headers)
balance_sheet_data = balance_sheet_response.json()

stockholder_equity = data.get('totalStockholderEquity', {}).get('raw')
total_assets = data.get('totalAssets', {}).get('raw')
total_liab = data.get('totalLiab', {}).get('raw')
total_current_assets = data.get('totalCurrentAssets', {}).get('raw')
"""

def fetch_total_assets(ticker):
    data = fetch_balance_sheet(ticker)
    total_assets = data.get('totalAssets', {}).get('raw')
    return total_assets

def fetch_total_liabilities(ticker):
    data = fetch_balance_sheet(ticker)
    total_liabilities = data.get('totalLiab', {}).get('raw')
    return total_liabilities

def fetch_total_stockholder_equty(ticker):
    data = fetch_balance_sheet(ticker)
    stockholder_equity = data.get('totalStockholderEquity', {}).get('raw')
    return stockholder_equity

print(fetch_total_stockholder_equty('tsla'))
class Stock:
    def __init__(self,name,ticker):
        self.name = name
        self.ticker = ticker
        self.assets = fetch_total_assets(ticker= ticker)
        self.liabilities = fetch_total_liabilities(ticker=ticker)
        self.equity = fetch_total_assets(ticker= ticker)
    #assets    
    @property    
    def fetch_asset_list(self):
        ticker = self.ticker
        data = fetch_balance_sheet(ticker)
    
    # Extracting data and placing into a DataFrame
        asset_df = pd.DataFrame({
        'cash': [data.get('cash', {}).get('raw', None)],
        'shortTermInvestments': [data.get('shortTermInvestments', {}).get('raw', None)],
        'netReceivables': [data.get('netReceivables', {}).get('raw', None)],
        'inventory': [data.get('inventory', {}).get('raw', None)],
        'otherCurrentAssets': [data.get('otherCurrentAssets', {}).get('raw', None)],
        'totalCurrentAssets': [data.get('totalCurrentAssets', {}).get('raw', None)],
        'propertyPlantEquipment': [data.get('propertyPlantEquipment', {}).get('raw', None)],
        'goodWill': [data.get('goodWill', {}).get('raw', None)],
        'intangibleAssets': [data.get('intangibleAssets', {}).get('raw', None)],
        'otherAssets': [data.get('otherAssets', {}).get('raw', None)],
        'totalAssets': [data.get('totalAssets', {}).get('raw', None)]
    }, index=[ticker])
        return asset_df
    #liabilties
    @property
    def fetch_liabilities_list(self):
        ticker = self.ticker
        data = fetch_balance_sheet(ticker)
        
        # Extracting data and placing into a DataFrame
        liability_df = pd.DataFrame({
            'accountsPayable': [data.get('accountsPayable', {}).get('raw', None)],
            'shortLongTermDebt': [data.get('shortLongTermDebt', {}).get('raw', None)],
            'otherCurrentLiab': [data.get('otherCurrentLiab', {}).get('raw', None)],
            'longTermDebt': [data.get('longTermDebt', {}).get('raw', None)],
            'otherLiab': [data.get('otherLiab', {}).get('raw', None)],
            'minorityInterest': [data.get('minorityInterest', {}).get('raw', None)],
            'totalCurrentLiabilities': [data.get('totalCurrentLiabilities', {}).get('raw', None)],
            'totalLiab': [data.get('totalLiab', {}).get('raw', None)]
        }, index=[ticker])    
        return liability_df
    #equity
    @property
    def fetch_equity_list(self):
        ticker = self.ticker
        data = fetch_balance_sheet(ticker)
        
        # Extracting equity data and placing into a DataFrame
        equity_df = pd.DataFrame({
            'commonStock': [data.get('commonStock', {}).get('raw', None)],
            'retainedEarnings': [data.get('retainedEarnings', {}).get('raw', None)],
            'treasuryStock': [data.get('treasuryStock', {}).get('raw', None)],
            'capitalSurplus': [data.get('capitalSurplus', {}).get('raw', None)],
            'otherStockholderEquity': [data.get('otherStockholderEquity', {}).get('raw', None)],
            'totalStockholderEquity': [data.get('totalStockholderEquity', {}).get('raw', None)],
            'netTangibleAssets': [data.get('netTangibleAssets', {}).get('raw', None)]
        }, index=[ticker])
        
        return equity_df
    def fetch_combined_data(self):
        asset_df = self.fetch_asset_list
        liability_df = self.fetch_liabilities_list
        equity_df = self.fetch_equity_list
        
        combined_df = pd.concat([asset_df, liability_df, equity_df], axis=1)
        return combined_df



########################
INPUT DATA INTO DATABASE
########################

import sqlite3
from file import Stock

conn = sqlite3.connect('stocks.db')  # This will create a new file 'stocks.db' or connect to it if it exists
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS stock_data (
    ticker TEXT PRIMARY KEY,
    name TEXT,
    assets INT,
    liabilities INT,
    equity INT,
    asset_list TEXT,
    liabilities_list TEXT,
    equity_list TEXT
)
''')
conn.commit()


def insert_stock_data(stock):
    cursor.execute('''
    INSERT OR REPLACE INTO stock_data (ticker, name, assets, liabilities, equity, asset_list, liabilities_list, equity_list)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (stock.ticker, stock.name, stock.assets, stock.liabilities, stock.equity,
          stock.fetch_asset_list.to_json(), stock.fetch_liabilities_list.to_json(), stock.fetch_equity_list.to_json()))
    conn.commit()

def get_stock_data(ticker):
    cursor.execute('SELECT * FROM stock_data WHERE ticker = ?', (ticker,))
    row = cursor.fetchone()
    
    if not row:
        return None

    stock = Stock(row[1], row[0])  # Initializing with name and ticker
    stock.assets = row[2]
    stock.liabilities = row[3]
    stock.equity = row[4]
    
    return stock

df = pd.read_sql("SELECT * FROM stock_data",conn)
