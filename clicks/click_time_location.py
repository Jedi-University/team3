from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, time

from loguru import logger
from mrjob.job import MRJob
from mrjob.protocol import JSONValueProtocol
from mrjob.step import MRStep

from app_config import location


class ClickTimeLocation(MRJob):

    DIRS = ['api']
    FILES = ['app_config.py']
    OUTPUT_PROTOCOL = JSONValueProtocol

    def mapper_time(self, _, line):
        # split str like '[2021-11-30 04:16:41.494514] 10.10.10.10'
        ip = line.split()[2]
        time_str = line.split()[1][:-1]
        hour = time.fromisoformat(time_str).hour
        if 8 <= hour < 19:
            yield (hour, ip), 1

    def reducer_sum(self, key, counts):
        yield key, sum(counts)

    def mapper_ip_part(self, hour_ip, count):
        hour, ip = hour_ip
        part = int(ip.split('.')[-1]) % 10
        yield part, (ip, hour, count)

    def reducer_location_by_ip_part(self, part, ip_hour_counts):
        # input:    3	["78.186.28.73", 4, 1]
        with ThreadPoolExecutor(max_workers=100) as executor:
            loc_counts = executor.map(lambda ip_c: (
                location.get(ip_c[0]), ip_c[1], ip_c[2]), ip_hour_counts)
        for loc, hour, count in loc_counts:
            yield (hour, loc), count

    def mapper_ip_location(self, hour_ip, counts):
        hour, ip = hour_ip
        loc = location.get(ip)
        yield (hour, loc), counts

    def mapper_hours(self, hour_loc, counts):
        hour, loc = hour_loc
        yield (hour, {loc: counts})

    def reducer_hours(self, hour, loc_data):
        yield hour, list(loc_data)

    def mapper_hours_data(self, hour, loc_data):
        hour_str = time(hour).isoformat(timespec='minutes')
        yield None, (hour_str, loc_data)

    def reducer_hours_data(self, _, hours_data):
        yield None, dict(hours_data)

    def steps(self):

        WITH_PARTS = True
        # WITH_PARTS = False

        if WITH_PARTS:
            return [
                MRStep(mapper=self.mapper_time,
                       reducer=self.reducer_sum),
                MRStep(mapper=self.mapper_ip_part,
                       reducer=self.reducer_location_by_ip_part),
                MRStep(reducer=self.reducer_sum),
                MRStep(mapper=self.mapper_hours,
                       reducer=self.reducer_hours),
                MRStep(mapper=self.mapper_hours_data,
                       reducer=self.reducer_hours_data),
            ]
        else:
            return [
                MRStep(mapper=self.mapper_time,
                       reducer=self.reducer_sum),
                MRStep(mapper=self.mapper_ip_location,
                       reducer=self.reducer_sum),
                MRStep(mapper=self.mapper_hours,
                       reducer=self.reducer_hours),
                MRStep(mapper=self.mapper_hours_data,
                       reducer=self.reducer_hours_data),
            ]


if __name__ == '__main__':
    logger.add('app.log', rotation='0.2 MB',
               retention=1, enqueue=True, diagnose=True)
    logger.info(f'{"-"*5} start {"-"*5}')
    start_time = datetime.now()

    ClickTimeLocation.run()

    time_delta = datetime.now() - start_time
    logger.info(f'Total minutes: {time_delta.total_seconds()/60:.2f}')
