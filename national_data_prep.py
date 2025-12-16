import pandas as pd
import numpy as np
from utils.dataprep_utils import (
    with_date_features,
    prepare_election_date,
    prepare_election_results,
    with_polling_stats,
    with_quarter_year_comparison,
    prepare_polling,
)
from config import election_dates

pdf_election_dates = prepare_election_date(election_dates)

pdf_results = prepare_election_results()

pdf_elections = pdf_results.merge(
    pdf_election_dates, on=["Year", "election_number_year"], how="inner"
).drop(columns=["election_number_year", "Year"])

pdf_polling = prepare_polling()

pdf_polling_elections = pdf_elections.merge(
    pdf_polling, on="Date", suffixes=("_election", "_polling"), how="outer"
).sort_values("Date")

election_cols = [
    "Conservative_election",
    "Labour_election",
    "Liberal Democrats_election",
]

# This forward fills the election results to have the latest election results for each date
pdf_polling_elections[election_cols] = pdf_polling_elections[election_cols].ffill()


pdf_polling_elections = pdf_polling_elections.pipe(
    with_polling_stats, election_cols
).pipe(with_date_features)

pdf_gdp = pd.read_csv("data/input/economic/gdp.csv").pipe(
    with_quarter_year_comparison, "GDP"
)

pdf_inflation = pd.read_csv("data/input/economic/inflation.csv")

pdf_inflation["Quarter"] = ((pdf_inflation["Month"] - 1) // 3) + 1

# Aggregated to get it for each quarter
pdf_inflation = (
    pdf_inflation.groupby(["Year", "Quarter"])
    .agg({"CPI Inflation": "mean"})
    .reset_index()
    .rename(columns={"CPI Inflation": "Inflation"})
    .pipe(with_quarter_year_comparison, "Inflation")
)

pdf_unemployment = pd.read_csv("data/input/economic/unemployment.csv")

pdf_economic = pdf_gdp.merge(
    pdf_inflation[["Year", "Quarter", "Inflation_QoQ", "Inflation_YoY"]],
    on=["Year", "Quarter"],
).merge(pdf_unemployment, how="left", on="Year")

pdf_all = pdf_polling_elections.merge(pdf_economic, how="left", on=["Year", "Quarter"])

pdf_all.to_csv("data/intermediate/national_data.csv", index=False)
