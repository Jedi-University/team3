from loguru import logger
from mrjob.job import MRJob
from mrjob.step import MRStep


class ClickCount(MRJob):

    def mapper_count_ip(self, _, line):
        ip = line.split()[2]
        yield (ip, 1)

    def combiner_count_ip(self, ip, counts):
        yield (ip, sum(counts))

    def reducer_count_ip(self, ip, counts):
        count = sum(counts)
        if count > 1:
            yield (ip, count)

    def steps(self):
        return [
            MRStep(mapper=self.mapper_count_ip,
                   combiner=self.combiner_count_ip,
                   reducer=self.reducer_count_ip),
        ]


if __name__ == '__main__':
    logger.add('app.log', rotation='0.2 MB',
           retention=1, enqueue=True, diagnose=True)
    logger.info(f'{"-"*5} start {"-"*5}')
    ClickCount.run()
