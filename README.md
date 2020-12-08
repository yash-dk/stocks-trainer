# Stocks Trainer
This is a trainer written in python using tkinter for GUI and selenium for controlling tradingview. It allows the user to practice trading in the replay feature provided in tradingview.com

# Running the trainer
Download the repo and install the requirements using `pip install -r requirements.txt` then execute the `app.py` using `python app.py`.

# How to use the trainer
Step 1: Start the trainer as specified above. Then login in tradingview and open chart from the navbar. `Note: The chart must be open in the same tab where the login screen was opened.`

Step 2: Open the Symbol that you want to trade.

Step 3: Click on Fetch this will get the symbol name.

Step 4: Then click on `◀◀` to bring the replay box then select from where to play the replay.

Step 5: Select the Buy or Sell button for what you wan to do.

Step 6: Then You can place the order in either Market Tab or Limit Tab.

		Step 6.1: If you choose to place market order consider following points.

			a) Quantity is necessary while Take Profit and Stop Loss is optional.
			b) The Order will be sold when either the take profit is hit or the stop loss is hit.
			c)If you want to sell it before either are hit or you have not specified any. just place the sell order of the desired quantity.
			
		Step 6.2: If you choose to place limit order consider following points.

			a) Quantity and Order price is necessary while Take Profit and Stop Loss is optional.
			b) The order will be executed with the order price is hit.
			c) The Order will be sold when either the take profit is hit or the stop loss is hit.
			d)If you want to sell it before either are hit or you have not specified any. just place the sell order of the desired quantity.

Step 7: Place the order by clicking `Place Order`

Step 8: Click on play `▶` button to start the playback or click `⏯` to advance only 1 bar at a time.

Step 9:  Click on play `▶` button to stop the playback, if you clicked it to start the playback first.

`NOTE: Do not hover the cursor over the chart while the replay is on as this might trigger your stoploss or take profit. Pause the replay from the trainer before hovering the cursor over the chart.`

Step 10: Enjoy! Open an issue is one arises. [This is still in Beta]

# Features
In addition to the above specified, 
1. You Can Average the position by buying more shares, you can sell any amount of quantity from what you bought.
	1.1. Example if you have 100 shares you can buy more 100, for a total of 200 shares then sell 50 shares if you want. 
2. There is the OHLC indicater above the orders tabs
3. Current position its ongoing unrealized Profit and loss the % return you have earned in this position.
4. Trade history conatins All trades you took in this position specifying which are pending and which are done.
5. The Account Value is `Work in progress`.

# Side Note
The trainer is still in beta so do let me know what you have any suggestions by opening the issue. And also report a issue if it appears.