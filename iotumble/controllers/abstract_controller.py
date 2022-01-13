from abc import ABC, abstractmethod
from importlib import import_module


class AbstractController(ABC):
    @abstractmethod
    def main(self):
        pass

    @staticmethod
    def load_controller(controller):
        module = import_module("iotumble.controllers." + controller.lower() + "_controller")
        controller = getattr(module, controller + "Controller")
        return controller

    @staticmethod
    def load_view(view):
        module = import_module("iotumble.views." + view.lower() + "_view")
        view = getattr(module, view + "View")
        return view
