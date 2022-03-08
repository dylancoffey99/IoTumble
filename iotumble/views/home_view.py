"""This module contains the HomeView class, to represent a home view of the program."""
import tkinter as tk
from tkinter import ttk

from PIL import Image, ImageTk

from iotumble.views.abstract_view import AbstractView


class HomeView(AbstractView, tk.Tk):
    """
    This class represents a home view of the program, implementing AbstractView and tk.Tk. It
    contains a constructor, a method for loading the programs styling, the methods for loading its
    icon and widgets, the methods for interacting with its widgets and controller, and the
    implemented abstract methods.
    """

    def __init__(self, controller):
        """This constructor instantiates a HomeView object."""
        super().__init__()
        self.withdraw()
        self.controller = controller
        self.icon = tk.Toplevel()
        self.header_logo = ImageTk.PhotoImage(Image.open("logo.png"))
        self.incidents_tree_view = ttk.Treeview()
        self.inputs = {"access": tk.StringVar(), "secret": tk.StringVar(), "region": tk.StringVar()}

    def load_root(self):
        self.overrideredirect(True)
        self.set_geometry(self, 600, 600)
        self.configure(background=self.primary_bg)
        self.frame = tk.Frame(self, background=self.primary_bg, relief="solid", borderwidth=1)
        self.frame.pack(expand=True, fill="both")

    def load_icon(self):
        """This method loads the programs toolbar icon."""
        self.icon.attributes("-alpha", 0.0)
        self.icon.title("IoTumble")
        self.icon.iconbitmap("logo.ico")
        self.icon.configure(background=self.secondary_bg)
        self.icon.protocol("WM_DELETE_WINDOW", lambda: self.close(self))

    def load_style(self):
        """
        This method loads the programs widget styling, such as its colors, fonts, and
        configurations.
        """
        style = ttk.Style()
        style.theme_create("iotumble", parent="default", settings={
            "TButton": {
                "configure": {
                    "anchor": "center", "background": self.primary_bg, "borderwidth": 0,
                    "font": (self.font, 12, "bold"), "foreground": self.primary_fg
                }, "map": {
                    "background": [("pressed", self.highlight_bg)]
                }},
            "header.TButton": {
                "configure": {
                    "anchor": "center", "background": self.primary_bg, "borderwidth": 0,
                    "font": (self.font, 14, "bold"), "foreground": self.primary_fg
                }, "map": {
                    "background": [("active", self.highlight_bg)]
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
                    "font": (self.font, 12, "bold"), "foreground": self.primary_fg, "padding": 10
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
                    "background": self.tertiary_bg, "borderwidth": 0,
                    "troughcolor": self.highlight_bg
                }},
            "Treeview": {
                "configure": {
                    "background": self.primary_bg, "borderwidth": 0,
                    "fieldbackground": self.secondary_bg, "font": (self.font, 12),
                    "foreground": self.primary_fg, "rowheight": 46
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
        header_logo_label = ttk.Label(self.frame, style="primary.TLabel", image=self.header_logo)
        header_logo_label.pack(expand=True, fill="both", side="top", ipady=24)
        header_logo_label.bind("<ButtonPress-1>", lambda e: self.pressed_window(self, True, e))
        header_logo_label.bind("<ButtonRelease-1>", lambda e: self.pressed_window(self, False, e))
        header_logo_label.bind("<B1-Motion>", lambda e: self.move_window(self, e))

    def load_incidents(self):
        """
        This method loads the incidents section and its widgets, such as its frame, label, treeview,
        and scrollbar.
        """
        incidents_frame = tk.Frame(self.frame, background=self.secondary_bg)
        incidents_frame.pack(expand=True, fill="both", side="left")
        incidents_title_label = ttk.Label(incidents_frame, style="tertiary.TLabel",
                                          text="Incidents")
        incidents_title_label.pack(fill="both")
        self.incidents_tree_view = ttk.Treeview(incidents_frame, show="tree", selectmode="browse")
        self.incidents_tree_view.pack(expand=True, fill="both", side="left")
        incidents_scrollbar = ttk.Scrollbar(incidents_frame, orient="vertical",
                                            command=self.incidents_tree_view.yview)
        incidents_scrollbar.pack(fill="both", side="right")
        self.incidents_tree_view.configure(yscrollcommand=incidents_scrollbar.set)
        self.incidents_tree_view.tag_configure("highlight", background=self.highlight_bg,
                                               foreground=self.primary_fg)
        self.incidents_tree_view.tag_configure("0", background=self.secondary_bg)
        self.incidents_tree_view.tag_configure("1", background=self.primary_bg)
        self.incidents_tree_view.bind("<Motion>", lambda e: self.highlight_tree_view(True, e))
        self.incidents_tree_view.bind("<Leave>", lambda e: self.highlight_tree_view(False, e))
        self.incidents_tree_view.bind("<<TreeviewSelect>>", lambda e: self.switch())

    def load_session(self):
        """
        This method loads the session section and its widgets, such as its frame, labels, entries,
        combobox, and buttons.
        """
        session_frame = tk.Frame(self.frame, background=self.secondary_bg)
        session_frame.pack(expand=True, fill="both", side="top", ipadx=47)
        session_title_label = ttk.Label(session_frame, style="tertiary.TLabel", text="Session")
        session_title_label.pack(fill="both")
        session_access_label = ttk.Label(session_frame, style="secondary.TLabel",
                                         text="Access Key ID")
        session_access_label.pack(expand=True, pady=(18, 0))
        session_access_entry = ttk.Entry(session_frame, font=(self.font, 12), width=21,
                                         show="*", textvariable=self.inputs["access"])
        session_access_entry.pack()
        session_secret_label = ttk.Label(session_frame, style="secondary.TLabel",
                                         text="Secret Access Key")
        session_secret_label.pack(expand=True)
        session_secret_entry = ttk.Entry(session_frame, font=(self.font, 12), width=21,
                                         show="*", textvariable=self.inputs["secret"])
        session_secret_entry.pack()
        session_region_label = ttk.Label(session_frame, style="secondary.TLabel",
                                         text="Region Name")
        session_region_label.pack(expand=True)
        session_region_combobox = ttk.Combobox(session_frame, state="readonly",
                                               font=(self.font, 12),
                                               textvariable=self.inputs["region"],
                                               values=["us-east-1", "us-east-2",
                                                       "us-west-1", "us-west-2"])
        session_region_combobox.pack()
        session_connect_button = ttk.Button(session_frame, takefocus=False, text="Connect",
                                            command=lambda: self.connect(session_frame))
        session_connect_button.pack(expand=True, fill="both", side="left", padx=(0, 5),
                                    pady=(46, 0), ipady=30)
        session_quit_button = ttk.Button(session_frame, takefocus=False, text="Quit",
                                         command=lambda: self.close(self))
        session_quit_button.pack(expand=True, fill="both", side="left", pady=(46, 0),
                                 ipadx=17, ipady=30)

    def show_message(self, message_text: str):
        """
        This method shows a pop-up for displaying a message.

        :param message_text: Text of the message pop-up.
        """
        message = tk.Toplevel()
        message.overrideredirect(True)
        message.attributes("-topmost", True)
        message.configure(background=self.secondary_bg)
        message_frame = tk.Frame(message, background=self.secondary_bg, relief="solid",
                                 borderwidth=1)
        message_frame.pack(expand=True, fill="both")
        message_label = ttk.Label(message_frame, anchor="center", justify="center", wraplength=250,
                                  style="secondary.TLabel", text=message_text)
        message_label.pack(expand=True, fill="both")
        message_label.bind("<ButtonPress-1>", lambda e: self.pressed_window(message, True, e))
        message_label.bind("<ButtonRelease-1>", lambda e: self.pressed_window(message, False, e))
        message_label.bind("<B1-Motion>", lambda e: self.move_window(message, e))
        message_button = ttk.Button(message_frame, takefocus=False, text="Continue",
                                    command=message.destroy)
        message_button.pack(expand=True, fill="both")
        self.set_geometry(message, 300, 300)

    def connect(self, session_frame: tk.Frame):
        """
        This method passes the session inputs to connect() from HomeController, and if it returns
        True, it covers the session section with a disconnect button.

        :param session_frame: Frame of the session section.
        """
        if self.controller.connect(self.inputs["access"].get(), self.inputs["secret"].get(),
                                   self.inputs["region"].get()):
            disconnect_button = ttk.Button(session_frame, takefocus=False, text="Disconnect",
                                           command=lambda: self.disconnect(disconnect_button))
            disconnect_button.place(height=460, width=293, y=22)

    def disconnect(self, disconnect_button: ttk.Button):
        """
        This method calls disconnect() from HomeController, clears the incidents treeview, and
        destroys the disconnect button.

        :param disconnect_button: Disconnect button to be destroyed.
        """
        self.controller.disconnect()
        self.clear_tree_view()
        disconnect_button.destroy()

    def fill_inputs(self, access_key_id: str, secret_access_key: str, region_name: str):
        """
        This method fills the inputs of the session section with its passed parameters.

        :param access_key_id: Access Key ID of the Session.
        :param secret_access_key: Secret Access Key of the Session.
        :param region_name: Region Name of the Session.
        """
        self.inputs["access"].set(access_key_id)
        self.inputs["secret"].set(secret_access_key)
        self.inputs["region"].set(region_name)

    def fill_incidents(self, incident_count: int):
        """
        This method fills the incidents treeview with a certain amount of items.

        :param incident_count: Count of incident items.
        """
        for i in range(incident_count):
            i += 1
            self.incidents_tree_view.insert("", 0, tags=str(i % 2), text="Incident " + str(i))

    def highlight_tree_view(self, highlighted: bool, event):
        """
        This method highlights a row in the incidents treeview if its being hovered over.

        :param highlighted: Boolean on if a row is highlighted.
        :param event: Event calling this method.
        """
        row = self.incidents_tree_view.identify_row(event.y)
        self.tk.call(self.incidents_tree_view, "tag", "remove", "highlight")
        if highlighted:
            self.tk.call(self.incidents_tree_view, "tag", "add", "highlight", row)

    def clear_tree_view(self):
        """This method clears all items from the incidents treeview."""
        for item in self.incidents_tree_view.get_children():
            self.incidents_tree_view.delete(item)

    def switch(self):
        """
        This method gets the selected item and its incident ID from the incidents treeview, and
        passes it to switch() in HomeController.
        """
        selected = self.incidents_tree_view.selection()[0]
        if selected != "":
            selected_text = self.incidents_tree_view.item(selected, "text")
            incident_id = int(selected_text.replace("Incident ", ""))
            self.controller.switch(incident_id)

    def hide(self):
        """This method hides the view and unbinds its icon."""
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
        self.open(self)
        self.mainloop()
