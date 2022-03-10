"""This module contains the IncidentView class, to represent an incident view of the program."""
import tkinter as tk
from tkinter import ttk
from typing import List, Tuple

from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from iotumble.views.abstract_view import AbstractView


class IncidentView(AbstractView, tk.Toplevel):
    """
    This class represents an incident view of the program, implementing AbstractView and
    tk.Toplevel. It contains a constructor, the methods for loading its icon and widgets, the
    methods for interacting with its widgets and controller, and the implemented abstract methods.
    """

    def __init__(self, controller):
        """This constructor instantiates an IncidentView object."""
        super().__init__()
        self.withdraw()
        self.controller = controller
        self.icon = controller.home_view.icon
        self.details_widgets = [ttk.Label(), ttk.Label(), ttk.Label(), ttk.Label(),
                                ttk.Label(), ttk.Label(), ttk.Treeview()]
        self.graph_widgets = [plt.figure(), plt.axes()]
        self.texts = ["All Acceleration", "Signal Vector Magnitude"]
        self.columns = ["Timestamp", "X-Acceleration", "Y-Acceleration", "Z-Acceleration", "SVM"]

    def load_root(self):
        self.overrideredirect(True)
        self.set_geometry(self, 1200, 800)
        self.configure(background=self.secondary_bg)
        self.frame = tk.Frame(self, background=self.secondary_bg, relief="solid", borderwidth=1)
        self.frame.pack(expand=True, fill="both")

    def load_header(self):
        header_frame = tk.Frame(self.frame, background=self.primary_bg)
        header_frame.pack(expand=True, fill="both", side="top")
        header_logo_label = ttk.Label(header_frame, style="primary.TLabel",
                                      image=self.controller.home_view.header_logo)
        header_logo_label.pack(fill="both", side="left", padx=44)
        header_back_button = ttk.Button(header_frame, takefocus=False, style="header.TButton",
                                        text="Back", command=self.controller.back)
        header_back_button.pack(fill="both", side="left", ipadx=55)
        for widget in [header_frame, header_logo_label]:
            widget.bind("<ButtonPress-1>", lambda e: self.pressed_window(self, True, e))
            widget.bind("<ButtonRelease-1>", lambda e: self.pressed_window(self, False, e))
            widget.bind("<B1-Motion>", lambda e: self.move_window(self, e))

    def load_details(self):
        """
        This method loads the details section and its widgets, such as its frames, labels, treeview,
        and scrollbar. It then calls fill_details() from IncidentController.
        """
        details_frame = tk.Frame(self.frame, background=self.secondary_bg)
        details_frame.pack(expand=True, fill="both", side="left")
        details_border_frame = tk.Frame(details_frame, background=self.tertiary_bg, width=15)
        details_border_frame.pack(fill="both", side="right")
        details_title_label = ttk.Label(details_frame, style="tertiary.TLabel",
                                        text="Incident Details")
        details_title_label.pack(fill="both", side="top")
        self.details_widgets[0] = ttk.Label(details_frame, style="secondary.TLabel",
                                            text="Date")
        self.details_widgets[0].pack(expand=True, fill="both")
        self.details_widgets[1] = ttk.Label(details_frame, style="secondary.TLabel",
                                            text=self.columns[0])
        self.details_widgets[1].pack(expand=True, fill="both")
        self.details_widgets[2] = ttk.Label(details_frame, style="secondary.TLabel",
                                            text=self.columns[1])
        self.details_widgets[2].pack(expand=True, fill="both")
        self.details_widgets[3] = ttk.Label(details_frame, style="secondary.TLabel",
                                            text=self.columns[2])
        self.details_widgets[3].pack(expand=True, fill="both")
        self.details_widgets[4] = ttk.Label(details_frame, style="secondary.TLabel",
                                            text=self.columns[3])
        self.details_widgets[4].pack(expand=True, fill="both")
        self.details_widgets[5] = ttk.Label(details_frame, style="secondary.TLabel",
                                            text=self.texts[1])
        self.details_widgets[5].pack(expand=True, fill="both")
        self.details_widgets[6] = ttk.Treeview(details_frame, columns=self.columns,
                                               show="headings", selectmode="none",
                                               style="details.Treeview")
        self.details_widgets[6].pack(expand=True, fill="both", side="left")
        details_scrollbar = ttk.Scrollbar(details_border_frame, orient="vertical",
                                          command=self.details_widgets[6].yview)
        details_scrollbar.place(height=280, width=15, y=420)
        self.details_widgets[6].configure(yscrollcommand=details_scrollbar.set)
        self.details_widgets[6].tag_configure("0", background=self.secondary_bg)
        self.details_widgets[6].tag_configure("1", background=self.primary_bg)
        self.details_widgets[6].bind("<Button-1>", self.stop_tree_view_resize)
        for column in self.columns:
            self.details_widgets[6].column(column, anchor="center", width=1)
            self.details_widgets[6].heading(column, text=column)
        self.controller.fill_details()

    def load_graph(self):
        """
        This method loads the graph section and its widgets, such as its label, graph figure,
        and graph canvas.
        """
        graph_title_label = ttk.Label(self.frame, style="tertiary.TLabel", text="Incident Graph")
        graph_title_label.pack(fill="both", side="top")
        self.graph_widgets[0] = plt.figure(facecolor=self.secondary_bg)
        self.graph_widgets[1] = self.graph_widgets[0].add_subplot(111)
        graph_canvas = FigureCanvasTkAgg(self.graph_widgets[0], master=self.frame).get_tk_widget()
        graph_canvas.configure(background=self.secondary_bg)
        graph_canvas.pack()

    def load_actions(self):
        """
        This method loads the actions section and its widgets, such as its frames, labels, combobox,
        and buttons.
        """
        actions_frame = tk.Frame(self.frame, background=self.secondary_bg)
        actions_frame.pack(expand=True, fill="both", side="top", pady=(15, 0), ipadx=60)
        actions_title_label = ttk.Label(actions_frame, style="tertiary.TLabel",
                                        text="Incident Actions")
        actions_title_label.pack(fill="both", side="top")
        actions_graph_label = ttk.Label(actions_frame, style="secondary.TLabel",
                                        text="Select Graph")
        actions_graph_label.pack(expand=True, side="left")
        actions_input = tk.StringVar()
        actions_graph_combobox = ttk.Combobox(actions_frame, state="readonly", width=30,
                                              font=(self.font, 12), textvariable=actions_input,
                                              values=[self.texts[0], self.columns[1],
                                                      self.columns[2], self.columns[3],
                                                      self.texts[1]])
        actions_graph_combobox.pack(expand=True, side="right")
        actions_graph_combobox.bind("<<ComboboxSelected>>",
                                    lambda e: self.select_graph(actions_input.get()))
        actions_button_frame = tk.Frame(self.frame, background=self.secondary_bg)
        actions_button_frame.pack(expand=True, fill="both", side="bottom")
        actions_graph_button = ttk.Button(actions_button_frame, takefocus=False,
                                          text="Export Graph", command=
                                          lambda: self.controller.export_graph(actions_input.get()))
        actions_graph_button.pack(expand=True, fill="both", side="left", padx=(0, 5), ipadx=5)
        actions_csv_button = ttk.Button(actions_button_frame, takefocus=False,
                                        text="Export CSV", command=self.controller.export_csv)
        actions_csv_button.pack(expand=True, fill="both", side="left", ipadx=2)

    def load_graph_style(self):
        """This method loads the graph style and sets its colors."""
        self.graph_widgets[1].set(facecolor=self.secondary_bg)
        self.graph_widgets[1].xaxis.label.set_color(self.primary_fg)
        self.graph_widgets[1].yaxis.label.set_color(self.primary_fg)
        self.graph_widgets[1].spines["top"].set_color(self.primary_fg)
        self.graph_widgets[1].spines["bottom"].set_color(self.primary_fg)
        self.graph_widgets[1].spines["left"].set_color(self.primary_fg)
        self.graph_widgets[1].spines["right"].set_color(self.primary_fg)
        self.graph_widgets[1].tick_params(color=self.primary_fg, labelcolor=self.primary_fg)

    def fill_details_labels(self, max_timestamp):
        """
        This method fills the details labels with the data of the maximum SVM timestamp.

        :param max_timestamp: Timestamp object with the maximum SVM value.
        """
        timestamp_data = [max_timestamp.get_date(), max_timestamp.get_time(),
                          round(max_timestamp.get_x_acc(), 8), round(max_timestamp.get_y_acc(), 8),
                          round(max_timestamp.get_z_acc(), 8), round(max_timestamp.get_svm(), 10)]
        for i, label in enumerate(self.details_widgets):
            if isinstance(label, ttk.Label):
                label_text = label.cget("text")
                self.details_widgets[i].configure(text=f"{label_text}  =  {str(timestamp_data[i])}")

    def fill_details_tree_view(self, timestamps: List):
        """
        This method fills the details treeview with the data of the incidents timestamps.

        :param timestamps: List of Timestamp objects.
        """
        for timestamp in timestamps:
            self.details_widgets[6].insert("", 0, tags=str(timestamp.get_timestamp_id() % 2),
                                           values=(timestamp.get_time(),
                                                   round(timestamp.get_x_acc(), 8),
                                                   round(timestamp.get_y_acc(), 8),
                                                   round(timestamp.get_z_acc(), 8),
                                                   round(timestamp.get_svm(), 10)))

    def select_graph(self, selected_graph: str):
        """
        This method clears the graph figure and passes the selected graph to fill_graph() of
        IncidentController.

        :param selected_graph: Name of selected graph.
        """
        self.graph_widgets[1].clear()
        self.controller.fill_graph(selected_graph)

    def plot_graph(self, time_data: List[float], acc_data: List[float], color: str):
        """
        This method plots a colored graph using the timestamps time-data and acceleration-data.

        :param time_data: Timestamps time-data for X-axis.
        :param acc_data: Timestamps acceleration-data for Y-axis.
        :param color: Color of graph.
        """
        self.graph_widgets[1].plot(time_data, acc_data, color=color, marker=".")

    def set_graph(self, time_data: List[float], selected_graph: str):
        """
        This method sets the title, labels, and legend of the graph depending on the name of the
        selected graph. It also sets the X-axis limit using the timestamps time-data.

        :param time_data: Timestamps time-data for X-axis.
        :param selected_graph: Name of selected graph.
        """
        self.graph_widgets[1].set(title=selected_graph, xlabel="Time (s)",
                                  xlim=(time_data[0], time_data[-1]))
        self.graph_widgets[1].title.set_color(self.primary_fg)
        self.graph_widgets[1].grid(color=self.primary_bg)
        if selected_graph == self.texts[0]:
            self.graph_widgets[1].legend(labels=[self.columns[1], self.columns[2], self.columns[3]],
                                         labelcolor=self.primary_fg, frameon=False)
        if selected_graph == self.texts[1]:
            self.graph_widgets[1].set(ylabel=self.columns[4])
        else:
            self.graph_widgets[1].set(ylabel="Acceleration (m/s$^2$)")
        self.graph_widgets[0].canvas.draw()

    def export_graph(self, graph_path: str):
        """
        This method exports the graph figure to the passed graph path.

        :param graph_path: Name of the graph path.
        """
        self.graph_widgets[0].savefig(graph_path)

    def get_graph_colors(self) -> Tuple:
        """
        This method gets the views graph colors.

        :returns: Tuple of the views graph colors.
        """
        return self.primary_fg, self.secondary_fg, self.tertiary_fg

    def stop_tree_view_resize(self, event):
        """
        This method stops the resizing of columns for the details tree view.

        :param event: Event to be stopped.
        """
        if self.details_widgets[6].identify_region(event.x, event.y) == "separator":
            return "break"
        return "continue"

    def start(self):
        self.load_root()
        self.load_header()
        self.load_details()
        self.load_graph()
        self.load_graph_style()
        self.load_actions()
        self.open(self)
        self.mainloop()
