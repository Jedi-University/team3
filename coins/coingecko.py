import pandas as pd
import requests


class CoinGecko():

    def __init__(self, path: str = 'input_data.csv',
                 id: str = 'binancecoin',
                 vs_currency: str = 'usd',
                 days: int = 365):
        self.path = path
        self.id = id
        self.vs_currency = vs_currency
        self.days = days

    def load(self):
        """Load data from api"""
        url = f"https://api.coingecko.com/api/v3/coins/{self.id}/ohlc"
        headers = {'Content-Type': "application/json"}
        params = {"vs_currency": self.vs_currency, "days": self.days}
        response = requests.request("GET", url, headers=headers, params=params)
        json_response = response.json()
        df = pd.DataFrame.from_dict(json_response)
        self.df = df
        return df

    def write_file(self):
        """Write data to csv file"""
        self.df.to_csv(path_or_buf=self.path, header=False)

    def proc_data(self):
        """Load and write data"""
        self.load()
        self.write_file()


if __name__ == '__main__':
    CoinGecko(path='input_data.csv').proc_data()
