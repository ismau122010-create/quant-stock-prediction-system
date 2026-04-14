import logging
import pandas as pd


from src.features.indicators import add_daily_return
from src.features.indicators import add_moving_average
from src.features.indicators import add_rsi
from src.features.indicators import add_macd
from src.features.indicators import add_atr
from src.features.indicators import add_rolling_volatility
from src.features.indicators import add_volume_features
from src.features.lag_features import add_lagged_features
from src.features.lag_features import add_price_position_features
from config.settings import FEATURE_WINDOWS
from config.settings import TARGET_SETTINGS
from src.features.target_builder import build_binary_target
from src.features.target_builder import remove_leakage_columns


logging.basicConfig(level=logging.INFO)


def build_feature_pipeline(data, settings): 
    """
    Build full feature engineering pipeline.

    Steps:
    1. Add daily return
    2. Add moving averages
    3. Add RSI
    4. Add MACD
    5. Add ATR
    6. Add rolling volatility
    7. Add volume features
    8. Add lagged features
    9. Add price position features
    10. Drop NaN rows caused by rolling windows
    """

    # CALL add_daily_return
    data = add_daily_return(data)

    # CALL add_moving_averages
    data = add_moving_average(
        data,
        settings["feature_windows"]["ma_windows"]
    )

    # CALL add_rsi
    data = add_rsi(
        data,
        settings["feature_windows"]["rsi_window"]
    )

    # CALL add_macd
    data = add_macd(
    data,
    settings["feature_windows"]["macd_fast_window"],
    settings["feature_windows"]["macd_slow_window"],
    settings["feature_windows"]["macd_signal_window"]
)

    # CALL add_atr
    data = add_atr(
        data,
        settings["feature_windows"]["atr_window"]
    )

    # CALL add_rolling_volatility
    data = add_rolling_volatility(
        data,
       settings["feature_windows"]["volatility_window"]
       
    )

    # CALL add_volume_features
    data = add_volume_features(
        data,
       settings["feature_windows"]["volume_window"]
    )

    # CALL add_lagged_features
    data = add_lagged_features(
        data,
        settings["feature_windows"]["lag_columns"],
        settings["feature_windows"]["lag_periods"]
    )

    # CALL add_price_position_features
    data = add_price_position_features(data)

    # DROP rows with NaN values caused by rolling windows and lags
    data = data.dropna()

    logging.info("Feature pipeline completed successfully.")

    return data


    


# -----------------------------------------

def prepare_modelling_dataset(data, settings):
    """
    Prepare dataset for machine learning modelling.

    Steps:
    1. Build feature pipeline
    2. Build binary target column
    3. Remove leakage columns
    4. Drop rows with missing target
    5. Return final modelling dataset
    """

    # call build_feature_pipeline
    data = build_feature_pipeline(data,settings)

    # call build binary_target
    data = build_binary_target(
        data,
        horizon=settings["target_settings"]["future_horizon"],
        threshold=settings["target_settings"]["return_threshold"]
    )

   
     # call remove_leakage_columns
    data = remove_leakage_columns(data)
    # drop rows with missing target
    data = data.dropna(subset=["target"])

    

    logging.info("Final modelling dataset prepared successfully")

    return data

if __name__ == "__main__":
    

    df = pd.read_csv("data/raw/SKYE_2020-01-02_to_2023-12-29.csv")
    settings = {
    "feature_windows": FEATURE_WINDOWS,
    "target_settings": TARGET_SETTINGS
}
    
      
    df2 = prepare_modelling_dataset(df,settings)

    print(df2.head())
    print(df2.columns)

    