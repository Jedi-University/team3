from statistics import mean

import pandas as pd


class SplitData():

    def __init__(self, input_path: str = 'input_data.csv',
                 n_split_rows: int = 30,
                 sma_lenght: int = 30):

        self.input_path = input_path
        self.n_split_rows = n_split_rows
        self.sma_lenght = sma_lenght

    def write_csv(self, path, lines):
        """Write data in new file"""
        with open(path, "w") as file_w:
            file_w.writelines(lines)

    def split_file(self):
        """Split data on small files"""

        with open(self.input_path, "r") as file:
            line_index = 0
            output_file_index = 1
            lines = []
            sma_lines = []
            sma_window = []

            while True:
                line = file.readline()

                if line == '':
                    # end of file
                    if len(lines):
                        self.write_csv(f"slice{output_file_index:04}.csv",
                                       lines)
                    if len(sma_lines):
                        self.write_csv(f"sma{self.sma_lenght}.csv",
                                       sma_lines)
                    break

                # slice files
                if line_index < self.n_split_rows:
                    lines.append(line)
                    line_index += 1
                else:
                    self.write_csv(f"slice{output_file_index:04}.csv",
                                   lines)
                    lines = [line]
                    line_index = 1
                    output_file_index += 1

                # sma on 'close' column
                close = float(line.strip().split(',')[-1])
                sma_window.append(close)
                if len(sma_window) == 30:
                    if close > mean(sma_window):
                        sma_lines.append(line)
                    sma_window.pop(0)

    def split_file_with_df(self):
        """Split data on small files using df"""

        df = pd.read_csv(self.input_path,
                         names=['time', 'open', 'high', 'low', 'close'])

        # split data
        n_parts = len(df) // self.n_split_rows
        if len(df) % self.n_split_rows > 0:
            n_parts += 1
        for i in range(n_parts):
            df_slice = df.iloc[i*self.n_split_rows:(i+1)*self.n_split_rows]
            df_slice.to_csv(path_or_buf=f"slice{i+1:04}.csv",
                            header=False)

    def sma_with_df(self):
        """Split data on small files using df"""

        df = pd.read_csv(self.input_path,
                         names=['time', 'open', 'high', 'low', 'close'])

        # write sma file
        sma = df['close'].rolling(self.sma_lenght).mean()
        df_sma = df[sma < df['close']]
        df_sma.to_csv(path_or_buf=f"sma{self.sma_lenght}.csv", header=False)


if __name__ == '__main__':
    # SplitData(input_path='input_data.csv').split_file()
    # SplitData(input_path='input_data.csv').split_file_with_df()
    SplitData(input_path='input_data.csv').sma_with_df()
