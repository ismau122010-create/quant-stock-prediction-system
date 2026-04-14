import pandas as pd
import logging


logging.basicConfig(level=logging.INFO)


def build_binary_target(
    data: pd.DataFrame,
    horizon: int,
    threshold: float
) -> pd.DataFrame:
    """
    Build binary target column based on future returns.

    Args:
        data: DataFrame containing 'close' column
        horizon: number of days ahead to look (e.g., 5)
        threshold: return threshold (e.g., 0.02 for +2%)

    Returns:
        DataFrame with 'target' column added
    """
    
    if "close" not in data.columns:
        logging.error("Missing close column")
        raise ValueError("close column required to build target")
    
    # Calculate future close price 
    # Note : future_close = close price after 2 days
    # The reason we do this is because in ML we need to compare the price today vs future price
    future_close = data["close"].shift(-horizon)

    # calculate future_return
    data["future_return"] = (future_close / data["close"]) -1

    # BUILD binary target column
    data["target"] = (data["future_return"] > threshold).astype(int)

    logging.info("Binary target column created successfully")

    return data




# -----------------------------------------------------------------

def remove_leakage_columns(data):
    """
    Remove columns that reveal future information
    and should not be used as model features.
    """

    # Columns that typically cause leakage
    leakage_columns = [
        "future_return",
        
        
    ]
    
    # remove columns only if they exist 
    columns_to_drop = [col for col in leakage_columns if col in data.columns]

    if columns_to_drop:
        data = data.drop(columns=columns_to_drop)
        logging.info(f"removed leakage columns: {columns_to_drop}")
    return data


if __name__ == "__main__":
    

    df = pd.read_csv("data/raw/SKYE_2020-01-02_to_2023-12-29.csv")
    horizon = 2
    threshold = 0.0001

    df1 = build_binary_target(df,horizon,threshold)
    print(df1)
    
    df2 =  remove_leakage_columns(df1)

    print((df2).tail(10))
    print(df2.columns)
