from selenium import webdriver
import traceback
import xpath
import time
from tkinter import messagebox

class Session:
    """This class represents a user session of trading.
    """
    def __init__(self):
        self.init_webdriver()
        input()
        self.demo()

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
        messagebox.showerror(str(exception),str(exception)+message)
    
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
            
if __name__ == "__main__":
    Session()
    input()