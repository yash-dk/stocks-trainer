from selenium import webdriver
import traceback
import xpath
from tkinter import messagebox

# TODO fix the avg value i think its broken

class Session:
    """This class represents a user session of trading.
    """
    def __init__(self):
        self.init_webdriver()
        self.account_start = 100000
        self.account_value = 100000
        self.percent_profit = 0
        self.pause_signal = False

    def init_webdriver(self):
        try:
            self.driver = webdriver.Chrome()
            self.driver.get("https://www.tradingview.com/#signin")
        except Exception as e:
            print("Error in chromedriver.")
            print(traceback.format_exc())

    def demo(self):
        pass

    def show_error(self, exception, message="Report the issue on github."):
        print(traceback.format_exc())
        messagebox.showerror(str(exception), str(exception)+message)

    def get_ohlc(self):
        
        ohlc = {}
        try:
            elem = self.driver.find_element_by_xpath(xpath.OPEN)
            open_ = elem.text

            elem = self.driver.find_element_by_xpath(xpath.HIGH)
            high = elem.text

            elem = self.driver.find_element_by_xpath(xpath.LOW)
            low = elem.text

            elem = self.driver.find_element_by_xpath(xpath.CLOSE)
            close = elem.text
        except Exception as e:
            self.show_error(e)
            return None

        try:
            open_ = float(open_)
            high = float(high)
            low = float(low)
            close = float(close)
        except Exception as e:
            self.show_error(e)
            return None

        ohlc["open"] = open_
        ohlc["high"] = high
        ohlc["low"] = low
        ohlc["close"] = close

        return ohlc

    def get_name(self):
        try:
            name = self.driver.find_element_by_xpath(xpath.STOCK_NAME)
            return name.text
        except Exception as e:
            self.show_error(e)
            return None

    def get_fname(self):
        try:
            fname = self.driver.find_element_by_xpath(xpath.STOCK_FULL_NAME)
            return fname.text
        except Exception as e:
            self.show_error(e)
            return None

    def click_replay(self):
        try:
            fname = self.driver.find_element_by_xpath(xpath.REPLAY_BUTTON)
            fname.click()
            return True
        except Exception as e:
            self.show_error(e)
            return False

    def click_pause_play(self):
        try:
            self.driver.execute_script(xpath.PLAY_PAUSE_SCRIPT)
            return True
        except Exception as e:
            self.show_error(e)
            return False

    def check_last_bar(self):
        try:

            x = self.driver.execute_script(xpath.LAST_BAR_CHECK)
            
            return x
        except Exception as e:
            self.show_error(e)
            return None

    def click_fwd_bar(self):
        try:
            self.driver.execute_script(xpath.FWD_BAR_SCRIPT)
            return True
        except Exception as e:
            self.show_error(e)
            return False

    def __del__(self):
        self.driver.close()

class Trade:
    """This class represents a trade taken by user.
    """
    status = True

    def __init__(self, ohlc=None, is_sell=False):
        self.ohlc = ohlc
        self.is_sell = is_sell
        self.taken_price = None

    def market_order(self, quantity, take_profit=None, stop_loss=None):
        self.mo = True
        self.lo = False
        if self.is_sell:
            self.quantity = -quantity
        else:
            self.quantity = quantity
        self.take_profit = take_profit
        self.stop_loss = stop_loss

    def limit_order(self, quantity, limit, take_profit=None, stop_loss=None):
        self.mo = False
        self.lo = True
        self.limit = limit
        if self.is_sell:
            self.quantity = -quantity
        else:
            self.quantity = quantity
        self.take_profit = take_profit
        self.stop_loss = stop_loss

    def execute(self):
        if self.ohlc is not None:
            if self.mo:
                self.taken_price = self.ohlc["close"]
                return self.quantity, self.ohlc["close"]
            elif self.lo:
                if (self.limit <= self.ohlc["high"]
                        and self.limit >= self.ohlc["low"]):
                    return self.quantity, self.limit
        return None, None

    def link_ohlc(self, ohlc):
        self.ohlc = ohlc

    def __str__(self):
        retst = ""
        if self.is_sell:
            retst += "Short @ "
        else:
            retst += "Long @ "

        if self.mo:
            retst += str(self.taken_price) + "[MO]"
        else:
            retst += str(self.limit) + "[LO]"

        retst += " Q."+str(abs(self.quantity))
        
        return retst

