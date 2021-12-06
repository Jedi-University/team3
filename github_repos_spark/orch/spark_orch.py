from loguru import logger
from pyspark.sql import SparkSession


class SparkOrch():

    def __init__(self, spark: SparkSession, workers: list, tops_n: int,
                 *args, **kwargs) -> None:
        self.spark = spark
        self.workers = workers
        self.tops_n = tops_n

    def run(self) -> list:
        worker_orgs = self.workers['orgs'].run
        worker_repos = self.workers['repos'].run
        # worker_top = self.workers['top'].run

        # get repo urls for organizations
        orgs_repos_url = [[url] for url in worker_orgs()]
        df_urls = self.spark.createDataFrame(
            orgs_repos_url, schema='url string')
        df_urls.show()

        # get repos information
        rdd_repos = df_urls.rdd.flatMap(lambda x: worker_repos(x['url']))
        df_repos = rdd_repos.toDF()

        # get top repos
        top_df = df_repos.sort('stars_count', ascending=False)
        top_df.show()
        top = top_df.head(self.tops_n)
        top = list(map(lambda x: x.asDict(), top))
        # logger.debug(top)

        return top
