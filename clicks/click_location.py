from concurrent.futures import ThreadPoolExecutor
from datetime import datetime

from loguru import logger
from mrjob.job import MRJob
from mrjob.step import MRStep

from app_config import location


class ClickLocation(MRJob):

    DIRS = ['api']
    FILES = ['app_config.py']

    def mapper_ip(self, _, line):
        # split str like '[2021-11-30 04:16:41.494514] 10.10.10.10'
        ip = line.split()[2]
        yield ip, None

    def mapper_ip_part(self, ip, _):
        part = int(ip.split('.')[-1]) % 10
        yield part, (ip, 1)

    def reducer_group_only(self, key, _):
        yield key, None

    def reducer_sum(self, key, counts):
        yield (key, sum(counts))

    def mapper_location(self, ip, _):
        loc = location.get(ip)
        yield (loc, 1)

    def reducer_location_by_ip_part(self, part, ip_counts):
        # 3	[["78.186.28.73", 1], ["10.73.83.143", 1]]
        with ThreadPoolExecutor(max_workers=100) as executor:
            loc_counts = executor.map(lambda ip_c: (
                location.get(ip_c[0]), ip_c[1]), ip_counts)
        for loc, count in loc_counts:
            yield loc, count

    def steps(self):

        WITH_PARTS = True
        # WITH_PARTS = False

        if WITH_PARTS:
            return [
                MRStep(mapper=self.mapper_ip,
                       reducer=self.reducer_group_only),
                MRStep(mapper=self.mapper_ip_part,
                       reducer=self.reducer_location_by_ip_part),
                MRStep(reducer=self.reducer_sum),
            ]
        else:
            return [
                MRStep(mapper=self.mapper_ip,
                       reducer=self.reducer_group_only),
                MRStep(mapper=self.mapper_location,
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
