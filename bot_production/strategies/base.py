from abc import ABC, abstractmethod

class Strategy(ABC):
    def __init__(self, data, params):
        self.data = data
        self.params = params

    @abstractmethod
    def analyze(self):
        pass