import pandas as pd
from statsmodels.stats.outliers_influence import variance_inflation_factor
import seaborn as sns
import matplotlib.pyplot as plt
from pandas import DataFrame
from sklearn.tree import DecisionTreeRegressor, plot_tree
from typing import List

def check_collinearity(X: pd.DataFrame, show_corr_heatmap: bool = True) -> pd.DataFrame:
    """
    Checks collinearity of the features in X using VIF and optionally shows a correlation heatmap.

    Args:
        X: DataFrame of numeric features (with or without constant column).
        show_corr_heatmap: Whether to display a heatmap of the correlation matrix.

    Returns:
        DataFrame with VIF values for each feature.
    """
    # Ensure all columns are numeric
    X_numeric = X.apply(pd.to_numeric, errors="coerce")

    # Compute VIF
    vif_data = pd.DataFrame()
    vif_data["feature"] = X_numeric.columns
    vif_data["VIF"] = [
        variance_inflation_factor(X_numeric.values, i)
        for i in range(X_numeric.shape[1])
    ]

    # Print sorted VIF
    print("\nVariance Inflation Factors:")
    print(vif_data.sort_values("VIF", ascending=False))

    # Optional: correlation heatmap
    if show_corr_heatmap:
        corr_matrix = X_numeric.corr()
        plt.figure(figsize=(12, 8))
        sns.heatmap(corr_matrix, annot=True, fmt=".2f", cmap="coolwarm", center=0)
        plt.title("Correlation Matrix of Features")
        plt.show()

    return vif_data

def plot_basic_decision_tree(
    pdf_train: DataFrame,
    features: List[str],
    target: str,
    max_depth: int = 4,
):
    """
    Trains a DecisionTreeRegressor on the given dataset and plots the resulting tree.
    This helps to visualize how a basic decision tree model makes predictions based on the features.

    Args:
        pdf_train (pd.DataFrame): Training dataset containing features and target.
        features (List[str]): List of feature column names.
        target (str): Target column name.
        max_depth (int, optional): Maximum depth of the tree. Defaults to 4.
        random_state (int, optional): Random seed for reproducibility. Defaults to 42.

    """
    # Train the model
    tree_model = DecisionTreeRegressor(max_depth=max_depth, random_state=42)
    tree_model.fit(pdf_train[features], pdf_train[target])

    # Plot the tree
    plt.figure(figsize=(24, 16))
    plot_tree(
        tree_model,
        feature_names=features,
        filled=True,
        rounded=True,
        fontsize=10
    )
    plt.show()
