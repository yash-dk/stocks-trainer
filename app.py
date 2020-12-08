import tkinter as tk
from tkinter import ttk
import tkinter.font as tkFont
from session import Session, Position, Trade


class App(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.master.configure(background="#121212")
        self.session = Session()
        self.pack()
        self.fonts()
        self.tvars()
        self.bg_color = "#121212"
        self.fg_color = "#ffffff"
        self.down_color = "#ef5350"
        self.up_color = "#26a69a"
        self.active_color = "#444444"
        
        self.configure(bg=self.bg_color)
        self.construct_widget()
        
        self.playback_running = False
        self.current_position = None
        self.order_type = None
        self.order_side = None
        self.done_positions = []
        
        
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
        self.acc_val_lab = tk.StringVar()
        self.acc_val_lab.set("Account Value: {} +0.0%".format(self.session.account_value))
        
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
                                     fg=self.fg_color,
                                     command=self.sell_button_cmd
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

        # Acc value
        tk.Label(self, textvariable=self.acc_val_lab, font=self.font_esmall,
                 bg=self.bg_color,
                 fg=self.fg_color,
                 ).grid(row=rowcount, column=0, columnspan=4, sticky="nw")
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

        self.positions_lb = tk.Listbox(self, height=3, bg=self.bg_color,
                                       fg=self.fg_color)
        self.positions_lb.grid(row=rowcount, column=0, columnspan=4, sticky="nsew")
        #self.positions_lb.insert(tk.END, "..")
    
    def buy_button_cmd(self):
        self.buy_button.configure(bg = self.up_color)
        self.sell_button.configure(bg = self.bg_color)
        self.order_side = "buy"
        tabindex = self.orderstab.index(self.orderstab.select())
        if tabindex == 0:
            self.order_type = "market"
        elif tabindex == 1:
            self.order_type = "limit"

    def sell_button_cmd(self):
        self.buy_button.configure(bg = self.bg_color)
        self.sell_button.configure(bg = self.down_color)
        self.order_side = "sell"
        tabindex = self.orderstab.index(self.orderstab.select())
        if tabindex == 0:
            self.order_type = "market"
        elif tabindex == 1:
            self.order_type = "limit"
            
    def place_order(self):
        self.clear_position()
        tabindex = self.orderstab.index(self.orderstab.select())
        if tabindex == 0:
            self.order_type = "market"
        elif tabindex == 1:
            self.order_type = "limit"

        if self.order_type == "market":
            print("in market")
            
            if self.order_side == "buy":
                trd = Trade()
            elif self.order_side == "sell":
                trd = Trade(is_sell=Trade)
            else:
                return
            try:
                quantitiy = int(self.moquantity.get())

                if self.motakep.get().strip():
                    takep = int(self.motakep.get())
                else:
                    takep = None
    
                if self.mostopl.get().strip():
                    stopl = int(self.mostopl.get())
                else:
                    stopl = None
            except:
                tk.messagebox.showerror("Value Error", "All the inputs must be Integers.")
                return

            trd.market_order(quantitiy, takep, stopl)
            if self.current_position is None:
                self.current_position = Position(trd, self.session)
            else:
                self.current_position.add_trade(trd)
        else:
            print("inlimit")
            
            if self.order_side == "buy":
                trd = Trade()
            elif self.order_side == "sell":
                trd = Trade(is_sell=Trade)
            else:
                return

            try:
                quantitiy = int(self.loquantity.get())
    
                if self.lotakep.get().strip():
                    takep = int(self.lotakep.get())
                else:
                    takep = None
                if self.lostopl.get().strip():
                    stopl = int(self.lostopl.get())
                else:
                    stopl = None

                limit = int(self.loorderp.get())
            except:
                tk.messagebox.showerror("Value Error", "All the inputs must be Integers.")
                return
            
            trd.limit_order(quantitiy, limit, takep, stopl)
            if self.current_position is None:
                self.current_position = Position(trd, self.session)
            else:
                self.current_position.add_trade(trd)

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
            try:
                perc = self.session.account_value / self.session.account_start
                perc -= 1
                if perc >= 0:
                    perc = round(perc*100, 3)
                    self.acc_val_lab.set("Account value: {} +{}".format(self.session.account_value, perc))
                else:
                    self.acc_val_lab.set("Account value: {} -{}".format(self.session.account_value, perc))
            except:
                self.acc_val_lab.set("Error")

            if self.current_position is not None:
                self.update_trades()
                self.current_position.update_ohlc(ohlc)
                if self.current_position.is_short:
                    typee = "Short"
                else:
                    typee = "Long"
                percent = round((self.current_position.get_profit() / self.current_position.invested_amount) * 100, 2)
                self.position_str.set("{} {} @{} Q.{}\nInv.{} PnL.{} {}%".format(typee, self.session.get_name(), self.current_position.get_value(), self.current_position.get_quantity(), self.current_position.invested_amount , round(self.current_position.get_profit(), 2), percent))
            
        if self.session.check_last_bar():
            self.session.click_pause_play()
            self.playback_running = False
        if self.playback_running:
            self.after(200, self.routine_task)

    def update_trades(self):
        if self.current_position is not None:
            self.positions_lb.delete(0, tk.END)
            self.positions_lb.insert(tk.END, "Pending")
            for i in self.current_position.pending_trades:
                self.positions_lb.insert(tk.END, str(i))
            self.positions_lb.insert(tk.END, "Done")
            for i in self.current_position.done_trades:
                self.positions_lb.insert(tk.END, str(i))
            
    def clear_position(self):
        if self.current_position is not None:
            if not self.current_position.status:
                self.done_positions.append(self.current_position)
                self.current_position = None
                self.position_str.set("No Position")

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


if __name__ == "__main__":
    
    root = tk.Tk()
    root.title('Trainer')
    root.attributes('-topmost', True)
    app = App(root)
    app.configure()
    app.mainloop()
