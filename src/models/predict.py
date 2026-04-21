import logging


logging.basicConfig(level=logging.INFO)


def generate_predictions(model, X_test):
    """
    Generate predictions from trained model.

    Args:
        model: trained ML model
        X_test: test feature dataset

    Returns:
        y_pred: predicted class labels
        y_prob: probability of positive class (if available), else None
    """

    # Generate class predication 
    y_pred = model.predict(X_test)

    # check if a model supports probability prediction 
    if hasattr(model,"predict_proba"):
        y_prob = model.predict_proba(X_test)[:,1]
    else:
        y_prob = None

    logging.info("predictions generated successfully.")

    return y_pred, y_prob

