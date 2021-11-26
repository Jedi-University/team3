from datetime import datetime

from loguru import logger
from mrjob.job import MRJob
from mrjob.step import MRStep

from app_config import location


class ClickLocation(MRJob):

    DIRS = ['api']
    FILES = ['app_config.py']

    def mapper_count_ip(self, _, line):
        ip = line.split()[2]
        yield (ip, 1)

    def reducer_sum(self, key, counts):
        yield (key, sum(counts))

    def mapper_location(self, ip, _):
        loc = location.get(ip)
        yield (loc, 1)

    def steps(self):

        return [
            MRStep(mapper=self.mapper_count_ip,
                   combiner=self.reducer_sum,
                   reducer=self.reducer_sum),
            MRStep(mapper=self.mapper_location,
                   combiner=self.reducer_sum,
                   reducer=self.reducer_sum),
        ]


if __name__ == '__main__':
    logger.add('app.log', rotation='0.2 MB',
               retention=1, enqueue=True, diagnose=True)
    logger.info(f'{"-"*5} start {"-"*5}')
    start_time = datetime.now()

    ClickLocation.run()

    time_delta = datetime.now() - start_time
    logger.info(f'Total minutes: {time_delta.total_seconds()/60:.2f}')