class Position:
    """This class represents a position taken by user.
    """

    def __init__(self, trade, session = None):
        self.pending_trades = [trade]
        self.done_trades = []
        self.ohlc = {
            "open": 0,
            "high": 0,
            "low": 0,
            "close": 0
        }

        self.pending_trades[0].link_ohlc(self.ohlc)
        self.is_short = trade.is_sell
        self.stop_loss = None
        self.take_profit = None

        self.status = True
        self.shares = []
        self.booked = []
        self.session = session

    def add_trade(self, trade):
        if isinstance(trade, Trade):
            trade.link_ohlc(self.ohlc)
            self.pending_trades.append(trade)

    def add_quantity(self, quantity, price):
        try:
            res = self.quantity + quantity

            if not self.is_short:
                if res == 0:
                    # squareoff
                    buy_cap = self.avg_price * self.quantity
                    sell_cap = price * self.quantity

                    self.booked.append([buy_cap, sell_cap])
                    self.shares = []
                    if self.session is not None:
                        self.session.percent_profit += (self.get_profit() / self.invested_amount) * 100
                    
                    self.status = False
                    pass
                elif res < 0:
                    # squareoff
                    buy_cap = self.avg_price * self.quantity
                    sell_cap = price * self.quantity

                    self.booked.append([buy_cap, sell_cap])
                    self.shares = []
                    if self.session is not None:
                        self.session.percent_profit += (self.get_profit() / self.invested_amount) * 100
                    
                    self.status = False
                    messagebox.showerror("Oversold", "You sold more quantity then you bought.")
                    pass
                else:

                    if quantity < 0:

                        bquant = quantity
                        net_price_sold = 0

                        pops = []
                        for i in range(len(self.shares)):

                            res = self.shares[i][1] + quantity

                            if res < 0:
                                quantity = res
                                net_price_sold += self.shares[i][0] * self.shares[i][1]
                                pops.append(self.shares[i])

                            elif res == 0:
                                quantity = res
                                pops.append(self.shares[i])
                                net_price_sold += self.shares[i][0] * self.shares[i][1]
                            else:
                                self.shares[i][1] = res
                                net_price_sold += self.shares[i][0] * abs(quantity)
                                quantity = 0

                        curr_value_sold = price * abs(bquant)

                        self.booked.append([net_price_sold, curr_value_sold])
                        for i in pops:
                            self.shares.remove(i)

                        self.quantity
                        self.avg_price
                        return
                    self.shares.append([price, quantity])
                    self.quantity
                    self.avg_price
                    buy_cap = self.avg_price * self.quantity
                    sell_cap = price * self.quantity

                    pass
            else:
                if res == 0:
                    # squareoff
                    buy_cap = self.avg_price * abs(self.quantity)
                    sell_cap = price * abs(self.quantity)
                    self.booked.append([buy_cap, sell_cap])
                    self.shares = []
                    if self.session is not None:
                        self.session.percent_profit += (self.get_profit() / self.invested_amount) * 100
                    self.status = False
                    pass
                elif res > 0:
                    # squareoff
                    buy_cap = self.avg_price * abs(self.quantity)
                    sell_cap = price * abs(self.quantity)
                    self.booked.append([buy_cap, sell_cap])
                    self.shares = []
                    if self.session is not None:
                        self.session.percent_profit += (self.get_profit() / self.invested_amount) * 100
                    
                    self.status = False
                    messagebox.showerror("Overbought", "You bought more quantity then you sold.")
                    pass
                else:
                    if quantity > 0:

                        bquant = quantity
                        net_price_sold = 0

                        pops = []

                        for i in range(len(self.shares)):

                            res = self.shares[i][1] + quantity

                            if res > 0:
                                quantity = res
                                net_price_sold += self.shares[i][0] * abs(self.shares[i][1])
                                pops.append(self.shares[i])

                            elif res == 0:
                                quantity = res
                                pops.append(self.shares[i])
                                net_price_sold += self.shares[i][0] * abs(self.shares[i][1])

                            else:

                                self.shares[i][1] = res
                                net_price_sold += self.shares[i][0] * abs(quantity)
                                quantity = 0

                        curr_value_sold = price * abs(bquant)

                        self.booked.append([net_price_sold, curr_value_sold])
                        for i in pops:

                            self.shares.remove(i)

                        self.quantity
                        self.avg_price
                        return

                    self.shares.append([price, quantity])
                    self.quantity
                    self.avg_price

                    pass

        except Exception as e:
            print("excp", e)
            print(traceback.format_exc())
            pass

    def get_value(self):
        return abs(self.avg_price)

    def get_profit(self):
        if self.is_short:
            return -(self.profit)
        else:
            return self.profit

    def get_quantity(self):
        return abs(self.quantity)

    @property
    def quantity(self):
        qnt = 0
        for i in self.shares:
            qnt += i[1]

        return qnt

    @property
    def profit(self):
        buy_price = 0
        sell_price = 0
        for i in self.booked:
            buy_price += i[0]
            sell_price += i[1]

        bookedp = sell_price - buy_price

        buy_price = 0
        for i in self.shares:
            buy_price += i[0] * abs(i[1])

        sell_price = abs(self.quantity) * self.ohlc["close"]
        
        notbookedp = sell_price - buy_price

        return notbookedp+bookedp

    @property
    def invested_amount(self):
        buy_price = 0
        for i in self.booked:
            buy_price += i[0]

        buy_price1 = 0
        for i in self.shares:
            buy_price1 += i[0] * abs(i[1])

        return buy_price + buy_price1

    @property
    def avg_price(self):
        avg = 0
        total_price = 0
        total_quantity = self.quantity
        for i in self.shares:
            total_price += (i[0] * i[1])
        try:
            avg = total_price/total_quantity
        except ZeroDivisionError:
            pass

        return avg

    def check_sl_tk(self):
        if self.stop_loss is not None:
            if self.stop_loss <= self.ohlc["high"] and self.stop_loss >= self.ohlc["low"]:
                buy_cap = self.avg_price * abs(self.quantity)
                sell_cap = self.stop_loss * abs(self.quantity)
                self.booked.append([buy_cap, sell_cap])
                self.shares = []
                if self.session is not None:
                        self.session.percent_profit += (self.get_profit() / self.invested_amount) * 100
                        self.session.click_pause_play()
                        self.session.pause_signal = True
                
                self.status = False
                messagebox.showinfo("Stop Loss","Stop loss hit.")
                print("sl hit")

        if self.take_profit is not None:
            if self.take_profit <= self.ohlc["high"] and self.take_profit >= self.ohlc["low"]:
                buy_cap = self.avg_price * abs(self.quantity)
                sell_cap = self.take_profit * abs(self.quantity)
                self.booked.append([buy_cap, sell_cap])
                self.shares = []
                if self.session is not None:
                        self.session.percent_profit += (self.get_profit() / self.invested_amount) * 100
                        self.session.click_pause_play()
                        self.session.pause_signal = True
                
                self.status = False
                messagebox.showinfo("Profit","Profit booked at take profit.")
                print("profit")

    def execute_trades(self):
        for i in self.pending_trades:
            quantity, price = i.execute()
            if quantity is not None:
                self.stop_loss = i.stop_loss
                self.take_profit = i.take_profit
                self.pending_trades.remove(i)
                self.done_trades.append(i)
                self.add_quantity(quantity, price)

    def update_ohlc(self, ohlc):
        if not self.status:
            return
        self.ohlc["open"] = ohlc["open"]
        self.ohlc["high"] = ohlc["high"]
        self.ohlc["low"] = ohlc["low"]
        self.ohlc["close"] = ohlc["close"]
        self.check_sl_tk()
        self.execute_trades()
        self.profit


if __name__ == "__main__":
    pass

