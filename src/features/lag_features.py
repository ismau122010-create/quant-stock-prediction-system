import pandas as pd
import logging



logging.basicConfig(level=logging.INFO)


def add_lagged_features(
        data: pd.DataFrame,
        columns: list,
        lag_periods: list
) -> pd.DataFrame:
    
     """
    Add lagged versions of selected columns.

    Args:
        data: Input DataFrame
        columns: List of column names to lag (e.g. ["close", "volume"])
        lag_periods: List of lag periods (e.g. [1, 2, 3, 5])

    Returns:
        DataFrame with lagged feature columns added
    """
     
     for column in columns:
          if column not in data.columns:
               logging.warning(f"column {column} not found. skipping")
               continue
          
          # for each lag in lag_periods
          for lag in lag_periods:
               
               # shift column by lag periods
               lagged_column_name = f"{column}_lag_{lag}"

               data[lagged_column_name] = data[column].shift(lag)

               logging.info(f"added {lagged_column_name}")

     return data           





def add_price_position_features(data: pd.DataFrame) -> pd.DataFrame:
    """
    Add binary features indicating whether Close price
    is above selected moving averages.

    Features created:
    - close_above_SMA_10
    - close_above_SMA_20
    - close_above_SMA_50
    """

    required_columns = ["close","SMA_10","SMA_20", "SMA_50"]

    for col in required_columns:
         if col not in data.columns:
              logging.error(f"missing column: {col}")
              raise ValueError (
                "Close and SMA_10, SMA_20, SMA_50 must exist before calling this function.")
         
    # calculate wether close > SMA10
    data["close_above_SMA_10"] = (data["close"] > data["SMA_10"]).astype(int)

    data["close_above_SMA_20"] = (data["close"] > data["SMA_20"]).astype(int)

    data["close_above_SMA_50"] = (data["close"] > data["SMA_50"]).astype(int)


    return data      


              
