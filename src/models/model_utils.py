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
