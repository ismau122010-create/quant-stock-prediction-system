# Data settings 
# -------------------------

DATA_SOURCE= "Yfinance"
TICKERS = ["SKYE"]
START_DATA = "2018-01-01"
END_DATA = "2025-01-01"

REQUIREMED_COLUMNS = ["data", "open", "high", "low","close","volume"]


# Feature settings 

FEATURE_WINDOWS = {
    "ma_windows": [10, 20, 50],
    "rsi_window": 14,
    "atr_window": 14,
    "macd_fast_window": 12,
    "macd_slow_window": 26,
    "macd_signal_window": 9,
    "volume_window": 14,
    "lag_columns": ["close", "volume"],
    "volatility_window": 20,
    "lag_periods": [1, 2, 3, 5]
}


# Target settings

TARGET_SETTINGS = {
    "target_type": "binary_classification",     # e.g. up/down
    "future_horizon": 5,                         # predict 5 days ahead
    "return_threshold": 0.02                   # 2% threhold
}


# model settings

MODEL_SETTINGS = {
  "model_name": "logistic_regression",
  "train_ratio": 0.70,
  "validation_ratio": 0.15,
  "test_ratio":0.15,
  "random_state":42,
  "model_hyperparameteres": {
    "penalty": "12",       # regularization type
     "C": 1.0,            # inverse regularization strenght 
     "solver": "ibfgs",   # optimization algorithm 
     "max_iter": 1000     # training iterations 
   }

}


# Signal settings 

SIGNAL_SETTINGS = {
    "buy_probability_threshold": 0.60,
    "sell_probability_threshold": 0.40,
    "hold_zone": (0.40,0.60)
}


# Risk settings 

RISK_SETTINGS = {
   "initial_captial": 1000,
   "risk_per_trade": 0.01,
   "stop_loss_pct": 0.02,
   "take_profit_pct": 0.04,
   "max_open_positions":3,
   "commission_pct":0.001,
   "slippage_pct":0.001

}

# PATH SETTHINGS

PATH_SETTINGS = {
    "raw_data_path":"data/raw/",
    "interim_data_path":"data/interim/",
    "processed_data_path": "data/processed/",
    "model/path": "models/trained/",
    "results_path": "data/results/",
    "report_path": "reports/"
}