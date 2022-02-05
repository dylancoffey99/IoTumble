import tkinter as tk
from tkinter import ttk

from PIL import Image, ImageTk

from iotumble.views.abstract_view import AbstractView


class HomeView(AbstractView, tk.Tk):
    def __init__(self, controller):
        super().__init__()
        self.withdraw()
        self.controller = controller
        self.icon = tk.Toplevel()
        self.border = tk.Frame()
        self.incidents_tree_view = ttk.Treeview()
        self.header_logo = ImageTk.PhotoImage(Image.open("logo.png"))

    def load_root(self):
        self.overrideredirect(True)
        self.set_geometry(self, 600, 600)
        self.configure(background=self.primary_bg)
        self.border = tk.Frame(self, background=self.primary_bg, relief="solid", borderwidth=1)
        self.border.pack(expand=True, fill="both")

    def load_icon(self):
        self.icon.attributes("-alpha", 0.0)
        self.icon.title("IoTumble")
        self.icon.iconbitmap("logo.ico")
        self.icon.configure(background=self.secondary_bg)
        self.icon.protocol("WM_DELETE_WINDOW", self.close)

    def load_style(self):
        style = ttk.Style()
        style.theme_create("iotumble", parent="default", settings={
            "TButton": {
                "configure": {
                    "anchor": "center", "background": self.primary_bg, "borderwidth": 0,
                    "font": (self.font, 12, "bold"), "foreground": self.primary_fg
                }, "map": {
                    "background": [("pressed", self.primary_fg)],
                    "foreground": [("pressed", self.secondary_bg)]
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
                    "foreground": self.primary_fg, "padding": 2, "relief": "flat",
                    "selectbackground": self.primary_bg, "selectforeground": self.primary_fg,
                }},
            "TEntry": {
                "configure": {
                    "borderwidth": 0, "fieldbackground": self.primary_bg,
                    "foreground": self.primary_fg, "insertcolor": self.primary_fg,
                    "padding": 2, "relief": "flat", "selectbackground": self.primary_fg,
                    "selectforeground": self.secondary_bg
                }},
            "primary.TLabel": {
                "configure": {
                    "anchor": "center", "background": self.primary_bg,
                    "font": (self.font, 12, "bold"), "foreground": self.primary_fg,
                    "padding": 10
                }},
            "secondary.TLabel": {
                "configure": {
                    "background": self.secondary_bg, "font": (self.font, 12, "bold"),
                    "foreground": self.primary_fg, "padding": 20
                }},
            "tertiary.TLabel": {
                "configure": {
                    "anchor": "center", "background": self.tertiary_bg,
                    "font": (self.font, 11, "bold"), "foreground": self.primary_fg
                }},
            "TScrollbar": {
                "configure": {
                    "background": self.primary_fg, "borderwidth": 0,
                    "troughcolor": self.tertiary_bg
                }, "map": {
                    "background": [("disabled", self.tertiary_bg)],
                }},
            "incidents.Treeview": {
                "configure": {
                    "background": self.primary_bg, "borderwidth": 0,
                    "fieldbackground": self.secondary_bg, "font": (self.font, 12),
                    "foreground": self.primary_fg, "rowheight": 46
                }, "map": {
                    "background": [("selected", "black")],
                    "foreground": [("selected", self.primary_fg)]
                }},
            "details.Treeview": {
                "configure": {
                    "background": self.primary_bg, "borderwidth": 0,
                    "fieldbackground": self.secondary_bg, "font": (self.font, 10),
                    "foreground": self.primary_fg, "rowheight": 26
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
        self.option_add("*TCombobox*Listbox*Font", (self.font, 12))
        self.option_add("*TCombobox*Listbox*Foreground", self.primary_fg)
        self.tk.eval("ttk::style configure ComboboxPopdownFrame -relief solid")

    def load_header(self):
        header_logo_label = ttk.Label(self.border, style="primary.TLabel", image=self.header_logo)
        header_logo_label.pack(expand=True, fill="both", side="top", ipady=24)
        header_logo_label.bind("<ButtonPress-1>", lambda e: self.pressed_window(self, True, e))
        header_logo_label.bind("<ButtonRelease-1>", lambda e: self.pressed_window(self, False, e))
        header_logo_label.bind("<B1-Motion>", lambda e: self.move_window(self, e))

    def load_incidents(self):
        incidents_frame = tk.Frame(self.border, background=self.secondary_bg)
        incidents_frame.pack(expand=True, fill="both", side="left")
        incidents_label = ttk.Label(incidents_frame, style="tertiary.TLabel", text="Incidents")
        incidents_label.pack(fill="both")
        self.incidents_tree_view = ttk.Treeview(incidents_frame, show="tree", selectmode="browse",
                                                style="incidents.Treeview")
        self.incidents_tree_view.pack(expand=True, fill="both", side="left")
        incidents_scrollbar = ttk.Scrollbar(incidents_frame, orient="vertical",
                                            command=self.incidents_tree_view.yview)
        incidents_scrollbar.pack(fill="both", side="right")
        self.incidents_tree_view.configure(yscrollcommand=incidents_scrollbar.set)
        self.incidents_tree_view.tag_configure("0", background=self.secondary_bg)
        self.incidents_tree_view.tag_configure("1", background=self.primary_bg)

    def load_session(self):
        session_frame = tk.Frame(self.border, background=self.secondary_bg)
        session_frame.pack(expand=True, fill="both", side="top", ipadx=47)
        session_label = ttk.Label(session_frame, style="tertiary.TLabel", text="Session")
        session_label.pack(fill="both")
        session_access_label = ttk.Label(session_frame, style="secondary.TLabel",
                                         text="Access Key ID")
        session_access_label.pack(expand=True, pady=(18, 0))
        session_access_entry = ttk.Entry(session_frame, font=(self.font, 12))
        session_access_entry.pack()
        session_secret_label = ttk.Label(session_frame, style="secondary.TLabel",
                                         text="Secret Access Key")
        session_secret_label.pack(expand=True)
        session_secret_entry = ttk.Entry(session_frame, font=(self.font, 12))
        session_secret_entry.pack()
        session_region_label = ttk.Label(session_frame, style="secondary.TLabel",
                                         text="Region Name")
        session_region_label.pack(expand=True)
        session_region_combobox = ttk.Combobox(session_frame, state="readonly",
                                               font=(self.font, 12),
                                               values=["us-east-1", "us-east-2",
                                                       "us-west-1", "us-west-2"])
        session_region_combobox.pack()

    def load_buttons(self):
        buttons_frame = tk.Frame(self.border, background=self.secondary_bg)
        buttons_frame.pack(expand=True, fill="both", side="bottom")
        connect_button = ttk.Button(buttons_frame, takefocus=False, style="login.TButton",
                                    text="Connect", command=self.controller.view)
        connect_button.pack(expand=True, fill="both", side="left", padx=(0, 5), pady=(46, 0))
        quit_button = ttk.Button(buttons_frame, takefocus=False, text="Quit", command=self.close)
        quit_button.pack(expand=True, fill="both", side="left", pady=(46, 0), ipadx=18)

    def hide(self):
        self.icon.unbind("<Map>")
        self.icon.unbind("<Unmap>")
        self.withdraw()

    def start(self):
        self.load_root()
        self.load_icon()
        self.load_style()
        self.load_header()
        self.load_incidents()
        self.load_session()
        self.load_buttons()
        self.open(self)
        self.mainloop()

    def close(self):
        self.destroy()
