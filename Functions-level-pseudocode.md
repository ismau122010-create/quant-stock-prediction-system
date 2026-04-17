A. config/settings.py
Purpose

Store all system settings in one place.


DEFINE DATA_SOURCE
DEFINE TICKERS
DEFINE START_DATE
DEFINE END_DATE

DEFINE REQUIRED_COLUMNS = [Date, Open, High, Low, Close, Volume]

DEFINE FEATURE_WINDOWS
    short_moving_average_window
    medium_moving_average_window
    long_moving_average_window
    rsi_window
    atr_window
    volatility_window
    lag_periods

DEFINE TARGET_SETTINGS
    target_type
    future_horizon
    return_threshold

DEFINE MODEL_SETTINGS
    model_name
    train_ratio
    validation_ratio
    test_ratio
    random_state
    model_hyperparameters

DEFINE SIGNAL_SETTINGS
    buy_probability_threshold
    sell_probability_threshold
    hold_zone

DEFINE RISK_SETTINGS
    initial_capital
    risk_per_trade
    stop_loss_pct
    take_profit_pct
    max_open_positions
    commission_pct
    slippage_pct

DEFINE PATH_SETTINGS
    raw_data_path
    interim_data_path
    processed_data_path
    model_path
    results_path
    report_path


------------------------------------------------------------------------------------    

B. src/data/downloader.py

  1. download_market_data(ticker, start_date, end_date)

FUNCTION download_market_data(ticker, start_date, end_date):
    CONNECT to data source API
    REQUEST OHLCV data for ticker between start_date and end_date

    IF request fails:
        LOG error
        RETURN empty dataset or raise exception

    CONVERT response into DataFrame
    STANDARDISE column names
    RETURN DataFrame
END FUNCTION

  2. save_raw_data(data, ticker, output_path)

  FUNCTION save_raw_data(data, ticker, output_path):
    BUILD filename using ticker and date range
    CREATE directory if it does not exist
    SAVE data as CSV
    LOG save success
   END FUNCTION
--------------------------------------------------------------------------------------------

C. src/data/loader.py

  1. load_csv_data(file_path)


  FUNCTION load_csv_data(file_path):
    CHECK whether file exists
    IF file does not exist:
        LOG error
        RAISE file not found exception

    READ CSV into DataFrame
    RETURN DataFrame
END FUNCTION



  2. load_latest_raw_data(ticker, raw_data_folder)

    FUNCTION load_latest_raw_data(ticker, raw_data_folder):
    FIND latest raw CSV for ticker
    LOAD CSV using load_csv_data
    RETURN DataFrame
END FUNCTION


--------------------------------------------------------------

D. src/data/validator.py

  1. validate_required_columns(data, required_columns)

    FUNCTION validate_required_columns(data, required_columns):
    FOR each column in required_columns:
        IF column not in data.columns:
            LOG missing column
            RETURN False

    RETURN True
END FUNCTION

  2. validate_date_order(data)
  

  FUNCTION validate_date_order(data):
    CHECK if Date column exists
    CHECK if Date column can be converted to datetime
    CHECK if dates are sorted ascending

    IF any check fails:
        RETURN False

    RETURN True
END FUNCTION

 3. validate_ohlcv_values(data)

   FUNCTION validate_ohlcv_values(data):
    CHECK Open, High, Low, Close, Volume are numeric
    CHECK no impossible negative prices
    CHECK Volume is not negative
    CHECK High is not below Low

    IF invalid rows found:
        LOG warning
        RETURN False

    RETURN True
 END FUNCTION

 ------------------------------------------------------


   
E. src/data/cleaner.py
1. clean_market_data(data)

 FUNCTION clean_market_data(data):
    COPY input data

    CONVERT Date column to datetime
    SORT rows by Date ascending
    REMOVE duplicate rows
    DROP duplicate dates if necessary

    HANDLE missing values
        forward fill where appropriate
        drop rows that remain unusable

    ENSURE numeric columns are numeric
    REMOVE rows with invalid OHLCV values

    RESET index
    RETURN cleaned DataFrame
END FUNCTION

2. save_cleaned_data(data, ticker, output_path)

FUNCTION save_cleaned_data(data, ticker, output_path):
    BUILD cleaned filename
    CREATE folder if missing
    SAVE DataFrame to CSV
    LOG success
END FUNCTION

-------------------------------------------------------------------------

F. src/features/indicators.py
1. add_daily_return(data)
  FUNCTION add_daily_return(data):
    CALCULATE percentage change of Close price
    STORE result in daily_return column
    RETURN data
END FUNCTION


2. add_moving_averages(data, windows)
  FUNCTION add_moving_averages(data, windows):
    FOR each window in windows:
        CALCULATE rolling mean of Close over window
        STORE as SMA_window

    RETURN data
END FUNCTION

