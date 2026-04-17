import logging
import pandas as pd

logging.basicConfig(level=logging.INFO)

from sklearn.linear_model import LogisticRegression

def select_model(model_name: str, hyperparameters: dict):
    """
    Select and initialize a machine learning model.

    Args:
        model_name: name of the model to use
        hyperparameters: dictionary of model hyperparameters

    Returns:
        Initialized model object
    """
    if model_name == "logistic_regression":
       model = LogisticRegression(**hyperparameters)

    else:
        raise ValueError(f"unsupported model: {model_name}")   

    logging.info(f"{model_name} model created successfully")

    return model

if __name__ == "__main__":
    
    

    model = select_model(
        "logistic_regression",
        {"max_iter": 1000}
    )

    print(model)


# ---------------------------------------------------

def split_features_target(
    data: pd.DataFrame,
    target_column: str,
    non_feature_columns: list = None
):
    """
    Split dataset into features (X) and target (y).

    Args:
        data: modelling dataset DataFrame
        target_column: name of target column (e.g., "target")
        non_feature_columns: optional list of columns to exclude
                             (e.g., ["date", "ticker"])

    Returns:
        X: feature DataFrame
        y: target Series
    """

    # Ensure target column exists 
    if target_column not in data.columns:
        logging.error(f"target column {target_column} not found")
        raise ValueError("target column missing from dataset")
    
    # handle optional exclusion columns
    if non_feature_columns is None:
        non_feature_columns = []

    # combine columns to drop from features 
    columns_to_drop = [target_column] + non_feature_columns

    # x= all columns except target column and non feature columns
    X = data.drop(columns=columns_to_drop, errors="ignore")

    # y = target column 
    y = data[target_column]

    logging.info("successfully split dataset into X (features) and y(target)")    

    return X,y

# -------------------------------

def time_series_train_test_split(X: pd.DataFrame, y: pd.Series, train_ratio: float):
    """
    Split dataset into train/test sets while preserving chronological order.

    Args:
        X: feature DataFrame
        y: target Series
        train_ratio: proportion of data used for training (e.g., 0.8)

    Returns:
        X_train, X_test, y_train, y_test
    """

    # validate ratio 

    if not 0 < train_ratio < 1:
        raise ValueError("train_ratio must be between 0 and 1")
    
    # calculate split index based on chronological order

    split_index = int(len(X) * train_ratio)

    # X_train = rows before split
    X_train = X.iloc[:split_index]

    # X_test = rows after split
    X_test = X.iloc[split_index:]

    # Y_train = rows before split
    Y_train = y.iloc[:split_index]

    # Y_test = rows before split 
    Y_test = y.iloc[split_index:]

    return X_train,X_test,Y_train,Y_test

if __name__ == "__main__":

    import pandas as pd

    # Example dataset
    df = pd.DataFrame({
        "open": [10, 11, 12, 13, 14],
        "close": [11, 10, 13, 15, 16],
        "target": [1, 0, 1, 1, 0]
    })

    X = df[["open", "close"]]
    y = df["target"]

    X_train, X_test, y_train, y_test = time_series_train_test_split(
        X, y, train_ratio=0.6
    )

    print("X_train:\n", X_train)
    print("\nX_test:\n", X_test)
    print("\ny_train:\n", y_train)
    print("\ny_test:\n", y_test)

