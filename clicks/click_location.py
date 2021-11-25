from loguru import logger
from mrjob.job import MRJob
from mrjob.step import MRStep

from app_config import location
# from api.location import location


class ClickLocation(MRJob):
    
    DIRS = ['api']
    FILES = ['app_config.py']

    def mapper_count_ip(self, _, line):
        ip = line.split()[2]
        yield (ip, 1)

    def combiner_count_ip(self, ip, counts):
        yield (ip, sum(counts))

    def reducer_count_ip(self, ip, counts):
        yield (ip, sum(counts))

    def mapper_location(self, ip, _):
        loc = location.get(ip)
        yield (loc, 1)

    def combiner_location(self, loc, counts):
        yield (loc, sum(counts))

    def reducer_location(self, loc, counts):
        yield (loc, sum(counts))

    def steps(self):
        
        return [
            MRStep(mapper=self.mapper_count_ip,
                   combiner=self.combiner_count_ip,
                   reducer=self.reducer_count_ip),
            MRStep(mapper=self.mapper_location,
                   combiner=self.combiner_location,
                   reducer=self.reducer_location),
        ]


if __name__ == '__main__':
    logger.add('app.log', rotation='0.2 MB',
               retention=1, enqueue=True, diagnose=True)
    logger.info(f'{"-"*5} start {"-"*5}')
    ClickLocation.run()
