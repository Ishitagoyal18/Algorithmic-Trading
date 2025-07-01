# Algorithmic Trading in Python and C++
## Technical Indicators

In this project, we rely on three popular technical indicators—RSI, MACD, and EMA—to help signal potential entry and exit points. 

### Relative Strength Index (RSI)

The RSI (Relative Strength Index) is a momentum oscillator that oscillates between 0 and 100. It tells you when a market might be overbought or oversold:

- **Calculation**  
  RSI = 100 − (100 / (1 + RS)), where RS = average gain ÷ average loss over the look‑back period (commonly 14 days).
- **Interpretation**  
  - RSI > 70 → overbought (possible pullback)  
  - RSI < 30 → oversold (possible rebound)
- **Why we use it**  
  It’s great for spotting when a trend may be tired and due for a reversal.

### Moving Average Convergence Divergence (MACD)

MACD is a trend‑following momentum indicator that highlights the relationship between two EMAs (typically 12‑day and 26‑day):

- **Components**  
  - **MACD Line** = 12‑day EMA − 26‑day EMA  
  - **Signal Line** = 9‑day EMA of the MACD Line  
  - **Histogram** = MACD Line − Signal Line
- **Interpretation**  
  - MACD Line crossing **above** Signal Line → bullish signal  
  - MACD Line crossing **below** Signal Line → bearish signal  
- **Why we use it**  
  It smooths out price action and helps confirm trend shifts.

### Exponential Moving Average (EMA)

EMA gives more weight to recent prices, making it quicker to react than a simple moving average:

- **Formula**  
  EMA<sub>today</sub> = (Price<sub>today</sub> × α) + (EMA<sub>yesterday</sub> × (1 − α)),  
  where α = 2 / (N + 1) and N is the period (e.g., 12, 26, 50, 200).
- **Key levels**  
  Traders often watch the 50‑ and 200‑period EMAs to gauge medium‑ and long‑term trends.
- **Why we use it**  
  When price stays above the EMA, the trend is likely up; when it falls below, the trend may be turning down.


  ## Assets used
8 Indian stocks across diverse sectors <br/>
EICHERMOT.NS (Auto)<br/>
VBL.NS (FMCG)<br/>
TRENT.NS (Retail)<br/>
FIRSTCRY.NS (Consumer)<br/>
TCS.NS (Technology)<br/>
DIVISLAB.NS (Pharma)<br/>
SBIN.NS (Banking)<br/>
BAJFINANCE.NS (Finance)<br/>
Timeframe: 15-minute intervals<br/>
Lookback Period (Backtest): 25 days<br/>


