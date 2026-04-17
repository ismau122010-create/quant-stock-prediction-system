import logging
import pandas as pd

import os
import json
import logging
import joblib


from src.models.model_utils import select_model



logging.basicConfig(level=logging.INFO)


def train_model(X_train, y_train, model_name: str, hyperparameters: dict):
    """
    Train machine learning model.

    Args:
        X_train: training feature dataset
        y_train: training target labels
        model_name: model type (e.g. 'logistic_regression')
        hyperparameters: dictionary of model hyperparameters

    Returns:
        trained model
    """

    # Call select model to create model
    model = select_model(model_name,hyperparameters)

    # fit model on X train and y_train 
    model.fit(X_train,y_train)

    logging.info(f"{model_name} trained successfully")
                 
    return model




# Create small sample dataset
data = pd.DataFrame({
    "feature1": [1, 2, 3, 4, 5],
    "feature2": [5, 4, 3, 2, 1],
    "target":   [0, 0, 1, 1, 1]
})


# Split features and target
X_train = data[["feature1", "feature2"]]
y_train = data["target"]


# Train model
model = train_model(
    X_train,
    y_train,
    model_name="logistic_regression",
    hyperparameters={
        "penalty": "l2",
        "C": 1.0,
        "solver": "lbfgs",
        "max_iter": 1000
    }
)


# Print model
print(model)
predictions = model.predict(X_train)

print("Predictions:", predictions)

# -----------------------

def save_model(model, model_path: str, metadata: dict):
    """
    Save trained model and metadata to disk.

    Args:
        model: trained machine learning model
        model_path: path where model should be saved
        metadata: dictionary containing model metadata
    """

    # create dictionary if missing 
    os.makedirs(os.path.dirname(model_path), exist_ok=True)

    # # serialise model to disk
    joblib.dump(model,model_path)

    # build metadata file path 
    metadata_path = model_path.replace(".pkl","_metadata.json")

    # save metadata file 
    with open(metadata_path,"w") as f:
        json.dump(metadata,f,indent=4)

    # LOG model save success
    logging.info(f"Model saved successfully at: {model_path}")
    logging.info(f"Metadata saved successfully at: {metadata_path}")

