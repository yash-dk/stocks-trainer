from selenium import webdriver
import traceback
import xpath
from tkinter import messagebox



class Session:
    """This class represents a user session of trading.
    """
    def __init__(self):
        self.init_webdriver()

    def init_webdriver(self):
        try:
            self.driver = webdriver.Chrome()
            self.driver.get("https://www.tradingview.com/#signin")
        except Exception as e:
            print("Error in chromedriver.")
            print(traceback.format_exc(e))

    def demo(self):
        pass

    def show_error(self, exception, message="Report the issue on github."):
        print(traceback.format_exc(exception))
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

    def click_fwd_bar(self):
        try:
            self.driver.execute_script(xpath.FWD_BAR_SCRIPT)
            return True
        except Exception as e:
            self.show_error(e)
            return False

class Trade:
    """This class represents a trade taken by user.
    """
    status = True
    def __init__(self, ohlc=None):
        self.ohlc = ohlc

    def market_order(self, quantity, take_profit=None, stop_loss=None):
        self.mo = True
        self.lo = False
        self.quantity = quantity
        self.take_profit = take_profit
        self.stop_loss = stop_loss

    def limit_order(self, quantity, limit, take_profit=None, stop_loss=None):
        self.mo = False
        self.lo = True
        self.limit = limit
        self.quantity = quantity
        self.take_profit = take_profit
        self.stop_loss = stop_loss

    def execute(self):
        if self.ohlc is not None:
            if self.mo:
                return self.quantity, self.ohlc["close"]
            elif self.lo:
                if self.limit <= self.ohlc["high"] and self.limit >= self.ohlc["low"]:
                    return self.quantity, self.limit
        return None, None

    def link_ohlc(self,ohlc):
        self.ohlc = ohlc


class Position:
    """This class represents a position taken by user.
    """
    
    def __init__(self, trade):
        self.pending_trades = [trade]
        self.done_trades = []
        self.ohlc = {
            "open":0,
            "high":0,
            "low":0,
            "close":0
        }

        self.pending_trades[0].link_ohlc(self.ohlc)
        self.stop_loss = None
        self.take_profit = None
        self.quantity = 0
        self.price = 0

    def add_trade(self, trade):
        if isinstance(trade, Trade):
            self.pending_trades.append(trade)

    def add_quantity(self, quantity, price):
        try:
            current_total = self.quantity * self.price
            self.quantity += quantity
            now_total = price * quantity
            current_total += now_total
            self.price = current_total/self.quantity
        except:
            pass
        
    def check_sl_tk(self):
        if self.stop_loss is not None:
            if self.stop_loss <= self.ohlc["high"] and self.stop_loss >= self.ohlc["low"]:
                messagebox.showinfo("Stop Loss","Stop loss hit.")

        if self.take_profit is not None:
            if self.take_profit <= self.ohlc["high"] and self.take_profit >= self.ohlc["low"]:
                messagebox.showinfo("Profit","Profit booked at take profit.")

    def execute_trades(self):
        for i in self.pending_trades:
            quantity, price = i.execute()
            if quantity is not None:
                self.add_quantity(quantity, price)
                self.stop_loss = i.stop_loss
                self.take_profit = i.take_profit
                self.pending_trades.remove(i)
                self.done_trades.append(i)

    def update_ohlc(self,ohlc):
        self.ohlc["open"] = ohlc["open"]
        self.ohlc["high"] = ohlc["high"]
        self.ohlc["low"] = ohlc["low"]
        self.ohlc["close"] = ohlc["close"]
        

if __name__ == "__main__":
    Session()
    input()
