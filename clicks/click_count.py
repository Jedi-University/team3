from datetime import datetime

from loguru import logger
from mrjob.job import MRJob
from mrjob.step import MRStep


class ClickCount(MRJob):

    def mapper_count_ip(self, _, line):
        # split line str like '[2021-11-30 04:16:41.494514] 10.10.10.10'
        ip = line.split()[2]
        yield ip, 1

    def reducer_sum(self, key, counts):
        yield (key, sum(counts))

    def reducer_sum_filter(self, ip, counts):
        count = sum(counts)
        if count > 1:
            yield ip, count

    def steps(self):
        return [
            MRStep(mapper=self.mapper_count_ip,
                   reducer=self.reducer_sum_filter),
        ]


if __name__ == '__main__':
    logger.add('app.log', rotation='0.2 MB',
               retention=1, enqueue=True, diagnose=True)
    logger.info(f'{"-"*5} start {"-"*5}')
    start_time = datetime.now()

    ClickCount.run()

    time_delta = datetime.now() - start_time
    logger.info(f'Total minutes: {time_delta.total_seconds()/60:.2f}')
