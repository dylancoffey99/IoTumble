import tkinter as tk
from tkinter import ttk

from PIL import Image, ImageTk

from iotumble.views.abstract_view import AbstractView


class HomeView(AbstractView, tk.Tk):
    def __init__(self, controller):
        super().__init__()
        self.home_controller = controller
        self.frames = [tk.Frame(), tk.Frame(), tk.Frame(), tk.Frame(), tk.Frame()]
        self.header_logo = None

    def load_root(self):
        self.title("IoTumble")
        self.geometry("1600x900")
        self.iconbitmap("logo.ico")
        self.resizable(width=False, height=False)

    def load_frames(self):
        self.frames[0] = tk.Frame(self, bg=self.primary_bg, highlightbackground=self.tertiary_bg,
                                  highlightthickness=1)  # Header Frame
        self.frames[0].pack(expand=True, fill="both", side="top")
        self.frames[1] = tk.Frame(self, bg=self.secondary_bg, highlightbackground=self.tertiary_bg,
                                  highlightthickness=1)  # Incidents Frame
        self.frames[1].pack(expand=True, fill="both", side="left", ipady=400)
        self.frames[2] = tk.Frame(self, bg=self.primary_bg, highlightbackground=self.tertiary_bg,
                                  highlightthickness=1)  # Graphs Frame
        self.frames[2].pack(expand=True, fill="both", side="top", ipadx=650)
        self.frames[3] = tk.Frame(self, bg=self.secondary_bg, highlightbackground=self.tertiary_bg,
                                  highlightthickness=1)  # Table Frame
        self.frames[3].pack(expand=True, fill="both", side="left", ipady=150)
        self.frames[4] = tk.Frame(self, bg=self.secondary_bg, highlightbackground=self.tertiary_bg,
                                  highlightthickness=1)  # Action Frame
        self.frames[4].pack(expand=True, fill="both", side="right", ipady=150)

    def load_header(self):
        self.header_logo = ImageTk.PhotoImage(Image.open("logo.png"))
        header_logo_label = ttk.Label(self.frames[0], image=self.header_logo,
                                      background=self.primary_bg)
        header_logo_label.pack(padx=48, fill="both", side="left")

    def start(self):
        self.load_root()
        self.load_frames()
        self.load_header()
        self.mainloop()

    def close(self):
        self.destroy()
