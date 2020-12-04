import tkinter as tk
from tkinter import ttk
import tkinter.font as tkFont
from session import Session

class App(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.master.configure(background="#1E1E1E")
        self.pack()
        self.fonts()
        self.tvars()
        self.construct_widget()
        self.session = Session()
        self.playback_running = False

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

    def tvars(self):
        self.open_label = tk.StringVar()
        self.open_label.set("Open")
        self.close_label = tk.StringVar()
        self.close_label.set("Close")
        self.high_label = tk.StringVar()
        self.high_label.set("High")
        self.low_label = tk.StringVar()
        self.low_label.set("Low")
        self.symbol = tk.StringVar()
        self.symbol_name = tk.StringVar()
        self.buy_label = tk.StringVar()
        self.buy_label.set("Buy\n0.00")
        self.sell_label = tk.StringVar()
        self.sell_label.set("Sell\n0.00")
        self.play_pause_label = tk.StringVar()
        self.play_pause_label.set("▶")
        

    def construct_widget(self):
        # Main GUI
        rowcount = 0

        # Symbol
        tk.Label(self,
                 textvariable=self.symbol,
                 font=self.font_normal,
                 width=15
                 ).grid(row=rowcount, column=0, columnspan=4, sticky="nsew",
                        padx=5, pady=5)
        rowcount += 1

        # Symbol Full Name
        tk.Label(self,
                 textvariable=self.symbol_name
                 ).grid(row=rowcount, column=0, columnspan=4, sticky="nsew")
        rowcount += 1

        ttk.Separator(self).grid(row=rowcount, column=0, columnspan=4,
                                 sticky="nsew")
        rowcount += 1

        # Buy Button
        tk.Button(self,
                  textvariable=self.buy_label,
                  font=self.font_esmall
                  ).grid(row=rowcount, column=0, columnspan=2, sticky="nsew",
                         padx=5, pady=5)

        # Sell Button
        tk.Button(self,
                  textvariable=self.sell_label,
                  font=self.font_esmall
                  ).grid(row=rowcount, column=2, columnspan=2, sticky="nsew",
                         padx=5, pady=5)
        rowcount += 1

        ttk.Separator(self).grid(row=rowcount, column=0, columnspan=4,
                                 sticky="nsew")
        rowcount += 1

        # Initialize replay
        tk.Button(self,
                  text="Fetch",
                  font=self.font_small,
                  command=self.fetch
                  ).grid(row=rowcount, column=0, columnspan=2, sticky="nsew",
                         padx=5, pady=5)
        tk.Button(self,
                  text="◀◀",
                  font=self.font_small,
                  command=self.replay
                  ).grid(row=rowcount, column=2, columnspan=2, sticky="nsew",
                         padx=5, pady=5)
        rowcount += 1

        # Play / Pause the replay
        tk.Button(self,
                  textvariable=self.play_pause_label,
                  font=self.font_small,
                  command=self.play_pause
                  ).grid(row=rowcount, column=0, columnspan=2, sticky="nsew",
                         padx=5, pady=5)

        # Advance the bar by one
        tk.Button(self,
                  text="⏯",
                  font=self.font_small,
                  command=self.bar_fwd
                  ).grid(row=rowcount, column=2,  columnspan=2, sticky="nsew",
                         padx=5, pady=5)
        rowcount += 1

        ttk.Separator(self).grid(row=rowcount, column=0, columnspan=4,
                                 sticky="nsew")
        rowcount += 1

        # OHLC Data of surrent candle
        ttk.Label(self,
                  textvariable=self.open_label
                  ).grid(row=rowcount, column=0, columnspan=1, sticky="nsew")

        ttk.Label(self,
                  textvariable=self.close_label
                  ).grid(row=rowcount, column=1, columnspan=1, sticky="nsew")

        ttk.Label(self,
                  textvariable=self.high_label
                  ).grid(row=rowcount, column=2, columnspan=1, sticky="nsew")

        ttk.Label(self,
                  textvariable=self.low_label
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

        ttk.Separator(self).grid(row=rowcount, column=0, columnspan=4,
                                 sticky="nsew")
        rowcount += 1

        # Positions

        tk.Label(self, text="Positions", font=self.font_esmall
                 ).grid(row=rowcount, column=0, columnspan=4, sticky="nsew")
        rowcount += 1

        tk.Label(self, text="Long Bitcoinnnn @ 123456789 Q.1,00,00,00,000"
                 ).grid(row=rowcount, column=0, columnspan=4, sticky="w")
        rowcount += 1

        ttk.Separator(self).grid(row=rowcount, column=0, columnspan=4,
                                 sticky="nsew")
        rowcount += 1

        tk.Label(self, text="Trade History", font=self.font_esmall
                 ).grid(row=rowcount, column=0, columnspan=4, sticky="nsew")
        rowcount += 1

        positions = tk.Listbox(self, height=3)
        positions.grid(row=rowcount, column=0, columnspan=4, sticky="nsew")
        positions.insert(tk.END, "..")
    
    def fetch(self):
        name = self.session.get_name()
        self.symbol.set(name)
        fname = self.session.get_fname()
        self.symbol_name.set(fname)


    def routine_task(self):
        ohlc = self.session.get_ohlc()
        if ohlc is not None:

            self.open_label.set("Open\n{}".format(ohlc["open"]))
            self.close_label.set("Close\n{}".format(ohlc["close"]))
            self.high_label.set("High\n{}".format(ohlc["high"]))
            self.low_label.set("Low\n{}".format(ohlc["low"]))
            self.buy_label.set("Buy\n{}".format(ohlc["close"]))
            self.sell_label.set("Sell\n{}".format(ohlc["close"]))
        if self.playback_running:
            self.after(200,self.routine_task)

    def replay(self):
        self.session.click_replay()

    def play_pause(self):
        if self.playback_running:
            self.playback_running = False
        else:
            self.playback_running = True
        
        self.routine_task()
        self.session.click_pause_play()

    def bar_fwd(self):
        self.session.click_fwd_bar()

    


root = tk.Tk()
root.title('Trainer')

app = App(root)
app.configure()
app.mainloop()
