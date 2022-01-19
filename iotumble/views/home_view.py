import tkinter as tk

from iotumble.views.abstract_view import AbstractView


class HomeView(AbstractView, tk.Tk):
    def __init__(self, controller):
        super().__init__()
        self.home_controller = controller
        self.frames = [tk.Frame(), tk.Frame(), tk.Frame(),
                       tk.Frame(), tk.Frame()]

    def load_root(self):
        self.title("IoTumble")
        self.geometry("1600x900")
        self.resizable(width=False, height=False)

    def load_frames(self):
        self.frames[0] = tk.Frame(self, bg=self.primary_bg)  # Header Frame
        self.frames[0].pack(expand=True, fill="both")
        self.frames[1] = tk.Frame(self, bg=self.secondary_bg)  # Incidents Frame
        self.frames[1].pack(ipady=400, expand=True, fill="both", side="left")
        self.frames[2] = tk.Frame(self, bg=self.tertiary_bg)  # Graphs Frame
        self.frames[2].pack(ipadx=650, expand=True, fill="both")
        self.frames[3] = tk.Frame(self, bg=self.primary_bg)  # Table Frame
        self.frames[3].pack(ipady=150, expand=True, fill="both", side="left")
        self.frames[4] = tk.Frame(self, bg=self.secondary_bg)  # Action Frame
        self.frames[4].pack(ipady=150, expand=True, fill="both", side="right")

    def start(self):
        self.load_root()
        self.load_frames()
        self.mainloop()

    def close(self):
        self.destroy()
