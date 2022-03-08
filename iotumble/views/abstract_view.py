"""
This module contains the abstract class AbstractView, containing the methods and variables that are
shared between HomeView and IncidentView.
"""
from abc import ABC, abstractmethod
from tkinter import EventType


class AbstractView(ABC):
    """
    This abstract class represents an abstract view and implements ABC (Abstract Base Class). It
    contains the methods, font name, and color hex codes to be shared between HomeView and
    IncidentView.
    """
    primary_bg = "#333333"
    secondary_bg = "#2B2B2B"
    tertiary_bg = "#3F3F3F"
    highlight_bg = "#232323"
    primary_fg = "#976FFF"
    secondary_fg = "#4F3A86"
    tertiary_fg = "#C8B3FF"
    font = "Helvetica"

    @abstractmethod
    def load_root(self):
        """This method loads the views root and sets its geometry, background color, and border."""

    @abstractmethod
    def load_header(self):
        """
        This method loads the views header and its widgets, such as its frame, logo, and
        buttons.
        """

    @abstractmethod
    def start(self):
        """
        This method runs the views various load methods, and the puts the views root in a
        loop.
        """

    @staticmethod
    def close(root):
        """
        This method closes the view by quitting and destroying its root.

        :param root: Root of the view.
        """
        root.quit()
        root.destroy()

    @staticmethod
    def open(root):
        """
        This method un-hides the view, and binds the minimizing of the programs icon to minimize the
        views root also.

        :param root: Root of the view.
        """
        root.icon.bind("<Map>", lambda e: root.minimize_window(root, e))
        root.icon.bind("<Unmap>", lambda e: root.minimize_window(root, e))
        root.deiconify()

    @staticmethod
    def set_geometry(root, width, height):
        """
        This method sets the geometry of the views root. It also centers it by calculating the X and
        Y coordinates for the center of the screen, and adding them to the views root geometry.

        :param root: Root of the view.
        :param width: Width geometry to be set to the root.
        :param height: Height geometry to be set to the root.
        """
        x_coord = int((root.winfo_screenwidth() / 2) - (width / 2))
        y_coord = int((root.winfo_screenheight() / 2) - (height / 2))
        root.geometry(f"{width}x{height}+{x_coord}+{y_coord}")

    @staticmethod
    def pressed_window(root, pressed, event):
        """
        This method checks if the header of the views root is being pressed, and sets the X and Y
        coordinates of the views root to the events X and Y coordinates.

        :param root: Root of the view.
        :param pressed: Boolean on if the header is being pressed.
        :param event: Event calling this method.
        """
        if pressed:
            root.x = event.x
            root.y = event.y
        else:
            root.x = None
            root.y = None

    @staticmethod
    def move_window(root, event):
        """
        This method moves the coordinates of the views root by adding an offset to its X and Y
        coordinates depending on the events X and Y coordinates. This is then added to the views
        root geometry.

        :param root: Root of the view.
        :param event: Event calling this method.
        """
        offset_x = event.x - root.x
        offset_y = event.y - root.y
        x_coord = root.winfo_x() + offset_x
        y_coord = root.winfo_y() + offset_y
        root.geometry(f"+{x_coord}+{y_coord}")

    @staticmethod
    def minimize_window(root, event):
        """
        This method minimizes and un-minimizes the views root depending on the event.

        :param root: Root of the view.
        :param event: Event calling this method.
        """
        if event.type == EventType.Map:
            root.deiconify()
        else:
            root.withdraw()
