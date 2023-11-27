from abc import ABCMeta, abstractmethod


class BaseWeather(metaclass=ABCMeta):
    def __init__(self, API_KEY, LAT, LON):
        self.API_KEY = API_KEY
        self.LAT = LAT
        self.LON = LON

    @abstractmethod
    def getWeather(self):
        pass
