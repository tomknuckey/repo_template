import pandas as pd
from statsmodels.stats.outliers_influence import variance_inflation_factor
import seaborn as sns
import matplotlib.pyplot as plt


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
