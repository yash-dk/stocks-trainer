import tkinter as tk
from tkinter import ttk
import tkinter.font as tkFont
from session import Session, Position, Trade


class App(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.master.configure(background="#121212")
        self.pack()
        self.fonts()
        self.tvars()
        self.bg_color = "#121212"
        self.fg_color = "#ffffff"
        self.configure(bg=self.bg_color)
        self.construct_widget()
        self.session = Session()
        self.playback_running = False
        self.current_position = None
        self.order_type = None
        self.order_side = None
        
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
        self.position_str = tk.StringVar()
        
    def construct_widget(self):
        # Main GUI
        rowcount = 0

        # Symbol
        tk.Label(self,
                 textvariable=self.symbol,
                 font=self.font_normal,
                 width=15,
                 bg=self.bg_color,
                 fg=self.fg_color
                 ).grid(row=rowcount, column=0, columnspan=4, sticky="nsew",
                        padx=5, pady=5)
        rowcount += 1

        # Symbol Full Name
        tk.Label(self,
                 textvariable=self.symbol_name,
                 bg=self.bg_color,
                 fg=self.fg_color
                 ).grid(row=rowcount, column=0, columnspan=4, sticky="nsew")
        rowcount += 1

        ttk.Separator(self).grid(row=rowcount, column=0, columnspan=4,
                                 sticky="nsew")
        rowcount += 1

        # Buy Button
        self.buy_button = tk.Button(self,
                                    textvariable=self.buy_label,
                                    font=self.font_esmall,
                                    command=self.buy_button_cmd,
                                    bg=self.bg_color,
                                    fg=self.fg_color
                                    )
        self.buy_button.grid(row=rowcount, column=0, columnspan=2, 
                             sticky="nsew", padx=5, pady=5)

        # Sell Button
        self.sell_button = tk.Button(self,
                                     textvariable=self.sell_label,
                                     font=self.font_esmall,
                                     bg=self.bg_color,
                                     fg=self.fg_color
                                     )
        self.sell_button.grid(row=rowcount, column=2, columnspan=2, 
                              sticky="nsew", padx=5, pady=5)
        rowcount += 1

        ttk.Separator(self).grid(row=rowcount, column=0, columnspan=4,
                                 sticky="nsew")
        rowcount += 1

        # Initialize replay
        tk.Button(self,
                  text="Fetch",
                  font=self.font_small,
                  command=self.fetch,
                  bg=self.bg_color,
                  fg=self.fg_color
                  ).grid(row=rowcount, column=0, columnspan=2, sticky="nsew",
                         padx=5, pady=5)
        tk.Button(self,
                  text="◀◀",
                  font=self.font_small,
                  command=self.replay,
                  bg=self.bg_color,
                  fg=self.fg_color
                  ).grid(row=rowcount, column=2, columnspan=2, sticky="nsew",
                         padx=5, pady=5)
        rowcount += 1

        # Play / Pause the replay
        tk.Button(self,
                  textvariable=self.play_pause_label,
                  font=self.font_small,
                  command=self.play_pause,
                  bg=self.bg_color,
                  fg=self.fg_color
                  ).grid(row=rowcount, column=0, columnspan=2, sticky="nsew",
                         padx=5, pady=5)

        # Advance the bar by one
        tk.Button(self,
                  text="⏯",
                  font=self.font_small,
                  command=self.bar_fwd,
                  bg=self.bg_color,
                  fg=self.fg_color
                  ).grid(row=rowcount, column=2,  columnspan=2, sticky="nsew",
                         padx=5, pady=5)
        rowcount += 1

        ttk.Separator(self).grid(row=rowcount, column=0, columnspan=4,
                                 sticky="nsew")
        rowcount += 1

        # OHLC Data of surrent candle
        tk.Label(self,
                 textvariable=self.open_label,
                 bg=self.bg_color,
                 fg=self.fg_color
                 ).grid(row=rowcount, column=0, columnspan=1, sticky="nsew")

        tk.Label(self,
                 textvariable=self.close_label,
                 bg=self.bg_color,
                 fg=self.fg_color
                 ).grid(row=rowcount, column=1, columnspan=1, sticky="nsew")

        tk.Label(self,
                 textvariable=self.high_label,
                 bg=self.bg_color,
                 fg=self.fg_color
                 ).grid(row=rowcount, column=2, columnspan=1, sticky="nsew")

        tk.Label(self,
                 textvariable=self.low_label,
                 bg=self.bg_color,
                 fg=self.fg_color
                 ).grid(row=rowcount, column=3, columnspan=1, sticky="nsew")
        rowcount += 1

        ttk.Separator(self).grid(row=rowcount, column=0, columnspan=4,
                                 sticky="nsew")
        rowcount += 1

        # Limit order and Market Order Tabs
        bstyle = ttk.Style()
        # bstyle.configure('W.TNotebook', background=self.bg_color)
        bstyle.theme_create("darknb", "alt", {
            "TNotebook": {
                "configure": {
                    "background": self.bg_color,
                    "foreground": self.fg_color,
                    "padding": [5, 5]
                }
            },
            "TNotebook.Tab": {
                "configure": {
                    "background": self.bg_color,
                    "foreground": self.fg_color,
                    "font": self.font_esmall,
                    "padding": [6, 6]
                },
                "map": {"background": [("selected", self.fg_color)], 
                        "foreground": [("selected", self.bg_color)]}
            },
            "TSeparator": {
                "configure": {
                    "background": self.fg_color
                }
            }
        })
        
        bstyle.theme_use("darknb")
        orderstab = ttk.Notebook(self)
        self.orderstab = orderstab
        # Market Tab
        markettab = tk.Frame(orderstab,
                             background=self.bg_color)
        # Limit Tab
        limittab = tk.Frame(orderstab,
                            background=self.bg_color)

        orderstab.add(markettab, text="Market")
        orderstab.add(limittab, text="Limit")

        # Add tabs to main GUI
        orderstab.grid(row=rowcount, column=0, columnspan=4, sticky="nsew")
        rowcount += 1

        # Configure Market Tab
        markettab.grid_columnconfigure(1, weight=1)
        tk.Label(markettab,
                 text="MARKET ORDER",
                 font=self.font_esmall,
                 bg=self.bg_color,
                 fg=self.fg_color
                  
                 ).grid(row=0, column=0,  columnspan=4, sticky="nsew",
                        padx=5, pady=5)

        tk.Label(markettab,
                 text="Quantity",
                 bg=self.bg_color,
                 fg=self.fg_color
                 ).grid(row=1, column=0,  columnspan=1, sticky="nsew",
                        padx=5, pady=5)

        self.moquantity = tk.Entry(markettab)
        
        self.moquantity.grid(row=1, column=1,  columnspan=2, 
                             sticky="nsew", padx=5, pady=5)

        tk.Button(markettab,
                  text="MAX",
                  bg=self.bg_color,
                  fg=self.fg_color
                  ).grid(row=1, column=3,  columnspan=1, sticky="nsew",
                         padx=5, pady=5)

        tk.Label(markettab,
                 text="Take Profit",
                 bg=self.bg_color,
                 fg=self.fg_color
                 ).grid(row=2, column=0,  columnspan=1, sticky="nsew",
                        padx=5, pady=5)

        self.motakep = tk.Entry(markettab)
                 
        self.motakep.grid(row=2, column=1,  columnspan=3, 
                          sticky="nsew", padx=5, pady=5)

        tk.Label(markettab,
                 text="Stop Loss",
                 bg=self.bg_color,
                 fg=self.fg_color
                 ).grid(row=3, column=0,  columnspan=1, sticky="nsew",
                        padx=5, pady=5)

        self.mostopl = tk.Entry(markettab)
        self.mostopl.grid(row=3, column=1,  columnspan=3,
                          sticky="nsew", padx=5, pady=5)

        # Configure Limit Tab
        limittab.grid_columnconfigure(1, weight=1)
        tk.Label(limittab,
                 text="LIMIT ORDER",
                 font=self.font_esmall,
                 bg=self.bg_color,
                 fg=self.fg_color
                 ).grid(row=0, column=0,  columnspan=4, sticky="nsew",
                        padx=5, pady=5)

        tk.Label(limittab,
                 text="Order Price",
                 bg=self.bg_color,
                 fg=self.fg_color
                 ).grid(row=1, column=0,  columnspan=1, sticky="nsew",
                        padx=5, pady=5)

        self.loorderp = tk.Entry(limittab)
        self.loorderp.grid(row=1, column=1,  columnspan=3,
                           sticky="nsew", padx=5, pady=5)

        tk.Label(limittab,
                 text="Quantity",
                 bg=self.bg_color,
                 fg=self.fg_color
                 ).grid(row=2, column=0,  columnspan=1, sticky="nsew",
                        padx=5, pady=5)

        self.loquantity = tk.Entry(limittab)
        self.loquantity.grid(row=2, column=1,  columnspan=3,
                             sticky="nsew", padx=5, pady=5)

        tk.Label(limittab,
                 text="Take Profit",
                 bg=self.bg_color,
                 fg=self.fg_color
                 ).grid(row=3, column=0,  columnspan=1, sticky="nsew",
                        padx=5, pady=5)

        self.lotakep = tk.Entry(limittab)
        self.lotakep.grid(row=3, column=1,  columnspan=3,
                          sticky="nsew", padx=5, pady=5)

        tk.Label(limittab,
                 text="Stop Loss",
                 bg=self.bg_color,
                 fg=self.fg_color
                 ).grid(row=4, column=0,  columnspan=1, sticky="nsew",
                        padx=5, pady=5)

        self.lostopl = tk.Entry(limittab)
        self.lostopl.grid(row=4, column=1,  columnspan=3,
                          sticky="nsew", padx=5, pady=5)

        tk.Button(self,
                  text="Place Order",
                  command=self.place_order,
                  bg=self.bg_color,
                  fg=self.fg_color
                  ).grid(row=rowcount, column=0, columnspan=4, sticky="nsew",
                         padx=5, pady=5)
        rowcount += 1

        ttk.Separator(self).grid(row=rowcount, column=0, columnspan=4,
                                 sticky="nsew")
        rowcount += 1

        # Positions

        tk.Label(self, text="Positions", font=self.font_esmall,
                 bg=self.bg_color,
                 fg=self.fg_color
                 ).grid(row=rowcount, column=0, columnspan=4, sticky="nsew")
        rowcount += 1

        tk.Label(self, textvariable=self.position_str,
                 bg=self.bg_color,
                 fg=self.fg_color
                 ).grid(row=rowcount, column=0, columnspan=4, sticky="w")
        rowcount += 1

        ttk.Separator(self).grid(row=rowcount, column=0, columnspan=4,
                                 sticky="nsew")
        rowcount += 1

        tk.Label(self, text="Trade History", font=self.font_esmall,
                 bg=self.bg_color,
                 fg=self.fg_color
                 ).grid(row=rowcount, column=0, columnspan=4, sticky="nsew")
        rowcount += 1

        positions = tk.Listbox(self, height=3, bg=self.bg_color,
                               fg=self.fg_color)
        positions.grid(row=rowcount, column=0, columnspan=4, sticky="nsew")
        positions.insert(tk.END, "..")
    
    def buy_button_cmd(self):
        #self.buy_button.configure(bg = "#4287f5")
        self.order_side = "buy"
        tabindex = self.orderstab.index(self.orderstab.select())
        if tabindex == 0:
            self.order_type = "market"
        elif tabindex == 1:
            self.order_type = "limit"
            
    def place_order(self):
        if self.order_side == "buy":
            print("in buy")
            if self.order_type == "market":
                print("in marekt")
                if self.current_position is None:
                    trd = Trade()
                    trd.market_order(int(self.moquantity.get()), int(self.motakep.get()), int(self.mostopl.get()))
                    self.current_position = Position(trd)

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

            if self.current_position is not None:
                self.current_position.update_ohlc(ohlc)
                self.position_str.set("Long {} @{} Q.{} pnl.{}".format(self.session.get_name(), self.current_position.get_value(), self.current_position.get_quantity(), self.current_position.get_profit()))
            
        if self.playback_running:
            self.after(200, self.routine_task)

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
        self.routine_task()

    


root = tk.Tk()
root.title('Trainer')

app = App(root)
app.configure()
app.mainloop()
