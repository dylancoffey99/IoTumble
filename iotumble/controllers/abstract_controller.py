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
    def read_credentials(credentials_path):
        credentials = ConfigParser()
        credentials.read(credentials_path)
        return credentials

    @staticmethod
    def check_path(path_name):
        return bool(path.exists(path_name))

    @staticmethod
    def join_path(parent, child):
        return path.join(parent, child)

    @staticmethod
    def create_path(path_name):
        if path_name == ".aws\\credentials.ini":
            credentials = ConfigParser()
            credentials.add_section("access")
            credentials.set("access", "access_key_id", "")
            credentials.set("access", "secret_access_key", "")
            credentials.set("access", "region_name", "")
            with open(path_name, "w", encoding="utf-8") as file:
                credentials.write(file)
        else:
            makedirs(path_name)
