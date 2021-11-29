import requests
from loguru import logger
from retry import retry


class Location:

    def __init__(self, url: str, *args, **kwargs):
        self.url = url
        self.session = self.get_session()

    def get_session(self):
        session = requests.Session()
        return session

    # @retry(tries=-1, delay=0, max_delay=None, backoff=1, jitter=0, logger=logger)
    @retry(tries=2, delay=0, max_delay=None, backoff=1, jitter=0, logger=logger)
    def get_api_response(self, ip: str) -> str:
        response = self.session.get(self.url, params={'ip': ip})
        # logger.debug(response.text)
        result = response.text
        return result

    @logger.catch
    def get(self, ip: str):
        location = self.get_api_response(ip)
        return location
