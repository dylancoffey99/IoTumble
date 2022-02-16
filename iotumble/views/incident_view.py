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
        self.details_widgets = [ttk.Label(), ttk.Label(), ttk.Label(),ttk.Label(),
                                ttk.Label(), ttk.Label(), ttk.Treeview()]
        self.graph_widgets = [plt.figure(), None]
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
        self.details_widgets[0] = ttk.Label(details_frame, style="secondary.TLabel",
                                            text="Date")
        self.details_widgets[0].pack(expand=True, fill="both", padx=(0, 15))
        self.details_widgets[1] = ttk.Label(details_frame, style="secondary.TLabel",
                                            text=self.columns[0])
        self.details_widgets[1].pack(expand=True, fill="both", padx=(0, 15))
        self.details_widgets[2] = ttk.Label(details_frame, style="secondary.TLabel",
                                            text=self.columns[1])
        self.details_widgets[2].pack(expand=True, fill="both", padx=(0, 15))
        self.details_widgets[3] = ttk.Label(details_frame, style="secondary.TLabel",
                                            text=self.columns[2])
        self.details_widgets[3].pack(expand=True, fill="both", padx=(0, 15))
        self.details_widgets[4] = ttk.Label(details_frame, style="secondary.TLabel",
                                            text=self.columns[3])
        self.details_widgets[4].pack(expand=True, fill="both", padx=(0, 15))
        self.details_widgets[5] = ttk.Label(details_frame, style="secondary.TLabel",
                                            text=self.texts[1])
        self.details_widgets[5].pack(expand=True, fill="both", padx=(0, 15))
        self.details_widgets[6] = ttk.Treeview(details_frame, columns=self.columns,
                                               show="headings", selectmode="none",
                                               style="details.Treeview")
        self.details_widgets[6].pack(expand=True, fill="both", side="left")
        details_scrollbar = ttk.Scrollbar(details_frame, orient="vertical",
                                          command=self.details_widgets[6].yview)
        details_scrollbar.pack(fill="both", side="right")
        self.details_widgets[6].configure(yscrollcommand=details_scrollbar.set)
        self.details_widgets[6].tag_configure("0", background=self.secondary_bg)
        self.details_widgets[6].tag_configure("1", background=self.primary_bg)
        self.details_widgets[6].bind("<Button-1>", self.stop_tree_view_resize)
        for column in self.columns:
            self.details_widgets[6].column(column, anchor="center", width=1)
            self.details_widgets[6].heading(column, text=column)
        self.controller.fill_details()

    def load_graph(self):
        graph_title_label = ttk.Label(self.frame, style="tertiary.TLabel", text="Incident Graph")
        graph_title_label.pack(fill="both", side="top")
        graph_figure = plt.figure(facecolor=self.secondary_bg)
        self.graph_widgets[0] = graph_figure.add_subplot(111)
        self.graph_widgets[1] = FigureCanvasTkAgg(graph_figure, master=self.frame)
        graph_plot = self.graph_widgets[1].get_tk_widget()
        graph_plot.pack()
        self.load_graph_style()

    def load_actions(self):
        actions_frame = tk.Frame(self.frame, background=self.secondary_bg)
        actions_frame.pack(expand=True, fill="both", side="top", ipadx=60)
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
                                    lambda e: self.select_graph(actions_input))
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

    def load_graph_style(self):
        self.graph_widgets[0].set(facecolor=self.secondary_bg)
        self.graph_widgets[0].xaxis.label.set_color(self.primary_fg)
        self.graph_widgets[0].yaxis.label.set_color(self.primary_fg)
        self.graph_widgets[0].spines["top"].set_color(self.primary_fg)
        self.graph_widgets[0].spines["bottom"].set_color(self.primary_fg)
        self.graph_widgets[0].spines["left"].set_color(self.primary_fg)
        self.graph_widgets[0].spines["right"].set_color(self.primary_fg)
        self.graph_widgets[0].tick_params(color=self.primary_fg, labelcolor=self.primary_fg)

    def fill_details_labels(self, timestamp):
        timestamp_data = [timestamp.get_date(), timestamp.get_time(), timestamp.get_x_acc(),
                          timestamp.get_y_acc(), timestamp.get_z_acc(), timestamp.get_svm()]
        for i, label in enumerate(self.details_widgets):
            if isinstance(label, ttk.Label):
                label_text = label.cget("text")
                self.details_widgets[i].config(text=f"[{label_text}]  =  {str(timestamp_data[i])}")

    def fill_details_tree_view(self, timestamps):
        for timestamp in timestamps:
            self.details_widgets[6].insert("", "end", tags=str(timestamp.get_timestamp_id() % 2),
                                           values=(timestamp.get_time(), timestamp.get_x_acc(),
                                                   timestamp.get_y_acc(), timestamp.get_z_acc(),
                                                   timestamp.get_svm()))

    def select_graph(self, actions_input):
        selected_graph = actions_input.get()
        self.graph_widgets[0].clear()
        self.graph_widgets[1].draw_idle()
        self.controller.fill_graph(selected_graph)

    def plot_graph(self, time, data, color):
        self.graph_widgets[0].plot(time, data, color=color)

    def set_graph(self, time, selected_graph):
        self.graph_widgets[0].title.set_color(self.primary_fg)
        self.graph_widgets[0].set(title=selected_graph, xlabel="Time (s)", xlim=(time[0], time[-1]))
        if selected_graph == self.texts[0]:
            self.graph_widgets[0].legend(labels=[self.columns[1], self.columns[2], self.columns[3]],
                                         facecolor=self.secondary_bg, edgecolor=self.secondary_bg,
                                         labelcolor=self.primary_fg)
        if selected_graph == self.texts[1]:
            self.graph_widgets[0].set(ylabel=self.columns[4])
        else:
            self.graph_widgets[0].set(ylabel="Acceleration ($m/s^2$)")

    def get_graph_colors(self):
        return self.primary_fg, self.secondary_fg, self.tertiary_fg

    def stop_tree_view_resize(self, event):
        if self.details_widgets[6].identify_region(event.x, event.y) == "separator":
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
        self.destroy()
