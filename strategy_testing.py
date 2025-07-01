import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Stock-specific parameters
STOCK_PARAMS = {
    "EICHERMOT.NS": {
        "ma_period": 20,
        "rsi_period": 10,
        "rsi_threshold": 45,
        "macd_fast": 8,
        "macd_slow": 24,
        "macd_signal": 7,
        "max_hold_candles": 60
    },
    "VBL.NS": {
        "ma_period": 25,
        "rsi_period": 14,
        "rsi_threshold": 55,
        "macd_fast": 12,
        "macd_slow": 26,
        "macd_signal": 9,
        "max_hold_candles": 80
    },
    "TRENT.NS": {
        "ma_period": 18,
        "rsi_period": 8,
        "rsi_threshold": 42,
        "macd_fast": 10,
        "macd_slow": 24,
        "macd_signal": 8,
        "max_hold_candles": 96
    },
    "TCS.NS": {
        "ma_period": 24,
        "rsi_period": 8,
        "rsi_threshold": 45,
        "macd_fast": 9,
        "macd_slow": 24,
        "macd_signal": 12,
        "max_hold_candles": 60
    },
    "DIVISLAB.NS": {
        "ma_period": 22,
        "rsi_period": 16,
        "rsi_threshold": 50,
        "macd_fast": 11,
        "macd_slow": 25,
        "macd_signal": 8,
        "max_hold_candles": 88
    },
    "SBIN.NS": {
        "ma_period": 16,
        "rsi_period": 8,
        "rsi_threshold": 55,
        "macd_fast": 9,
        "macd_slow": 26,
        "macd_signal": 12,
        "max_hold_candles": 96
    },
    "BAJFINANCE.NS": {
        "ma_period": 16,
        "rsi_period": 16,
        "rsi_threshold": 50,
        "macd_fast": 9,
        "macd_slow": 24,
        "macd_signal": 12,
        "max_hold_candles": 60
    },
    "FIRSTCRY.NS": {
        "ma_period": 16,
        "rsi_period": 12,
        "rsi_threshold": 47,
        "macd_fast": 9,
        "macd_slow": 22,
        "macd_signal": 7,
        "max_hold_candles": 60
    }
}

# Settings
assets = [
    "EICHERMOT.NS", "VBL.NS", "TRENT.NS", "TCS.NS", "DIVISLAB.NS",
    "FIRSTCRY.NS", "SBIN.NS", "BAJFINANCE.NS"
]
interval = "15m"
end_date = datetime.now()
start_date = end_date - timedelta(days=10)

