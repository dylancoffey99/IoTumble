import tkinter as tk
from tkinter import ttk

from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from iotumble.views.abstract_view import AbstractView


class IncidentView(AbstractView, tk.Toplevel):
    def __init__(self, controller):
        super().__init__()
        self.withdraw()
        self.controller = controller
        self.icon = controller.home_view.icon
        self.header_logo = controller.home_view.header_logo
        self.details_labels = [ttk.Label()] * 5
        self.details_tree_view = ttk.Treeview()
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
        header_logo_label = ttk.Label(header_frame, style="primary.TLabel", image=self.header_logo)
        header_logo_label.pack(fill="both", side="left", padx=44)
        header_options_button = ttk.Button(header_frame, takefocus=False, style="header.TButton",
                                           text="Options")
        header_options_button.pack(fill="both", side="left", ipadx=42)
        header_back_button = ttk.Button(header_frame, takefocus=False, style="header.TButton",
                                        text="Back", command=self.controller.back)
        header_back_button.pack(fill="both", side="left", ipadx=55)
        for widget in [header_frame, header_logo_label]:
            widget.bind("<ButtonPress-1>", lambda e: self.pressed_window(self, True, e))
            widget.bind("<ButtonRelease-1>", lambda e: self.pressed_window(self, False, e))
            widget.bind("<B1-Motion>", lambda e: self.move_window(self, e))

    def load_details(self):
        details_frame = tk.Frame(self.frame, background=self.tertiary_bg)
        details_frame.pack(expand=True, fill="both", side="left")
        details_title_label = ttk.Label(details_frame, style="tertiary.TLabel",
                                        text="Incident Details")
        details_title_label.pack(fill="both", side="top")
        self.details_labels[0] = ttk.Label(details_frame, style="secondary.TLabel",
                                           text=self.columns[0])
        self.details_labels[0].pack(expand=True, fill="both", padx=(0, 15))
        self.details_labels[1] = ttk.Label(details_frame, style="secondary.TLabel",
                                           text=self.columns[1])
        self.details_labels[1].pack(expand=True, fill="both", padx=(0, 15))
        self.details_labels[2] = ttk.Label(details_frame, style="secondary.TLabel",
                                           text=self.columns[2])
        self.details_labels[2].pack(expand=True, fill="both", padx=(0, 15))
        self.details_labels[3] = ttk.Label(details_frame, style="secondary.TLabel",
                                           text=self.columns[3])
        self.details_labels[3].pack(expand=True, fill="both", padx=(0, 15))
        self.details_labels[4] = ttk.Label(details_frame, style="secondary.TLabel",
                                           text="Signal Vector Magnitude (SVM)")
        self.details_labels[4].pack(expand=True, fill="both", padx=(0, 15))
        self.details_tree_view = ttk.Treeview(details_frame, columns=self.columns, show="headings",
                                              selectmode="none", style="details.Treeview")
        self.details_tree_view.pack(expand=True, fill="both", side="left")
        details_scrollbar = ttk.Scrollbar(details_frame, orient="vertical",
                                          command=self.details_tree_view.yview)
        details_scrollbar.pack(fill="both", side="right")
        self.details_tree_view.configure(yscrollcommand=details_scrollbar.set)
        self.details_tree_view.tag_configure("0", background=self.secondary_bg)
        self.details_tree_view.tag_configure("1", background=self.primary_bg)
        self.details_tree_view.bind("<Button-1>", self.stop_tree_view_resize)
        for column in self.columns:
            self.details_tree_view.column(column, anchor="center", width=1)
            self.details_tree_view.heading(column, text=column)
        self.controller.fill_details()

    def load_graph(self):
        graph_title_label = ttk.Label(self.frame, style="tertiary.TLabel", text="Incident Graph")
        graph_title_label.pack(fill="both", side="top")
        graph = plt.figure(facecolor=self.secondary_bg)
        graph_canvas = FigureCanvasTkAgg(graph, master=self.frame).get_tk_widget()
        graph_canvas.pack()
        graph_plot = graph.add_subplot(111)
        self.load_graph_style(graph_plot)

    def load_actions(self):
        actions_frame = tk.Frame(self.frame, background=self.secondary_bg)
        actions_frame.pack(expand=True, fill="both", side="top", ipadx=60)
        actions_title_label = ttk.Label(actions_frame, style="tertiary.TLabel",
                                        text="Incident Actions")
        actions_title_label.pack(fill="both", side="top")
        actions_graph_label = ttk.Label(actions_frame, style="secondary.TLabel",
                                        text="Select Graph")
        actions_graph_label.pack(expand=True, side="left")
        actions_graph_combobox = ttk.Combobox(actions_frame, state="readonly", width=30,
                                              font=(self.font, 12),
                                              values=["All Acceleration", self.columns[1],
                                                      self.columns[2], self.columns[3],
                                                      self.columns[4]])
        actions_graph_combobox.pack(expand=True, side="right")
        actions_button_frame = tk.Frame(self.frame, background=self.secondary_bg)
        actions_button_frame.pack(expand=True, fill="both", side="bottom")
        actions_graph_button = ttk.Button(actions_button_frame, takefocus=False,
                                          text="Export Graph")
        actions_graph_button.pack(expand=True, fill="both", side="left", ipadx=8)
        actions_details_button = ttk.Button(actions_button_frame, takefocus=False,
                                            text="Export Details")
        actions_details_button.pack(expand=True, fill="both", side="left", padx=5, ipadx=5)
        actions_delete_button = ttk.Button(actions_button_frame, takefocus=False,
                                           text="Delete Incident")
        actions_delete_button.pack(expand=True, fill="both", side="left", ipadx=2)

    def load_graph_style(self, graph_plot):
        graph_plot.set(facecolor=self.secondary_bg)
        graph_plot.xaxis.label.set_color(self.primary_fg)
        graph_plot.yaxis.label.set_color(self.primary_fg)
        graph_plot.title.set_color(self.primary_fg)
        graph_plot.tick_params(color=self.primary_fg, labelcolor=self.primary_fg)
        graph_plot.spines["top"].set_color(self.primary_fg)
        graph_plot.spines["bottom"].set_color(self.primary_fg)
        graph_plot.spines["left"].set_color(self.primary_fg)
        graph_plot.spines["right"].set_color(self.primary_fg)

    def fill_details_labels(self, timestamp_data):
        for i, label in enumerate(self.details_labels):
            label_text = label.cget("text")
            self.details_labels[i].config(text=f"{label_text} = {str(timestamp_data[i])}")

    def fill_details_tree_view(self, timestamps):
        for timestamp in timestamps:
            self.details_tree_view.insert("", "end", tags=str(timestamp.get_timestamp_id() % 2),
                                          values=(timestamp.get_time(), timestamp.get_x_acc(),
                                                  timestamp.get_y_acc(), timestamp.get_z_acc(),
                                                  timestamp.get_svm()))

    def stop_tree_view_resize(self, event):
        if self.details_tree_view.identify_region(event.x, event.y) == "separator":
            return "break"
        return "continue"

    def start(self):
        self.load_root()
        self.load_header()
        self.load_details()
        self.load_graph()
        self.load_actions()
        self.open(self)
        self.mainloop()

    def close(self):
        self.icon.unbind("<Map>")
        self.icon.unbind("<Unmap>")
        self.destroy()
