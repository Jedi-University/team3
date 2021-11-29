from loguru import logger
from itertools import cycle

class MockLocation:
    
    def __init__(self, *args, **kwargs):
        self.locations = cycle(['Ru', 'Us', 'Gb', 'Ch'])

    def get(self, ip: str):
        return next(self.locations)