3. add_rsi(data, window)
  FUNCTION add_rsi(data, window):
    CALCULATE price changes
    SEPARATE gains and losses
    COMPUTE average gain and average loss over rolling window
    CALCULATE relative strength
    CALCULATE RSI
    STORE in RSI column
    RETURN data
END FUNCTION

4. add_macd(data)

FUNCTION add_macd(data):
    CALCULATE fast EMA of Close
    CALCULATE slow EMA of Close
    COMPUTE MACD line = fast EMA - slow EMA
    COMPUTE MACD signal line
    COMPUTE MACD histogram if needed
    STORE results
    RETURN data
END FUNCTION

5. add_atr(data, window)
FUNCTION add_atr(data, window):
    CALCULATE true range for each row
    CALCULATE rolling average of true range
    STORE as ATR column
    RETURN data
END FUNCTION

6. add_rolling_volatility(data, window)

FUNCTION add_rolling_volatility(data, window):
    CALCULATE rolling standard deviation of returns
    STORE as rolling_volatility
    RETURN data
END FUNCTION

7. add_volume_features(data, window)

FUNCTION add_volume_features(data, window):
    CALCULATE volume change percentage
    CALCULATE rolling average volume
    CALCULATE relative volume = current volume / rolling volume average
    STORE results
    RETURN data
END FUNCTION


--------------------------------------------------------------------

G. src/features/lag_features.py

1. add_lagged_features(data, columns, lag_periods)
 
 FUNCTION add_lagged_features(data, columns, lag_periods):
    FOR each column in columns:
        FOR each lag in lag_periods:
            SHIFT column by lag periods
            STORE as column_lag_lagNumber

    RETURN data
END FUNCTION

2. add_price_position_features(data)

FUNCTION add_price_position_features(data):
    CALCULATE whether Close > SMA_10
    CALCULATE whether Close > SMA_20
    CALCULATE whether Close > SMA_50
    STORE binary features
    RETURN data
END FUNCTION

-----------------------

H. src/features/target_builder.py

1. build_binary_target(data, horizon, threshold)

 FUNCTION build_binary_target(data, horizon, threshold):
    CALCULATE future_return = (future Close after horizon / current Close) - 1

    FOR each row:
        IF future_return > threshold:
            target = 1
        ELSE:
            target = 0

    STORE target column
    RETURN data
END FUNCTION

2. remove_leakage_columns(data)

 FUNCTION remove_leakage_columns(data):
    REMOVE columns that directly reveal future information
    REMOVE temporary future return columns if not needed for modelling
    RETURN data
END FUNCTION

---------------------------------------------------------------

I. src/features/feature_pipeline.py
 1. build_feature_pipeline(data, settings)
   FUNCTION build_feature_pipeline(data, settings):
    CALL add_daily_return
    CALL add_moving_averages
    CALL add_rsi
    CALL add_macd
    CALL add_atr
    CALL add_rolling_volatility
    CALL add_volume_features
    CALL add_lagged_features
    CALL add_price_position_features

    DROP rows with NaN values caused by rolling windows and lags
    RETURN feature-enriched data
END FUNCTION

2. prepare_modelling_dataset(data, settings)
  FUNCTION prepare_modelling_dataset(data, settings):
    CALL build_feature_pipeline
    CALL build_binary_target
    CALL remove_leakage_columns
    DROP rows with missing target
    RETURN final modelling dataset
END FUNCTION

-----------------------------------------------------------
J. src/models/model_utils.py


 1. select_model(model_name, hyperparameters)
   
   FUNCTION select_model(model_name, hyperparameters):
    IF model_name is logistic_regression:
        CREATE Logistic Regression model using hyperparameters

    ELSE IF model_name is decision_tree:
        CREATE Decision Tree model

    ELSE IF model_name is random_forest:
        CREATE Random Forest model

    ELSE IF model_name is xgboost:
        CREATE XGBoost model

    ELSE:
        RAISE unsupported model error

    RETURN model
END FUNCTION


2. split_features_target(data, target_column)
  
  FUNCTION split_features_target(data, target_column):
    X = all columns except target_column and non-feature columns
    y = target_column
    RETURN X, y
END FUNCTION

 3. time_series_train_test_split(X, y, train_ratio)

   FUNCTION time_series_train_test_split(X, y, train_ratio):
    CALCULATE split index based on chronological order
    X_train = rows before split
    X_test = rows after split
    y_train = rows before split
    y_test = rows after split

    RETURN X_train, X_test, y_train, y_test
END FUNCTION

--------------------------------------

K. src/models/train.py

 
 1. train_model(X_train, y_train, model_name, hyperparameters)

 FUNCTION train_model(X_train, y_train, model_name, hyperparameters):
    CALL select_model to create model
    FIT model on X_train and y_train
    RETURN trained model
END FUNCTION

2. save_model(model, model_path, metadata)

 FUNCTION save_model(model, model_path, metadata):
    SERIALISE model to disk
    SAVE metadata file
    LOG model save success
END FUNCTION


----------------------------------------------------------------