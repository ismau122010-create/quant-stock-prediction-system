import logging 
import pandas as pd

logging.basicConfig(level=logging.info)

def validate_required_columns(data: pd.DataFrame, required_columns: list) -> bool:

    """
    Check whether required columns exist in a DataFrame.

    Args:
        data: Input DataFrame
        required_columns: List of required column names

    Returns:
        True if all required columns exist, otherwise False
    """
        
    for column in required_columns:    
        if column not in data.columns:
            logging.error(f"Missing required column: {column}")
            return False
    return True


# ----------------

def validate_data_order(data: pd.DataFrame) -> bool:

    """
    Validate whether the 'date' column exists, is convertible to datetime,
    and is sorted in ascending order.

    Args:
        data: Input DataFrame

    Returns:
        True if validation passes, otherwise False
    """
      # Check if date column exists
    if "date" not in data.columns:
        logging.error("Missing 'date' column.")
        return False
    
    # check if date column can be converted to datetime

    try:
        data["date"] = pd.to_datetime(data["date"])
    except Exception:
        logging.error("date column cannot be converted to datetime") 
        return False

    # check if dates are sorted asending 

    if not data["date"].is_monotonic_decreasing:
        logging.error("dates are not sorted in ascending order. ")
        return False

    return True       


# -----------------------

def validate_ohlcv_values(data: pd.DataFrame) -> bool:
    """
    Validate OHLCV values in the dataset.

    Checks:
    - Open, High, Low, Close, Volume are numeric
    - No negative prices
    - Volume is not negative
    - High is not below Low

    Returns:
        True if valid, False otherwise
    """
    required_columns = ["open","high","low","close","volume"]

    # check required columns exist 
    for col in required_columns:
        if col not in data.columns:
            logging.error(f"Missing column: {col}")
            return False
        
    # check numeric values:
    for col in required_columns:
        if not pd.api.types.is_numeric_dtype(data[col]):
            logging.error(f"Column {col} is not numeric")   
            return False 

    # check for negative prices 
    if (data[["open","high","low","close"]] < 0).any().any():
       logging.warning("Negative price values detected")
       return False
    
    # Check for negative volume
    if (data["volume"] < 0).any():
        logging.warning("negative volume values detected")
        return False

    # check high is not below low
    if (data["high"]< data["low"]).any():
        logging.warning("some rows have high < low")
        return False
    return True


