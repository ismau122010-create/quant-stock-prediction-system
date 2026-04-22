import logging
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    confusion_matrix
)

logging.basicConfig(level=logging.INFO)


def evaluate_classification_model(y_true, y_pred, y_prob=None):
    """
    Evaluate classification model performance.

    Args:
        y_true: actual labels
        y_pred: predicted labels
        y_prob: probability predictions (optional)

    Returns:
        dictionary containing evaluation metrics
    """

    results = {}

    # Calculate accuracy
    results["accuracy"] = accuracy_score(y_true,y_pred)

    # calculate precision 
    results["precision"] = precision_score(y_true,y_pred)

    # calculare recall 
    results["recall"] = recall_score(y_true,y_pred)

    # calculate F1 score 
    results["f1_score"] = f1_score(y_true,y_pred)

    # if y_prob is available: calculate ROC AUC 
    if y_prob is not None:
        results["roc_auc"] = roc_auc_score(y_true,y_prob)
    else:
        results["roc_auc"] = None

    # calculate confusion metrix 
    results ["confusion_metrix"] = confusion_matrix(y_true,y_pred)

    logging.info("model evaluation completed successfully")

    return results


if __name__ == "__main__":

    # Example real values
    y_true = [1, 0, 1, 1, 0]

    # Example predicted values
    y_pred = [1, 0, 0, 1, 1]

    # Example prediction probabilities
    y_prob = [0.85, 0.22, 0.40, 0.77, 0.63]

    results = evaluate_classification_model(y_true, y_pred, y_prob)

    print(results)

