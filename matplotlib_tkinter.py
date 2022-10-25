import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
import yfinance as yf
import datetime
import numpy as np

plt.style.use('ggplot')


def plot_stock_price(price_data, name=None):
    plt.clf()
    plt.plot(price_data["Close"])
    ax = plt.gca()
    if name:
        ax.set(title=f'{name} Close Price')
    else:
        ax.set(title='Close Price')
    # just plt.draw() won't do!
    plt.gcf().canvas.draw()


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
        stock_label.grid(row=2, column=0)

        self.stock_num = tk.StringVar()
        self.stock_num.trace_add('write', self.choose_stock)

        self.stock_choice = ttk.Combobox(self, textvariable=self.stock_num)
        self.stock_choice['values'] = ('BARC.L',
                                       'MKS.L',
                                       'MSFT',
                                       'AMZN',
                                       'T',
                                       'DIS')
        self.stock_choice.current(0)
        self.stock_choice.grid(row=3, column=0, padx=10)

        fig = Figure(figsize=(5, 4), dpi=100)
        canvas = FigureCanvasTkAgg(fig, master=self)
        # canvas.draw()

        toolbar = NavigationToolbar2Tk(canvas, self, pack_toolbar=False)
        canvas.get_tk_widget().grid(row=1, column=1, rowspan=6, padx=10, pady=5)
        toolbar.grid(row=7, column=1, pady=5)

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
        plot_stock_price(self.stock_df, name=name)


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Graphs in Tkinter")
    # root.geometry("500x500")
    graph_page = GraphPage()
    graph_page.pack()
    root.mainloop()
