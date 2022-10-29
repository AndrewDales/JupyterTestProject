import tkinter as tk
from tkinter import Tk, Button
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure


class GraphFrame(tk.Frame):
    def __init__(self):
        super().__init__()
        self.shift = 0

        # Draw button
        draw_button = Button(self, text="Shift!", command=self.plot_shift)

        # Figure and tk_canvas
        self.fig = Figure(figsize=(5, 4), dpi=100)
        self.ax = self.fig.add_subplot()
        self.canvas = FigureCanvasTkAgg(self.fig, master=self)

        # Toolbar
        toolbar = NavigationToolbar2Tk(self.canvas, self, pack_toolbar=False)
        # Allows key to control the toolbar
        self.canvas.mpl_connect("key_press_event", key_press_handler)

        # Use grid to place elements
        draw_button.grid(row=0, column=0, padx=(10, 5))
        self.canvas.get_tk_widget().grid(row=0, column=1, padx=5, pady=5)
        toolbar.grid(row=1, column=1)

        # Draw the plot
        self.draw_plot()

    def draw_plot(self):
        x = np.arange(0.0, 4 * np.pi, 0.01)
        self.ax.clear()
        self.ax.plot(x, np.sin(x + self.shift),
                     label=rf'$\sin(x + {{{self.shift:.1f}}})$')
        self.ax.set_title(f'Sine wave shifted left {self.shift:.1f} radians')
        self.ax.legend(loc='upper right')

        # update tk_canvas
        self.canvas.draw()

    def plot_shift(self):
        self.shift += 0.1
        self.draw_plot()


plt.style.use('ggplot')
# GUI
# matplotlib.use('TkAgg')
root = Tk()
root.title("Sample Sine Wave Graph in Tkinter")
graph_page = GraphFrame()
graph_page.pack()

root.mainloop()
