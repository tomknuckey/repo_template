import pandas as pd
from sklearn.metrics import root_mean_squared_error, r2_score
from typing import List
import matplotlib.pyplot as plt

def evaluate_model_groups(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate R² and RMSE grouped by model_run_date, model_type, and version.

    Parameters:
    df (pd.DataFrame): DataFrame with actual and predicted values.

    Returns:
    pd.DataFrame: Grouped metrics.
    """
    grouped = df.groupby(["model_run_date", "model_type", "version", "features_used"])

    results = []
    for group_keys, group_df in grouped:
        r2 = r2_score(group_df["actual_value"], group_df["predicted_value"])
        rmse = root_mean_squared_error(group_df["actual_value"], group_df["predicted_value"])

        results.append({
            "model_run_date": group_keys[0],
            "model_type": group_keys[1],
            "version": group_keys[2],
            "features_used": group_keys[3],
            "feature_count": len(group_keys[3].split(",")),
            "r2_score": r2,
            "rmse": rmse
        })

    return pd.DataFrame(results).sort_values("r2_score", ascending=False)


def plot_feature_importance(model, features: List[str], plot_mode, top_n: int = 20) -> None:
    """
    Plots the top N feature importances from a trained tree-based model.

    Args:
        model (BaseEstimator): Trained model with `feature_importances_` attribute.
        features (List[str]): List of feature names.
        top_n (int): Number of top features to display (default 10).
    """

    if plot_mode:
        importances = pd.Series(model.feature_importances_, index=features)
        top_features = importances.sort_values(ascending=False).head(top_n)

        plt.figure(figsize=(8, 6))
        top_features.plot(kind='barh')
        plt.title(f"Top {top_n} Feature Importances")
        plt.xlabel("Importance")
        plt.gca().invert_yaxis()
        plt.show()

        return importances.sort_values(ascending=False)