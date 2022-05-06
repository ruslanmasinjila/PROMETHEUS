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

numCandles     = 50
offset = 1

RainbowSignals =[]
RainbowSignalsTF =[]
##########################################################################################


# In[ ]:


def getSignals(rates_frame,strTimeframe):
    
    fractalCandle = -3
    
    Time, Open, Close, High, Low = getTOCHL(rates_frame)
    
    ######################################################################################
    
    SMA50 = np.mean(Close)
    SMA45 = np.mean(Close[5:])
    SMA40 = np.mean(Close[10:])
    SMA35 = np.mean(Close[15:])
    SMA30 = np.mean(Close[20:])
    SMA25 = np.mean(Close[25:])
    SMA20 = np.mean(Close[30:])
    
    if(SMA45<SMA50 and SMA40<SMA45 and SMA35<SMA40 and SMA30<SMA35 and SMA25<SMA30 and SMA20<SMA25):
        if(strTimeframe=="M1"):
            if(High[fractalCandle]<SMA50):
                if(High[fractalCandle]>High[fractalCandle+1] and
                   High[fractalCandle]>High[fractalCandle+2] and
                   High[fractalCandle]>High[fractalCandle-2] and
                   High[fractalCandle]>High[fractalCandle-1]):
                    RainbowSignals.append("SELL")
                    RainbowSignalsTF.append(strTimeframe)
        else:
            RainbowSignals.append("SELL")
            RainbowSignalsTF.append(strTimeframe)
                
        
    if(SMA45>SMA50 and SMA40>SMA45 and SMA35>SMA40 and SMA30>SMA35 and SMA25>SMA30 and SMA20>SMA25):
        if(strTimeframe=="M1"):
            if(Low[fractalCandle]>SMA50):
                if(Low[fractalCandle]<Low[fractalCandle+1] and
                   Low[fractalCandle]<Low[fractalCandle+2] and
                   Low[fractalCandle]<Low[fractalCandle-2] and
                   Low[fractalCandle]<Low[fractalCandle-1]):
                    RainbowSignals.append("BUY")
                    RainbowSignalsTF.append(strTimeframe)
        else:
            RainbowSignals.append("BUY")
            RainbowSignalsTF.append(strTimeframe)
                


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
def getTOCHL(rates_frame):
    return  (list(rates_frame["time"]), 
            list(rates_frame["open"]), 
            list(rates_frame["close"]),
            list(rates_frame["high"]),
            list(rates_frame["low"]))

##########################################################################################


# In[ ]:


banner = ""
banner+="##############################\n"
banner+="           SIGNALS            \n"
banner+="##############################\n"
while(True):
    
    display = banner
    for cp in currency_pairs:
        display+="["+cp+"]"+"\n"
        RainbowSignals =[]
        RainbowSignalsTF =[]
        for t in range(len(mt5Timeframe)):
            rates_frame = getRates(cp, mt5Timeframe[t], numCandles)
            getSignals(rates_frame,strTimeframe[t])
        if(all(x == RainbowSignals[0] for x in RainbowSignals)):
            if(RainbowSignalsTF[0]=="M1"):
                display+=" ".join(RainbowSignals)+"\n"
                display+=" ".join(RainbowSignalsTF)+"\n"
                winsound.Beep(freq, duration)
                    
        display+="==============================\n"
    print(display)
    time.sleep(60)
    os.system('cls' if os.name == 'nt' else 'clear')

