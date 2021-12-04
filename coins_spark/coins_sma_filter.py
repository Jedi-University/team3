from pyspark import SparkContext
from pyspark.sql import SparkSession
from pyspark.sql import functions as func
from pyspark.sql.window import Window

SMA_LENGHT = 30


class CoinsSmaFilter:

    def __init__(self) -> None:
        self.sc = SparkContext('local[*]')
        self.spark = SparkSession.builder.getOrCreate()

    def load(self, path='coins.csv'):
        schema=('index long, time long, open double, '
                'high double, low double, close double')
        return self.spark.read.csv(path, header=False,schema=schema)

    def filter(self, df_input):        
        windowSpec = Window.partitionBy('partition').orderBy(
            'index').rowsBetween(-SMA_LENGHT, 0)

        df = df_input.withColumn("partition", func.lit("1")).withColumn(
            "sma", func.mean("close").over(windowSpec))
        # df = df.filter(df['close'] > df['sma']).drop('sma', 'partition')
        df = df.filter((df['close'] > df['sma']) & (df['index'] >= SMA_LENGHT)).drop('sma', 'partition')
        return df
    
    def store(self, df):
        df.show()
        df.write.parquet('coins.parquet')

    def run(self):
        df = self.load()
        df = self.filter(df)
        self.store(df)

if __name__ == '__main__':
    CoinsSmaFilter().run()
