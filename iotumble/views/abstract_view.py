from abc import ABC, abstractmethod


class AbstractView(ABC):
    @abstractmethod
    def start(self):
        pass

    @abstractmethod
    def close(self):
        pass
