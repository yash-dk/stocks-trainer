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
        """
            Create standard font sizes.
        """
        self.font_normal = tkFont.Font(
            family="Times New Roman",
            weight="bold", size=20)

        self.font_large = tkFont.Font(
            family="Times New Roman",
            weight="bold",
            size=round(20 * 1.5))

        self.font_small = tkFont.Font(
            family="Times New Roman",
            weight="bold",
            size=round(20 * .66))

        self.font_esmall = tkFont.Font(
            family="Times New Roman",
            weight="bold",
            size=round(20 * .45))

    def construct_widget(self):
        # Main GUI
        rowcount = 0

        # Symbol
        tk.Label(self,
                 text="BITCOIN",
                 font=self.font_normal,
                 width=15
                 ).grid(row=rowcount, column=0, columnspan=4, sticky="nsew",
                        padx=5, pady=5)
        rowcount += 1

        # Symbol Full Name
        tk.Label(self,
                 text="BITCOIN PTV. LTD."
                 ).grid(row=rowcount, column=0, columnspan=4, sticky="nsew")
        rowcount += 1

        ttk.Separator(self).grid(row=rowcount, column=0, columnspan=4,
                                 sticky="nsew")
        rowcount += 1

        # Buy Button
        tk.Button(self,
                  text="BUY\n$2020",
                  font=self.font_esmall
                  ).grid(row=rowcount, column=0, columnspan=2, sticky="nsew",
                         padx=5, pady=5)

        # Sell Button
        tk.Button(self,
                  text="SELL\n$2020",
                  font=self.font_esmall
                  ).grid(row=rowcount, column=2, columnspan=2, sticky="nsew",
                         padx=5, pady=5)
        rowcount += 1

        ttk.Separator(self).grid(row=rowcount, column=0, columnspan=4,
                                 sticky="nsew")
        rowcount += 1

        # Initialize replay
        tk.Button(self,
                  text="◀◀",
                  font=self.font_small
                  ).grid(row=rowcount, column=0, columnspan=4, sticky="nsew",
                         padx=5, pady=5)
        rowcount += 1

        # Play / Pause the replay
        tk.Button(self,
                  text="▶",
                  font=self.font_small
                  ).grid(row=rowcount, column=0, columnspan=2, sticky="nsew",
                         padx=5, pady=5)

        # Advance the bar by one
        tk.Button(self,
                  text="⏯",
                  font=self.font_small
                  ).grid(row=rowcount, column=2,  columnspan=2, sticky="nsew",
                         padx=5, pady=5)
        rowcount += 1

        ttk.Separator(self).grid(row=rowcount, column=0, columnspan=4,
                                 sticky="nsew")
        rowcount += 1

        # OHLC Data of surrent candle
        ttk.Label(self,
                  text="open\n15.12"
                  ).grid(row=rowcount, column=0, columnspan=1, sticky="nsew")

        ttk.Label(self,
                  text="close\n15.10"
                  ).grid(row=rowcount, column=1, columnspan=1, sticky="nsew")

        ttk.Label(self,
                  text="high\n16.10"
                  ).grid(row=rowcount, column=2, columnspan=1, sticky="nsew")

        ttk.Label(self,
                  text="low\n10.25"
                  ).grid(row=rowcount, column=3, columnspan=1, sticky="nsew")
        rowcount += 1

        ttk.Separator(self).grid(row=rowcount, column=0, columnspan=4,
                                 sticky="nsew")
        rowcount += 1

        # Limit order and Market Order Tabs
        orderstab = ttk.Notebook(self)

        # Market Tab
        markettab = ttk.Frame(orderstab)
        # Limit Tab
        limittab = ttk.Frame(orderstab)

        orderstab.add(markettab, text="Market")
        orderstab.add(limittab, text="Limit")

        # Add tabs to main GUI
        orderstab.grid(row=rowcount, column=0, columnspan=4, sticky="nsew")
        rowcount += 1

        # Configure Market Tab
        markettab.grid_columnconfigure(1, weight=1)
        tk.Label(markettab,
                 text="MARKET ORDER",
                 font=self.font_esmall
                 ).grid(row=0, column=0,  columnspan=4, sticky="nsew",
                        padx=5, pady=5)

        tk.Label(markettab,
                 text="Quantity"
                 ).grid(row=1, column=0,  columnspan=1, sticky="nsew",
                        padx=5, pady=5)

        tk.Entry(markettab
                 ).grid(row=1, column=1,  columnspan=2, sticky="nsew",
                        padx=5, pady=5)
        
        tk.Button(markettab,
                 text="MAX"
                 ).grid(row=1, column=3,  columnspan=1, sticky="nsew",
                        padx=5, pady=5)

        tk.Label(markettab,
                 text="Take Profit"
                 ).grid(row=2, column=0,  columnspan=1, sticky="nsew",
                        padx=5, pady=5)

        tk.Entry(markettab
                 ).grid(row=2, column=1,  columnspan=3, sticky="nsew",
                        padx=5, pady=5)

        tk.Label(markettab,
                 text="Stop Loss"
                 ).grid(row=3, column=0,  columnspan=1, sticky="nsew",
                        padx=5, pady=5)

        tk.Entry(markettab
                 ).grid(row=3, column=1,  columnspan=3, sticky="nsew",
                        padx=5, pady=5)

        # Configure Limit Tab
        limittab.grid_columnconfigure(1, weight=1)
        tk.Label(limittab,
                 text="LIMIT ORDER",
                 font=self.font_esmall
                 ).grid(row=0, column=0,  columnspan=4, sticky="nsew",
                        padx=5, pady=5)

        tk.Label(limittab,
                 text="Order Price"
                 ).grid(row=1, column=0,  columnspan=1, sticky="nsew",
                        padx=5, pady=5)

        tk.Entry(limittab
                 ).grid(row=1, column=1,  columnspan=3, sticky="nsew",
                        padx=5, pady=5)

        tk.Label(limittab,
                 text="Quantity"
                 ).grid(row=2, column=0,  columnspan=1, sticky="nsew",
                        padx=5, pady=5)

        tk.Entry(limittab
                 ).grid(row=2, column=1,  columnspan=3, sticky="nsew",
                        padx=5, pady=5)

        tk.Label(limittab,
                 text="Take Profit"
                 ).grid(row=3, column=0,  columnspan=1, sticky="nsew",
                        padx=5, pady=5)

        tk.Entry(limittab
                 ).grid(row=3, column=1,  columnspan=3, sticky="nsew",
                        padx=5, pady=5)

        tk.Label(limittab,
                 text="Stop Loss"
                 ).grid(row=4, column=0,  columnspan=1, sticky="nsew",
                        padx=5, pady=5)

        tk.Entry(limittab
                 ).grid(row=4, column=1,  columnspan=3, sticky="nsew",
                        padx=5, pady=5)

        tk.Button(self,
                  text="Place Order"
                  ).grid(row=rowcount, column=0, columnspan=4, sticky="nsew",
                         padx=5, pady=5)
        rowcount += 1

        # Positions
        
        tk.Label(self,text="Positions", font=self.font_esmall).grid(row=rowcount, column=0, columnspan=4, sticky="nsew")
        rowcount += 1
        
        positions = tk.Listbox(self)
        positions.grid(row=rowcount, column=0, columnspan=4, sticky="nsew")
        positions.insert(tk.END, "B.BITCOINNNN @ 200,000 Q.100,000")

root = tk.Tk()
root.title('Trainer')

app = App(root)
app.configure()
app.mainloop()
