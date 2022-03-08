"""
This module contains the abstract class AbstractController, containing the methods that are shared
between HomeController and IncidentController.
"""
from abc import ABC, abstractmethod
from configparser import ConfigParser
from importlib import import_module
from os import makedirs, path


class AbstractController(ABC):
    """
    This abstract class represents an abstract controller and implements ABC (Abstract Base Class).
    It contains the abstract and static methods to be shared between HomeController and
    IncidentController.
    """

    @abstractmethod
    def main(self):
        """This method starts the controllers view."""

    @staticmethod
    def load_controller(controller):
        """
        This method returns an instance of a controller object.

        :param controller: Name of the controller.
        :returns: Instance of a controller object.
        """
        module = import_module("iotumble.controllers." + controller.lower() + "_controller")
        controller = getattr(module, controller + "Controller")
        return controller

    @staticmethod
    def load_view(view):
        """
        This method returns an instance of a view object.

        :param view: Name of the view.
        :returns: Instance of a view object.
        """
        module = import_module("iotumble.views." + view.lower() + "_view")
        view = getattr(module, view + "View")
        return view

    @staticmethod
    def read_credentials(credentials_path: str) -> ConfigParser:
        """
        This method creates and returns a ConfigParser object of a read credentials.ini file of a
        passed path.

        :param credentials_path: Name of the credentials path.
        :returns: ConfigParser object of a read credentials.ini.
        """
        credentials = ConfigParser()
        credentials.read(credentials_path)
        return credentials

    @staticmethod
    def check_path(path_name: str) -> bool:
        """
        This method checks if a passed path exists.

        :param path_name: Name of the path.
        :returns: Boolean outcome on if path exists.
        """
        return bool(path.exists(path_name))

    @staticmethod
    def join_path(parent_path: str, child_path: str) -> str:
        """
        This method joins and returns a parent and child path together.

        :param parent_path: Name of the parent path.
        :param child_path: Name of the child path.
        :returns: Joined path of parent and child.
        """
        return path.join(parent_path, child_path)

    @staticmethod
    def create_path(path_name: str):
        """
        This method creates a credentials.ini or a passed path.

        :param path_name: Name of the path.
        """
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
