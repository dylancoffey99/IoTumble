from abc import ABC, abstractmethod
from configparser import ConfigParser
from importlib import import_module
from os import makedirs, path


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

    @staticmethod
    def read_config():
        config = ConfigParser()
        config.read("config.ini")
        return config

    @staticmethod
    def check_path(path_name):
        return bool(path.exists(path_name))

    @staticmethod
    def join_path(parent, child):
        return path.join(parent, child)

    @staticmethod
    def create_path(path_name):
        if path_name == "config":
            config = ConfigParser()
            config.add_section(path_name)
            config.set(path_name, "access_key_id", "")
            config.set(path_name, "secret_access_key", "")
            config.set(path_name, "region_name", "")
            with open(f"{path_name}.ini", "w", encoding="utf-8") as file:
                config.write(file)
        else:
            makedirs(path_name)
