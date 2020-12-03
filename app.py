import tkinter as tk
from tkinter import ttk
import tkinter.font as tkFont 

class App(tk.Frame):
    
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.master.configure(background="#1E1E1E")
        self.pack()
        self.fonts()
        self.construct_widget()

    def fonts(self):
        self.font_normal = tkFont.Font(family="Times New Roman", weight="bold", size=20)
        self.font_large = tkFont.Font(family="Times New Roman", weight="bold", size=round(20 * 1.5))
        self.font_small = tkFont.Font(family="Times New Roman", weight="bold", size=round(20 * .66))
    
    def construct_widget(self):
        tk.Label(self, text="BITCOI", font=self.font_normal, width=15).grid(row=0, column=0, columnspan=4, sticky="nsew", padx=5, pady=5)
        tk.Label(self, text="BITCOIN PTV. LTD.").grid(row=1, column=0, columnspan=4, sticky="nsew")
        ttk.Separator(self).grid(row=2,column=0,columnspan=4,sticky="nsew")
        tk.Button(self, text="BUY\n$2020", font=self.font_small).grid(row=3, column=0, columnspan=2, sticky="nsew", padx=5, pady=5)
        tk.Button(self, text="SELL\n$2020", font=self.font_small).grid(row=3, column=2, columnspan=2, sticky="nsew", padx=5, pady=5)
        ttk.Separator(self).grid(row=4,column=0,columnspan=4,sticky="nsew")
        tk.Button(self, text="◀◀", font=self.font_small).grid(row=5, column=0, columnspan=4, sticky="nsew", padx=5, pady=5)
        tk.Button(self, text="▶", font=self.font_small).grid(row=6, column=0, columnspan=2, sticky="nsew", padx=5, pady=5)
        tk.Button(self, text="⏯", font=self.font_small).grid(row=6, column=2,  columnspan=2,sticky="nsew", padx=5, pady=5)
        ttk.Separator(self).grid(row=7,column=0,columnspan=4,sticky="nsew")
        tabscon = ttk.Notebook(self)
        tab1 = ttk.Frame(tabscon)
        tab2 = ttk.Frame(tabscon)
        tabscon.add(tab1, text="Market")
        tabscon.add(tab2, text="Limit")
        tabscon.grid(row=8,column=0,columnspan=4, sticky="nsew")
        tab1.grid_columnconfigure(1,weight=1)
        tk.Label(tab1, text="MARKET ORDER", font=self.font_small).grid(row=0, column=0,  columnspan=4,sticky="nsew", padx=5, pady=5)
        tk.Label(tab1, text="Quantity").grid(row=1, column=0,  columnspan=1,sticky="nsew", padx=5, pady=5)
        tk.Entry(tab1).grid(row=1, column=1,  columnspan=3,sticky="nsew", padx=5, pady=5)
        tk.Label(tab1, text="Take Profit").grid(row=2, column=0,  columnspan=1,sticky="nsew", padx=5, pady=5)
        tk.Entry(tab1).grid(row=2, column=1,  columnspan=3,sticky="nsew", padx=5, pady=5)
        tk.Label(tab1, text="Stop Loss").grid(row=3, column=0,  columnspan=1,sticky="nsew", padx=5, pady=5)
        tk.Entry(tab1).grid(row=3, column=1,  columnspan=3,sticky="nsew", padx=5, pady=5)

        tk.Button(self, text="Place Order").grid(row=10,column=0,columnspan=4, sticky="nsew", padx=5, pady=5)



root = tk.Tk()
root.title('Trainer')

app = App(root)
app.configure()
app.mainloop()
