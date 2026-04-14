import logging 
import os
import pandas as pd 

logging.basicConfig(level=logging.INFO)


def clean_market_data(data: pd.DataFrame) -> pd.DataFrame:
    """
    Clean raw market OHLCV data.

    Steps:
    - Copy input data
    - Convert date column to datetime
    - Sort rows by date ascending
    - Remove duplicate rows
    - Drop duplicate dates
    - Handle missing values
    - Ensure numeric columns are numeric
    - Remove rows with invalid OHLCV values
    - Reset index
    """

   # Copy input data
    df= data.copy()

    # convert date column to datetime 
    if "date" not in df.columns:
        logging.error("Missing date column")
        raise ValueError("Date column required")
    
    df["date"] = pd.to_datetime(df["date"], errors="coerce")

    # sort rows by date ascending 
    df = df.sort_values(by="date")

    # remove duplicate rows
    df = df.drop_duplicates()

    # drop duplicate dates if necessary
    df = df.drop_duplicates(subet=["date"])

    # handle missing values
    df = df.ffill()  # forward fill where appropriate
    df = df.dropna()  # drop rows that is unusable 

    # Ensure numeric columns are numeric 
    numeric_columns = ["open", "high", "low", "close", "volume"]

    for col in numeric_columns:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    # Remove rows with invalid OHLCV VALUES
    # its a boolean series of true/false per row)
    invalid_rows = (
        (df["open"]< 0) |
        (df["high"] < 0)|
        (df["low"] < 0) |
        (df["close"] < 0) |
        (df["volume"] < 0)|
        (df["high"] < df["low"])
    )        
    # this will remove the only the true rows above and only keeps false.
    df = df[~invalid_rows]

    # Reset index

    df = df.reset_index(drop=True)

    return df



# -------------------

def save_cleaned_data(data: pd.DataFrame, ticker: str, output_path: str) -> str:
    """
    Save cleaned market data as CSV.

    Args:
        data: Cleaned DataFrame
        ticker: Stock ticker symbol (e.g., AAPL)
        output_path: Directory where file will be saved

    Returns:
        Full path of saved file
    """

    if data.empty:
        logging.error("No cleaned data to save.")
        raise ValueError("Cannot save empty dataset")
    
    try:
        # build cleaned filename using data range
        start_date = data["date"].min().strftime("%Y-%m-%d")
        end_date = data["date"].max().strftime("%Y-%m-%d")

        filename = f"{ticker}_cleaned_{start_date}_to_{end_date}.csv"
        full_path = os.path.join(output_path, filename)

        # create folder if missing
        os.makedirs(output_path, exist_ok=True)

        # Save dataframe to csv
        data.to_csv(full_path, index=False)

        # log success 
        logging.info(f"cleaned data saved successfully at : {full_path}")

        return full_path
    
    except Exception as e:
        logging.error(f"failed to save cleaned data: {e}")
        raise


