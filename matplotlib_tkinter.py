import tkinter as tk
from tkinter import ttk
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
import yfinance as yf
import datetime
import numpy as np

plt.style.use('ggplot')
matplotlib.use('TkAgg', force=True)


def plot_stock_price(price_data, name=None, ax=None):
    if ax is None:
        ax = plt.gca()
    ax.clear()
    ax.plot(price_data["Close"])
    if name:
        ax.set(title=f'{name} Close Price')
    else:
        ax.set(title='Close Price')
    return ax


def get_stock_data(ticker):
    stock_info = yf.Ticker(ticker)
    price_df = yf.download(ticker, start='2000-01-01', end=datetime.date.today())
    price_df['log_ret'] = np.log(price_df["Adj Close"]) - np.log(price_df["Adj Close"].shift(1))
    return price_df, stock_info


class GraphPage(tk.Frame):
    def __init__(self):
        super().__init__()

        title = tk.Label(self, text='Stock Price Viewer',
                         padx=10, pady=10, font=('Arial', 14))
        title.grid(row=0, column=1)

        stock_label = tk.Label(self, text='Choose stock:')
        stock_label.grid(row=1, column=0, sticky='s')

        self.tk_axes = None
        self.stock_num = tk.StringVar()

        self.stock_choice = ttk.Combobox(self, textvariable=self.stock_num)
        self.stock_choice['values'] = ('BARC.L',
                                       'MKS.L',
                                       'MSFT',
                                       'AMZN',
                                       'T',
                                       'DIS')
        self.stock_choice.current(0)
        self.stock_choice.grid(row=2, column=0, padx=10, sticky='n')

        self.fig = Figure(figsize=(5, 4), dpi=100)
        self.tk_axes = self.fig.add_subplot()
        self.tk_canvas = FigureCanvasTkAgg(self.fig, master=self)

        # Code will run self.choose_stock when ever the stock_num variable changes
        # (via the stock_choice Combobox
        self.stock_num.trace_add('write', self.choose_stock)

        toolbar = NavigationToolbar2Tk(self.tk_canvas, self, pack_toolbar=False)
        self.tk_canvas.get_tk_widget().grid(row=1, column=1, rowspan=2, padx=10, pady=5)
        toolbar.grid(row=3, column=1, pady=5)

        self.stock_df = None
        self.stock_info = None
        # Will get stock info according to the ticker selected in the ComboBox
        self.choose_stock()

    def choose_stock(self, *args):
        # Gets the stock code that is currently chosen in the stock ComboBox
        stock = self.stock_choice.get()
        print(stock)
        # Retrieves stock prices and info about the stock
        self.stock_df, self.stock_info = get_stock_data(stock)
        self.plot_graph()

    # Plot the current stock data
    def plot_graph(self):
        name = self.stock_info.info['shortName']
        plot_stock_price(self.stock_df, name=name, ax=self.tk_axes)

        # update tk_canvas
        self.tk_canvas.draw()


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Graphs in Tkinter")
    # root.geometry("500x500")
    graph_page = GraphPage()
    graph_page.pack()
    root.mainloop()
