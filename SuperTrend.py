import pandas as pd
import numpy as np

# Supertrend Indıcator
def Supertrend(df, atr_period = 10, multiplier = 3):
    
    high = df['high']
    low = df['low']
    close = df['open']
    
    price_diffs = [high - low, 
                   high - close.shift(), 
                   close.shift() - low]
    true_range = pd.concat(price_diffs, axis=1)
    true_range = true_range.abs().max(axis=1)

    atr = true_range.ewm(alpha=1/atr_period,min_periods=atr_period).mean() 

    hl2 = (high + low) / 2
    
    final_upperband = upperband = hl2 + (multiplier * atr)
    final_lowerband = lowerband = hl2 - (multiplier * atr)
    
    supertrend = [True] * len(df)
    
    for i in range(1, len(df.index)):
        curr, prev = i, i-1

        if close[curr] > final_upperband[prev]:
            supertrend[curr] = True

        elif close[curr] < final_lowerband[prev]:
            supertrend[curr] = False

        else:
            supertrend[curr] = supertrend[prev]
            
            if supertrend[curr] == True and final_lowerband[curr] < final_lowerband[prev]:
                final_lowerband[curr] = final_lowerband[prev]
            if supertrend[curr] == False and final_upperband[curr] > final_upperband[prev]:
                final_upperband[curr] = final_upperband[prev]

        if supertrend[curr] == True:
            final_upperband[curr] = np.nan
        else:
            final_lowerband[curr] = np.nan      
    
    return pd.DataFrame({
        'Supertrend': supertrend,
        'Final Lowerband': final_lowerband,
        'Final Upperband': final_upperband,
        'trend': np.where(supertrend, 1, -1)
        }, index=df.index)

def supertrend_signals(df):
    buy_signal = df['Supertrend'].iloc[-1] == True and df['Supertrend'].iloc[-2] == False
    sell_signal = df['Supertrend'].iloc[-1] == False and df['Supertrend'].iloc[-2] == True
    return buy_signal, sell_signal