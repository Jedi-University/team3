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
        # split line str like '[2021-11-30 04:16:41.494514] 10.10.10.10'
        ip = line.split()[2]
        time_str = line.split()[1][:-1]
        click_time_hour = time.fromisoformat(time_str).hour
        # if 8 <= click_time_hour < 19:
            # yield (click_time_hour, ip), 1
        yield (click_time_hour, ip), 1

    def reducer_sum(self, key, counts):
        yield key, sum(counts)

    def mapper_ip_location(self, hour_ip, counts):
        hour, ip = hour_ip
        loc = 'Ru'
        # loc = location.get(ip)
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

        return [
            MRStep(mapper=self.mapper_time,
                   combiner=self.reducer_sum,
                   reducer=self.reducer_sum),
            MRStep(mapper=self.mapper_ip_location,
                   combiner=self.reducer_sum,
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
