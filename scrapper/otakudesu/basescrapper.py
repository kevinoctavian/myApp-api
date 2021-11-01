import requests
from constant import OTAKUDESU_LINK

class BaseScrapper:
    BASELINK = OTAKUDESU_LINK

    def __init__(self):
        self._requestText = None

    def _setRequest(self, link=None):
        if link:
            self._requestText = requests.get(link).text
        else:
            self._requestText = requests.get(link).text

