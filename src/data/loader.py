import os 
import logging
import glob
import pandas as pd 


logging.basicConfig(level=logging.INFO)


def load_csv_data(file_path: str) -> pd.DataFrame:

   """
    Load CSV file into a pandas DataFrame.

    Args:
        file_path: Path to the CSV file

    Returns:
        DataFrame containing CSV data

    Raises:
        FileNotFoundError: If file does not exist
    """
   
   # check whether file exists 

   if not os.path.exists(file_path):
      logging.error(f"File not found: {file_path}")
      raise FileNotFoundError(f"No file found at {file_path}")
   
   try:
      # Read CSV into Dataframe 

      df = pd.read_csv(file_path)

      logging.info("CSV file loaded successfully")

      return df
   
   except Exception as e:
      logging.error(f"Failed to load CSV file: {e}")
      raise
   

# -------------------------
# Load latest dataset automatically without inserting the path of the datafile
#  This is called modular pipeline design, it makes the system resustable,automated,scaleable and production ready.
# # Its exactly the architecture used in trading system and data pipelines. 

# analogy: instead of opening specific book the load latest function opens the newest book from the shelf automatically. 

def load_latest_raw_data(ticker: str, raw_data_folder: str) -> pd.DataFrame:
    """
    Load the most recent raw CSV file for a given ticker.

    Args:
        ticker: Stock ticker symbol (e.g., SKYE)
        raw_data_folder: Folder where raw CSV files are stored

    Returns:
        DataFrame containing the latest raw data
    """

    # Find all CSV files matching ticker pattern
    pattern = os.path.join(raw_data_folder, f"{ticker}_*.csv")
    matching_files = glob.glob(pattern)

    if not matching_files:
       logging.error(f"No raw data files found for ticker: {ticker}")
       raise FileNotFoundError(f"No raw CSV files found for {ticker}")
    
    # Select the latest file based on modiviction time
    latest_file = max(matching_files, key=os.path.getmtime)

    logging.info(f"Latest file found: {latest_file}")

    # Load CSV using load_csv_data
    df = load_csv_data(latest_file)

    return df


if __name__ == "__main__":
    file_path = "data/raw"

    df = load_latest_raw_data("SKYE", file_path)

    print(df.head())
    print(type(df.columns))