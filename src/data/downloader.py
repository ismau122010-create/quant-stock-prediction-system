import os
import logging 

import pandas as pd 
import yfinance as yf 
from datetime import datetime


logging.basicConfig(level=logging.INFO)

def download_market_data(ticker: str, start_date: str, end_date: str) -> pd.DataFrame: 

    """
     Download OHLCV market data for a ticker between start date and end date.

     Args: 
       ticker: stock symbol : SKYE
       start date : start date
       end date: end date


    returns :
      A pandas Dataframe with standardised PH;CV colum 

    Raises:
    Value error: if no data is returned 
    Exception: if download fails un expectedly      

    """


    try:

     # connect to data source API and request OHLCV data 

       data = yf.download(ticker, start=start_date, end=end_date, auto_adjust=False)
       
      # if request return no data 
       if data.empty:
         logging.error(f"No data returned for {ticker} from {start_date} to {end_date}")
         raise ValueError("empty dataset returned")
      
      # convert response to Dataframe 
       df = pd.DataFrame(data)

     # standardise column names 
       df = df.rename(columns={
        "Open": "open",
        "High": "high",
        "Low": "low",
        "Close": "close",
        "Adj Close": "adj_close",
        "Volume": "volume"
     })
      
    # reset index so date becomes a normal column
       df = df.reset_index()
    # Remove the mulitindex columns
       df.columns = df.columns.get_level_values(0)

       # remove column name
       df.columns.name = None


    # standardised date column name 
       if "Date" in df.columns:
          df = df.rename(columns={"Date": "date"})  

       return df

    except Exception as e:
       logging.error(f"Failed to download market data for {ticker}:{e}")
       raise



# ------------------------------------------------------------------------------


def save_raw_data(data: pd.DataFrame, ticker: str, output_path: str) -> None:
   """
   save new market data as CSV.

   Args:
   data: DataFrame containing market data
   ticker: stock ticker symbol (e.g, KYYE)
   output_path: Directory where file will be saved
   """

   if data.empty:
      logging.error("No data to save")
      return
   
   try:
      
      # build filename using ticker and date range 
      start_data = data["date"].min().strftime("%Y-%m-%d")
      end_date = data["date"].max().strftime("%Y-%m-%d")
        
        # Build filename automatically
      filename = f"{ticker}_{start_data}_to_{end_date}.csv"
      full_path = os.path.join(output_path, filename)

      # create directory if it does not exist 
      os.makedirs(output_path,exist_ok=True)

      # save data as CSV
      data.to_csv(full_path, index=False)

      # log save success 
      logging.info(f"Raw data saved successfully at : {full_path}")

   except Exception as e :
      logging.error(f"Failed to save raw data: {e}")  



if __name__ == "__main__":
    df = download_market_data("SKYE", "2020-01-01", "2024-01-01")
    print(df.head())    
    print(type(df.columns))
    save_raw_data(df, "SKYE", "data/raw")


