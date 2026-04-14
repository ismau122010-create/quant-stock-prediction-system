
import pandas as pd 
import logging

logging.basicConfig(level=logging.INFO)

def add_daily_return(data: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate daily percentage return from the Close price
    and store it in a new column called 'daily_return'.

    Args:
        data: DataFrame containing at least a 'close' column

    Returns:
        DataFrame with added 'daily_return' column
    """

    if "close" not in data.columns:
        logging.error("Missing close column.")
        raise ValueError("close column required to calculate daily return")
    

    # calculate percentage change of close price 
    data["daily_return"] = data["close"].pct_change()

    
    return data






# -------------------------------


def add_moving_average(data: pd.DataFrame, windows: list) -> pd.DataFrame:
     """
    Add Simple Moving Average (SMA) columns for given window sizes.

    Args:
        data: DataFrame containing at least a 'close' column
        windows: List of window sizes (e.g., [5, 10, 20])

    Returns:
        DataFrame with added SMA columns
    """
     
     if "close" not in data.columns:
         logging.error("Missing close column.")
         raise ValueError("close column required to calculate moving average")
     
     # for each window in windows
     for window in windows:
         # calculate rolling mean of close over winodw
         column_name = f"SMA_{window}"
         data[column_name] = data["close"].rolling(window=window).mean()

         logging.info(f"added {column_name}")
     return data     






# --------------------------

def add_rsi(data: pd.DataFrame, window: int) -> pd.DataFrame:
     """
    Calculate Relative Strength Index (RSI) and add it as a column.

    Args:
        data: DataFrame containing at least a 'close' column
        window: RSI lookback period (default = 14)

    Returns:
        DataFrame with added 'RSI' column
    """
    
     if "close" not in data.columns:
         logging.error("Missing close column")
         raise ValueError("Close column required")
     
     # calculate price changes
     delta = data["close"].diff()

     # separate gains and losses
     gain = delta.clip(lower=0)
     loss = -delta.clip(upper=0)

     # compute average gain and average loss over rolling window
     avg_gain = gain.rolling(window=window).mean()
     avg_loss = loss.rolling(window=window).mean()

     # calculate relative strength 
     rs = avg_gain / avg_loss

     # calculate RSI
     rsi = 100-(100/(1+rs))

     # store in RSI column 

     data["RSI"] = rsi

     return data






# -----------------------------
# 

def add_macd(
        data: pd.DataFrame,
        fast_window: int,
        slow_window: int,
        signal_window: int
)  -> pd.DataFrame:
    
    """
    Calculate MACD indicator and add MACD line, signal line,
    and histogram to the DataFrame.

    Args:
        data: DataFrame containing at least a 'close' column
        fast_window: period for fast EMA (default = 12)
        slow_window: period for slow EMA (default = 26)
        signal_window: period for signal line EMA (default = 9)

    Returns:
        DataFrame with MACD columns added
    """

    if "close" not in data.columns:
        logging.error("missing close column")
        raise ValueError("close column required to calculate MACD")
    
    # calculate fast EMA of close
    fast_ema = data["close"].ewm(span=fast_window, adjust=False).mean()

    # calculate slow EMA of close
    slow_ema = data["close"].ewm(span=slow_window, adjust=False).mean()

    # calculate MACD line = fast EMA - slow EMA
    data["MACD"] = fast_ema - slow_ema

    # calculate MACD signal line 
    data["MACD_signal"] = data["MACD"].ewm(span=signal_window, adjust=False).mean()

    # calculate MACD histogram
    data["MACD_hist"] = data["MACD"] - data["MACD_signal"]

    return data






    # ------------------------------------


def add_atr(data: pd.DataFrame, window: int) -> pd.DataFrame:
        """
        Calculate Average True Range (ATR) and add it as a column.

        Args:
          data: DataFrame containing 'high', 'low', and 'close'
          window: ATR rolling window size (default = 14)

        Returns:
         DataFrame with added 'ATR' column
        """
    
        
        required_columns = ["high","low","close"]

        for col in required_columns:
          if col not in data.columns:
              logging.error(f"Missing column: {col}")
              raise ValueError("high, low, close columns required for ATR calculations")
          
        # calculate previous close
        prev_close = data["close"].shift(1)

        # calculate TR true range for each row
        tr1 = data["high"] - data["low"]
        tr2 = (data["high"] - prev_close).abs()
        tr3= (data["low"] -prev_close).abs()

        True_range = pd.concat([tr1,tr2,tr3], axis=1).max(axis=1)

        # calculate rolling average of true range ATR

        data["ATR"] = True_range.rolling(window=window).mean()

        return data





# --------------------------------

def add_rolling_volatility(data:pd.DataFrame, window: int) -> pd.DataFrame:
    """
    Calculate rolling volatility (standard deviation of returns)
    and add it as a column.

    Args:
        data: DataFrame containing either 'daily_return' or 'close'
        window: rolling window size (default = 14)

    Returns:
        DataFrame with added 'rolling_volatility' column
    """
    
    # if daily_return doesnt exist calculate it first
    if"daily_return" not in data.columns:
        if"close" not in data.columns:
            logging.error("missing close column")
            raise ValueError("close column required to compute returns")
        
        data["daily_return"] = data["close"].pct_change()

        # calculate rolling standard deviation of returns 
        data["rolling_volatility"] = (
            data["daily_return"]
            .rolling(window=window)
            .std()
        )
    return data    





def add_volume_features(data:pd.DataFrame, window: int) -> pd.DataFrame:
    """
    Add volume-based features to the dataset.

    Features:
    - volume_change_pct
    - volume_sma (rolling average volume)
    - relative_volume

    Args:
        data: DataFrame containing 'volume'
        window: rolling window size (default = 20)

    Returns:
        DataFrame with added volume feature columns
    """ 
    
    if "volume" not in data.columns:
        logging.error("missing volume column")
        raise ValueError("volume column required")
    
    # calculate volume change precentage
    data["volume_change_pct"] = data["volume"].pct_change()

    # calculate rolling average volume
    data["volume_sma"] = data["volume"].rolling(window=window).mean()

    # calculate relative volume = current volume / rolling volume precentage 
    data ["relative_volume"] = data["volume"] / data["volume_sma"]

    return data



if __name__ == "__main__":
    

    df = pd.read_csv("data/raw/SKYE_2020-01-02_to_2023-12-29.csv")
    window = 14
    
    
    df = add_volume_features(df,window)

    print(df[["date", "volume", "volume_change_pct", "volume_sma", "relative_volume"]].tail(10))