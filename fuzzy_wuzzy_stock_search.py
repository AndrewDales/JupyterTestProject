import tkinter as tk
from fuzzywuzzy import process
import requests

# Get S&P500 components in JSON format
r = requests.get('https://pkgstore.datahub.io/core/s-and-p-500-companies/constituents_json/data'
                 '/87cab5b5abab6c61eafa6dfdfa068a42/constituents_json.json')
stock_list = r.json()
stock_list = [{k: v for k, v in sk.items() if k == "Name" or k == "Symbol"} for sk in stock_list]


def find_stock(partial_name):
    return process.extract(partial_name, stock_list)


class SearchFrame(tk.Frame):
    def __init__(self):
        super().__init__()
        self.search_string = tk.StringVar()
        self.lb_var = tk.StringVar()
        self.lb_var.set("")
        self.result_string = tk.StringVar()
        self.result_string.set("")
        instr_label = tk.Label(self, text="Enter the stock name or code",
                               padx=10, pady=10, font=('Arial', 10))
        instr_label.grid(row=0, column=0)
        self.search_box = tk.Entry(self, textvariable=self.search_string)
        self.search_box.grid(row=1, column=0)
        self.found_lb = tk.Listbox(self, listvariable=self.lb_var, bd=0, height=5)

        self.result_box = tk.Label(self, textvariable=self.result_string,
                                   padx=10, pady=10)
        self.result_box.grid(row=3, column=0)
        self.search_box.focus()

        self.search_string.trace_add('write', self.change_name)
        self.found_lb.bind("<<ListboxSelect>>", self.select_name)

        # Placeholder for the list of stocks matching the search criteria
        self.found_list = []

    def change_name(self, *args):
        search = self.search_box.get()
        if search:
            self.found_list = find_stock(search)
            found_names = [sk[0]['Name'] for sk in self.found_list]
            self.lb_var.set(found_names)
            self.found_lb.grid(row=2, column=0, padx=10, pady=(0, 10))
            self.found_lb.select_set(0)
            self.search_box.focus()
        else:

            self.lb_var.set("")
            self.found_lb.grid_forget()

    def select_name(self, event):
        select_num = self.found_lb.curselection()
        if select_num:
            select_num = select_num[0]
            self.result_string.set(self.found_list[select_num][0]["Symbol"])
        else:
            self.result_string.set("")


if __name__ == "__main__":
    root = tk.Tk()
    sf = SearchFrame()
    sf.pack()
    root.mainloop()