def run_strategy(symbol):
    print(f"\nFetching data for: {symbol}")
    df = yf.download(symbol, interval=interval, start=start_date, end=end_date, progress=False, auto_adjust=True)
    
    if df.empty or len(df) < 100:
        print(f"{symbol}: Not enough data.\n")
        return
    
    df.dropna(inplace=True)
    
    # Get stock-specific parameters
    params = STOCK_PARAMS.get(symbol, {
        "ma_period": 20, "rsi_period": 14, "rsi_threshold": 50,
        "macd_fast": 12, "macd_slow": 26, "macd_signal": 9, "max_hold_candles": 96
    })
    
    # Indicators with stock-specific parameters
    df['ma20'] = df['Close'].rolling(params['ma_period']).mean()
    df['rsi'] = compute_rsi(df['Close'], params['rsi_period'])
    df['ema12'] = df['Close'].ewm(span=params['macd_fast'], adjust=False).mean()
    df['ema26'] = df['Close'].ewm(span=params['macd_slow'], adjust=False).mean()
    df['macd'] = df['ema12'] - df['ema26']
    df['macd_signal'] = df['macd'].ewm(span=params['macd_signal'], adjust=False).mean()
    
    df['signal'] = 0
    trades = []
    position = False
    entry_price = 0
    entry_index = 0
    
    # Start from index 26 to ensure all indicators have valid values
    for i in range(26, len(df)):
        if not position:
            # Extract scalar values using .values[0] to avoid Series comparison issues
            try:
                close_val = df['Close'].iloc[i].item() if hasattr(df['Close'].iloc[i], 'item') else df['Close'].iloc[i]
                ma20_val = df['ma20'].iloc[i].item() if hasattr(df['ma20'].iloc[i], 'item') else df['ma20'].iloc[i]
                rsi_val = df['rsi'].iloc[i].item() if hasattr(df['rsi'].iloc[i], 'item') else df['rsi'].iloc[i]
                macd_val = df['macd'].iloc[i].item() if hasattr(df['macd'].iloc[i], 'item') else df['macd'].iloc[i]
                macd_signal_val = df['macd_signal'].iloc[i].item() if hasattr(df['macd_signal'].iloc[i], 'item') else df['macd_signal'].iloc[i]
            except:
                # Fallback method using .values
                close_val = df['Close'].values[i]
                ma20_val = df['ma20'].values[i]
                rsi_val = df['rsi'].values[i]
                macd_val = df['macd'].values[i]
                macd_signal_val = df['macd_signal'].values[i]
            
            # Check if all values are valid (not NaN) and conditions are met
            if (not np.isnan(ma20_val) and 
                not np.isnan(rsi_val) and 
                not np.isnan(macd_val) and 
                not np.isnan(macd_signal_val) and
                close_val > ma20_val and 
                rsi_val > params['rsi_threshold'] and 
                macd_val > macd_signal_val):
                
                position = True
                entry_price = close_val
                entry_index = i
                df.at[df.index[i], 'signal'] = 1
        else:
            hold_period = i - entry_index
            try:
                macd_val = df['macd'].iloc[i].item() if hasattr(df['macd'].iloc[i], 'item') else df['macd'].iloc[i]
                macd_signal_val = df['macd_signal'].iloc[i].item() if hasattr(df['macd_signal'].iloc[i], 'item') else df['macd_signal'].iloc[i]
                exit_price_val = df['Close'].iloc[i].item() if hasattr(df['Close'].iloc[i], 'item') else df['Close'].iloc[i]
            except:
                macd_val = df['macd'].values[i]
                macd_signal_val = df['macd_signal'].values[i]
                exit_price_val = df['Close'].values[i]
            
            # Exit conditions
            if (not np.isnan(macd_val) and 
                not np.isnan(macd_signal_val) and
                (macd_val < macd_signal_val or hold_period >= params['max_hold_candles'])):
                
                trades.append((entry_price, exit_price_val))
                position = False
                df.at[df.index[i], 'signal'] = -1

    # Performance
    returns = [(sell - buy) / buy for buy, sell in trades]
    
    if len(returns) == 0:
        print("No trades executed.")
        return
    
    win_rate = (np.sum(np.array(returns) > 0) / len(returns)) * 100
    avg_return = np.mean(returns)
    
    print(f"  Parameters: MA={params['ma_period']}, RSI={params['rsi_period']}, RSI_threshold={params['rsi_threshold']}")
    print(f"  MACD: {params['macd_fast']}/{params['macd_slow']}/{params['macd_signal']}, Max_hold={params['max_hold_candles']}")
    print(f"  Trades       : {len(returns)}")
    print(f"  Win Rate     : {win_rate:.2f}%")
    print(f"  Avg Return   : {avg_return:.4f}")
    
    if len(returns) >= 4 and avg_return > 0 and win_rate >= 60:
        print(" MEETS ALL CRITERIA!")
    else:
        print(" Did not meet performance criteria.")
        if len(returns) < 4:
            print(f"    Need ≥4 trades (got {len(returns)})")
        if win_rate < 60:
            print(f"    Need ≥60% win rate (got {win_rate:.1f}%)")
        if avg_return <= 0:
            print(f"    Need positive avg return (got {avg_return:.4f})")

def compute_rsi(series, period=14):
    delta = series.diff()
    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)
    avg_gain = gain.rolling(window=period).mean()
    avg_loss = loss.rolling(window=period).mean()
    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

# Run strategy
for asset in assets:
    run_strategy(asset)