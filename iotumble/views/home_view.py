import tkinter as tk
from tkinter import ttk

from PIL import Image, ImageTk
from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from iotumble.views.abstract_view import AbstractView


class HomeView(AbstractView, tk.Tk):
    def __init__(self, controller):
        super().__init__()
        self.home_controller = controller
        self.frames = [tk.Frame(), tk.Frame(), tk.Frame(), tk.Frame(), tk.Frame(), tk.Frame()]
        self.header_logo = ImageTk.PhotoImage(Image.open("logo.png"))
        self.tree_views = [ttk.Treeview(), ttk.Treeview()]
        self.details_columns = ["Timestamp", "X-Acceleration", "Y-Acceleration", "Z-Acceleration",
                                "SVM"]

    def load_root(self):
        self.title("IoTumble")
        self.geometry("1600x900")
        self.iconbitmap("logo.ico")
        self.resizable(width=False, height=False)

    def load_style(self):
        style = ttk.Style()
        style.theme_create("iotumble", parent="default", settings={
            "actions.TButton": {
                "configure": {
                    "anchor": "center", "background": self.primary_bg, "borderwidth": 0,
                    "font": (self.font, 12, "bold"), "foreground": self.primary_fg
                }, "map": {
                    "background": [("active", self.primary_fg)],
                    "foreground": [("active", self.secondary_bg)]
                }},
            "header.TButton": {
                "configure": {
                    "anchor": "center", "background": self.primary_bg, "borderwidth": 0,
                    "font": (self.font, 14, "bold"), "foreground": self.primary_fg
                }, "map": {
                    "background": [("active", self.primary_fg)],
                    "foreground": [("active", self.secondary_bg)]
                }},
            "TCombobox": {
                "configure": {
                    "arrowcolor": self.primary_fg, "background": self.tertiary_bg,
                    "borderwidth": 0, "fieldbackground": self.primary_bg,
                    "foreground": self.primary_fg, "relief": "flat",
                    "selectbackground": self.primary_bg, "selectforeground": self.primary_fg
                }},
            "primary.TLabel": {
                "configure": {
                    "anchor": "center",
                    "background": self.primary_bg,
                    "foreground": self.primary_fg,
                    "font": (self.font, 12, "bold"),
                    "padding": 10
                }},
            "secondary.TLabel": {
                "configure": {
                    "background": self.secondary_bg,
                    "foreground": self.primary_fg,
                    "font": (self.font, 12, "bold")
                }},
            "TScrollbar": {
                "configure": {
                    "background": self.tertiary_bg, "borderwidth": 0,
                    "troughcolor": self.secondary_bg
                }, "map": {
                    "background": [("active", self.tertiary_bg)]
                }},
            "incidents.Treeview": {
                "configure": {
                    "background": self.primary_bg, "borderwidth": 0,
                    "fieldbackground": self.secondary_bg, "font": (self.font, 12),
                    "foreground": self.primary_fg, "rowheight": 44
                }, "map": {
                    "background": [("selected", self.primary_fg)],
                    "foreground": [("selected", self.secondary_bg)]
                }},
            "details.Treeview": {
                "configure": {
                    "background": self.primary_bg, "borderwidth": 0,
                    "fieldbackground": self.secondary_bg, "font": (self.font, 10),
                    "foreground": self.primary_fg, "rowheight": 24
                }},
            "details.Treeview.Heading": {
                "configure": {
                    "background": self.tertiary_bg, "font": (self.font, 10),
                    "foreground": self.primary_fg
                }}})
        style.theme_use("iotumble")
        style.layout("Treeview.Item", [("Treeitem.padding", {
            "children": [("Treeitem.indicator", {
                "side": "left", "sticky": ""
            }), ("Treeitem.text", {
                "side": "left", "sticky": ""
            })]})])
        style.layout("TScrollbar", [("TScrollbar.trough", {
            "children": [("TScrollbar.thumb", {
                "expand": "1", "sticky": "nsew"
            })]})])
        self.option_add("*TCombobox*Listbox*Background", self.secondary_bg)
        self.option_add("*TCombobox*Listbox*BorderWidth", 0)
        self.option_add("*TCombobox*Listbox*Foreground", self.primary_fg)
        self.option_add("*TCombobox*Listbox*Font", (self.font, 12, "bold"))
        self.tk.eval("ttk::style configure ComboboxPopdownFrame -relief solid")

    def load_frames(self):
        self.frames[0] = tk.Frame(self, background=self.primary_bg)
        self.frames[0].pack(expand=True, fill="both", side="top", ipady=20)
        self.frames[1] = tk.Frame(self, background=self.secondary_bg)
        self.frames[1].pack(expand=True, fill="both", side="left")
        self.frames[2] = tk.Frame(self, background=self.secondary_bg)
        self.frames[2].pack(expand=True, fill="both", side="top", ipadx=324)
        self.frames[3] = tk.Frame(self, background=self.primary_bg)
        self.frames[3].pack(expand=True, fill="both", side="left")
        self.frames[4] = tk.Frame(self, background=self.secondary_bg)
        self.frames[4].pack(expand=True, fill="both", side="top", ipadx=60)
        self.frames[5] = tk.Frame(self, background=self.secondary_bg)
        self.frames[5].pack(expand=True, fill="both", side="bottom")

    def load_header(self):
        header_logo_label = ttk.Label(self.frames[0], style="primary.TLabel",
                                      image=self.header_logo)
        header_logo_label.pack(fill="both", side="left", padx=44)
        header_refresh_button = ttk.Button(self.frames[0], takefocus=False, text="Refresh",
                                           style="header.TButton")
        header_refresh_button.pack(fill="both", side="left", ipadx=40)
        header_options_button = ttk.Button(self.frames[0], takefocus=False, text="Options",
                                           style="header.TButton")
        header_options_button.pack(fill="both", side="left", ipadx=40)
        header_exit_button = ttk.Button(self.frames[0], takefocus=False, text="Exit",
                                        style="header.TButton", command=self.close)
        header_exit_button.pack(fill="both", side="left", ipadx=40)

    def load_incidents(self):
        self.tree_views[0] = ttk.Treeview(self.frames[1], show="tree", selectmode="browse",
                                          style="incidents.Treeview")
        self.tree_views[0].pack(expand=True, fill="both", side="left")
        incidents_scrollbar = ttk.Scrollbar(self.frames[1], orient="vertical",
                                            command=self.tree_views[0].yview)
        incidents_scrollbar.pack(fill="both", side="right")
        self.tree_views[0].configure(yscrollcommand=incidents_scrollbar.set)
        self.tree_views[0].tag_configure("0", background=self.secondary_bg)
        self.tree_views[0].tag_configure("1", background=self.primary_bg)

    def load_details(self):
        details_label = ttk.Label(self.frames[3], style="primary.TLabel", text="Incident Details")
        details_label.pack()
        self.tree_views[1] = ttk.Treeview(self.frames[3], columns=self.details_columns,
                                          show="headings", selectmode="none",
                                          style="details.Treeview")
        self.tree_views[1].pack(expand=True, fill="both", side="left")
        details_scrollbar = ttk.Scrollbar(self.frames[3], orient="vertical",
                                          command=self.tree_views[1].yview)
        details_scrollbar.pack(fill="both", side="right")
        self.tree_views[1].configure(yscrollcommand=details_scrollbar.set)
        self.tree_views[1].tag_configure("0", background=self.secondary_bg)
        self.tree_views[1].tag_configure("1", background=self.primary_bg)
        for column in self.details_columns:
            self.tree_views[1].column(column, anchor="center", width=1)
            self.tree_views[1].heading(column, text=column)

    def load_graph(self):
        graph_figure = plt.figure(facecolor=self.secondary_bg)
        graph_canvas = FigureCanvasTkAgg(graph_figure, master=self.frames[2]).get_tk_widget()
        graph_canvas.pack(fill="both")

    def load_actions(self):
        actions_label = ttk.Label(self.frames[4], style="primary.TLabel", text="Incident Actions")
        actions_label.pack(fill="both", side="top")
        actions_graph_label = ttk.Label(self.frames[4], style="secondary.TLabel",
                                        text="Incident Graph")
        actions_graph_label.pack(expand=True, side="left")
        actions_graph_combobox = ttk.Combobox(self.frames[4], state="readonly", width=30,
                                              font=(self.font, 12, "bold"),
                                              values=["All Acceleration", "X-Acceleration",
                                                      "Y-Acceleration", "Z-Acceleration",
                                                      "Signal Vector Magnitude (SVM)"])
        actions_graph_combobox.pack(expand=True, side="left")
        actions_export_graph_button = ttk.Button(self.frames[5], takefocus=False,
                                                 style="actions.TButton", text="Export Graph")
        actions_export_graph_button.pack(expand=True, fill="both", side="left")
        actions_export_details_button = ttk.Button(self.frames[5], takefocus=False,
                                                   style="actions.TButton", text="Export Details")
        actions_export_details_button.pack(expand=True, fill="both", side="left", padx=5)
        actions_delete_button = ttk.Button(self.frames[5], takefocus=False,
                                           style="actions.TButton", text="Delete Incident")
        actions_delete_button.pack(expand=True, fill="both", side="left")

    def start(self):
        self.load_root()
        self.load_style()
        self.load_frames()
        self.load_header()
        self.load_incidents()
        self.load_details()
        self.load_graph()
        self.load_actions()
        self.mainloop()

    def close(self):
        self.destroy()
