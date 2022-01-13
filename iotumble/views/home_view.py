import tkinter as tk

from iotumble.views.abstract_view import AbstractView


class HomeView(AbstractView, tk.Tk):
    def __init__(self, controller):
        super().__init__()
        self.home_controller = controller

    def start(self):
        self.mainloop()

    def close(self):
        self.destroy()
