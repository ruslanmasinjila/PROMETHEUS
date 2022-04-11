#!/usr/bin/env python
# coding: utf-8

# In[ ]:


##########################################################################################
# PROJECT PROMETHEUS
# AUTHOR: RUSLAN MASINJILA
##########################################################################################
import MetaTrader5 as mt5
import pandas as pd
import numpy as np
import time
import os

import winsound
duration = 100
freq     = 1000

# NUMBER OF COLUMNS TO BE DISPLAYED
pd.set_option('display.max_columns', 500)

# MAXIMUM TABLE WIDTH TO DISPLAY
pd.set_option('display.width', 1500)      
 
# ESTABLISH CONNECTION TO MT5 TERMINAL
if not mt5.initialize():
    print("initialize() FAILED, ERROR CODE =",mt5.last_error())
    quit()


# In[ ]:


# MT5 TIMEFRAME
MN1  = mt5.TIMEFRAME_MN1
W1  = mt5.TIMEFRAME_W1
D1  = mt5.TIMEFRAME_D1
H12 = mt5.TIMEFRAME_H12
H8  = mt5.TIMEFRAME_H8
H6  = mt5.TIMEFRAME_H6
H4  = mt5.TIMEFRAME_H4
H3  = mt5.TIMEFRAME_H3
H2  = mt5.TIMEFRAME_H2
H1  = mt5.TIMEFRAME_H1
M30 = mt5.TIMEFRAME_M30
M20 = mt5.TIMEFRAME_M20
M15 = mt5.TIMEFRAME_M15
M12 = mt5.TIMEFRAME_M12
M10 = mt5.TIMEFRAME_M10
M6  = mt5.TIMEFRAME_M6
M5  = mt5.TIMEFRAME_M5
M4  = mt5.TIMEFRAME_M4
M3  = mt5.TIMEFRAME_M3
M2  = mt5.TIMEFRAME_M2
M1  = mt5.TIMEFRAME_M1

currency_pairs = None
with open('instruments.txt') as f:
    currency_pairs = [line.rstrip('\n') for line in f]


# TIMEFRAMES
mt5Timeframe   = [M1,M2,M3,M4,M5,M6,M10,M12,M15,M20,M30,H1,H2,H3,H4,H6,H8,H12,D1]
strTimeframe   = ["M1","M2","M3","M4","M5","M6","M10","M12","M15","M20","M30","H1","H2","H3","H4","H6","H8","H12","D1"]

numCandles     = 2
offset = 1

DeMarkSignals = []
DeMarkSignalsTF = []

##########################################################################################


# In[ ]:


def getSignal(rates_frame):
    
    leftCandle    = -2
    rightCandle   = -1
    signal        = []
    
    Time, Open, Close, High, Low, Volume = getTOCHLV(rates_frame)
    
    Difference = High[leftCandle] - Low[leftCandle]
    upperBound = High[leftCandle] - 0.3*Difference
    lowerBound = Low[leftCandle]  + 0.3*Difference               
    ######################################################################################
    # Supper SELL
    if(Close[leftCandle]<Open[leftCandle] and Close[rightCandle]<Open[rightCandle]):
        if(Open[rightCandle]>Open[leftCandle] and Close[rightCandle]<Close[leftCandle]):
            signal.append("SELL SUPER")
            return signal
        
    # Bearigh Engulfing on an inverted Hammer or Shooting Star
    if(Open[leftCandle]<lowerBound and Close[leftCandle]<lowerBound):
        if(Open[rightCandle]>=Open[leftCandle] and Open[rightCandle]>=Close[leftCandle]):
            if(Close[rightCandle]<Open[leftCandle] and Close[rightCandle]<Close[leftCandle]):
                if(Low[leftCandle]==Close[leftCandle]):
                    signal.append("SELL ENGULFING SUPER")
                else:
                    signal.append("SELL ENGULFING")
                return signal
    ######################################################################################
    # Super BUY
    if(Close[leftCandle]>Open[leftCandle] and Close[rightCandle]>Open[rightCandle]):
        if(Open[rightCandle]<Open[leftCandle] and Close[rightCandle]>Close[leftCandle]):
            signal.append("BUY SUPER")
            return signal
        
    # Bullish Engulfing on an Hammer or Hanging man
    if(Open[leftCandle]>upperBound and Close[leftCandle]>upperBound):
        if(Open[rightCandle]<=Open[leftCandle] and Open[rightCandle]<=Close[leftCandle]):
            if(Close[rightCandle]>Open[leftCandle] and Close[rightCandle]>Close[leftCandle]):
                if(High[leftCandle]==Close[leftCandle]):
                    signal.append("BUY ENGULFING SUPER")
                 
                else:
                    signal.append("BUY ENGULFING")
                return signal
    ######################################################################################

    return signal


# In[ ]:


# Gets the most recent <numCandles> prices for a specified <currency_pair> and <mt5Timeframe>
# Excludes the bar that has not finished forming <i.e offset = 1>
def getRates(currency_pair, mt5Timeframe, numCandles):
    rates_frame =  mt5.copy_rates_from_pos(currency_pair, mt5Timeframe, offset, numCandles)
    rates_frame = pd.DataFrame(rates_frame)
    return rates_frame

##########################################################################################


# In[ ]:


# Decomposes the DataFrame into individual lists for Time, Close, High and Low
def getTOCHLV(rates_frame):
    return  (list(rates_frame["time"]), 
            list(rates_frame["open"]), 
            list(rates_frame["close"]),
            list(rates_frame["high"]),
            list(rates_frame["low"]),
            list(rates_frame["tick_volume"]))

##########################################################################################


# In[ ]:


banner = ""
banner+="##############################\n"
banner+="           SIGNALS            \n"
banner+="##############################\n"
while(True):
    
    display = banner
    for cp in currency_pairs:
        display+=cp+"\n"
        for t in range(len(mt5Timeframe)):
            
            rates_frame = getRates(cp, mt5Timeframe[t], numCandles)
            signal=getSignal(rates_frame)
            if(len(signal)>0):
                winsound.Beep(freq, duration)
                display+=signal[0] + " ********************************* " + strTimeframe[t]+"\n"
                
        display+="==============================\n"
    print(display)
    time.sleep(60)
    os.system('cls' if os.name == 'nt' else 'clear')
print("DONE")

