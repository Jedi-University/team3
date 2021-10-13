from load import CoinGecko
from slice import SplitData

DATA_PATH = 'data/'
PATH = DATA_PATH + 'input_data.csv'

if __name__ == '__main__':
    
    # load data
    CoinGecko(path=PATH).proc_data()

    # split data to small files
    split_data  = SplitData(input_path=PATH, data_path=DATA_PATH)
    split_data.split_file_with_df()
    
    # wite file with close > sma30
    split_data.sma_with_df()

