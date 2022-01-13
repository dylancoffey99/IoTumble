from iotumble.controllers.abstract_controller import AbstractController


class HomeController(AbstractController):
    def __init__(self):
        self.home_view = self.load_view("Home")

    def main(self):
        self.home_view(self).start()
