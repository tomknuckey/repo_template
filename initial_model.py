import pandas as pd
import plotly.express as px
from sklearn.preprocessing import MinMaxScaler
import statsmodels.api as sm
from sklearn.metrics import mean_absolute_error
from utils.model_utils import check_collinearity

from config import features, target, scale_mode

pdf_all = pd.read_csv("data/intermediate/national_data.csv")

pdf_all = pd.get_dummies(pdf_all, columns=["Incumbent"], drop_first=True, dtype=int)

# Drop rows with missing values in target/features
pdf_all_filtered = pdf_all[[target] + features].dropna(subset=[target] + features)

if scale_mode:
    scaler = MinMaxScaler()
    numeric_cols = pdf_all_filtered.select_dtypes(include=["number"]).columns
    pdf_all_filtered[numeric_cols] = scaler.fit_transform(
        pdf_all_filtered[numeric_cols]
    )

# Prepare X and y
X = pdf_all_filtered[features]
X = sm.add_constant(X, has_constant="add")
y = pdf_all_filtered[target]

vif_table = check_collinearity(X, show_corr_heatmap=True)

# Fit regression
model = sm.OLS(y, X).fit()

predictions = model.predict(X)
results_df = pd.DataFrame(
    {"actual": y, "predicted": predictions, "residual": y - predictions}
).round(2)

mae = mean_absolute_error(y, predictions)

print(model.summary())

px.scatter(
    results_df,
    x="actual",
    y="predicted",
    trendline="ols",
    title=f"Actual vs Predicted (MAE: {mae:.2f})",
)
