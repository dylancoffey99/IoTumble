from abc import ABC, abstractmethod


class AbstractView(ABC):
    primary_bg = "#333333"
    primary_fg = "#976FFF"
    secondary_bg = "#2B2B2B"
    tertiary_bg = "#3F3F3F"

    @abstractmethod
    def start(self):
        pass

    @abstractmethod
    def close(self):
        pass
