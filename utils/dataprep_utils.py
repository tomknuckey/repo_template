import pandas as pd
import numpy as np


def with_date_features(pdf: pd.DataFrame) -> pd.DataFrame:
    """
    Adds date-based features to a DataFrame, including year, month, weekday,
    and a weekend flag.

    Args:
        pdf (pd.DataFrame): DataFrame containing a 'date' column.

    Returns:
        pd.DataFrame: DataFrame with additional date-related columns.
    """
    pdf["Date"] = pd.to_datetime(pdf["Date"])
    pdf["Month"] = pdf["Date"].dt.month
    pdf["Year"] = pdf["Date"].dt.year
    pdf["Quarter"] = ((pdf["Month"] - 1) // 3) + 1

    return pdf


def prepare_election_date(election_dates):
    """
    This generates a dataframe from a list of election dates with year and election number in that year.
    """

    df = pd.DataFrame({"Date": election_dates})
    df["Date"] = pd.to_datetime(df["Date"])

    df["Year"] = df["Date"].dt.year
    df["election_number_year"] = df.groupby("Year").cumcount() + 1

    return df


def prepare_election_results():
    """
    This gets the election results for the UK from the main results dataframe and pivots it to have parties as columns.
    """
    pdf = pd.read_csv("data/input/election_results/general_election_results.csv")

    # TODO - Make this more flexible for choosing parties
    pdf_filtered = (
        pdf.query("Geography == 'UK'")
        .query("Party in ['Conservative', 'Labour', 'Liberal Democrats']")[
            ["Year", "Party", "Seats"]
        ]
        .pivot(index="Year", columns="Party", values="Seats")
        .reset_index()
    )

    # TODO - handle 1975 anomaly where there's two elections in a config
    pdf_filtered["Year"] = np.where(
        pdf_filtered["Year"] == 1975, 1974, pdf_filtered["Year"]
    )

    pdf_filtered["election_number_year"] = pdf_filtered.groupby("Year").cumcount() + 1

    pdf_filtered["Election_Flag"] = 1

    return pdf_filtered


def with_polling_stats(pdf, election_cols):
    """
    Add polling-related stats to the dataframe.
    """

    # Ensure Date column is datetime
    pdf["Date"] = pd.to_datetime(pdf["Date"])

    # Identify incumbent party each day
    pdf["Incumbent"] = pdf[election_cols].idxmax(axis=1)

    # Start date of current incumbent (most recent takeover)
    # Compute on a date-sorted temporary DF so shift() reflects chronological order,
    # then align the result back to the original dataframe to preserve row order.
    tmp = pdf.sort_values("Date").copy()
    tmp["Incumbent_Change"] = tmp["Incumbent"] != tmp["Incumbent"].shift(1)
    tmp["Incumbent_Start_Date"] = tmp["Date"].where(tmp["Incumbent_Change"]).ffill()
    # If Incumbent is missing for a row, ensure start date is NaT
    tmp.loc[tmp["Incumbent"].isna(), "Incumbent_Start_Date"] = pd.NaT
    pdf["Incumbent_Start_Date"] = tmp["Incumbent_Start_Date"]

    # Duration (days since incumbent started)
    pdf["Incumbent_Duration_Days"] = (pdf["Date"] - pdf["Incumbent_Start_Date"]).dt.days

    # Conservative polling lead
    pdf["Conservative_Lead"] = pdf["Conservative_polling"] - pdf["Labour_polling"]

    # Incumbent_Win logic:
    # If Conservatives are incumbent → use lead
    # If Labour is incumbent → negative of Conservative lead
    pdf["Incumbent_Win"] = np.where(
        pdf["Incumbent"] == "Conservative_election",
        pdf["Conservative_Lead"],
        -pdf["Conservative_Lead"],
    )

    return pdf


def with_quarter_year_comparison(pdf, col_name):

    pdf[f"{col_name}_QoQ"] = pdf[col_name].pct_change()
    pdf[f"{col_name}_YoY"] = pdf[col_name].pct_change(4)

    return pdf


def prepare_polling():
    pdf_polling = pd.read_csv("data/input/polling/polling_average.csv")[
        ["Date", "Conservative", "Labour", "Liberal Democrats"]
    ]

    pdf_polling["Date"] = pd.to_datetime(pdf_polling["Date"])
    pdf_polling["Polling_Flag"] = 1

    return pdf_polling

def add_event_flag(
    pdf: pd.DataFrame,
    start: str,
    end: str,
    flag_name: str,
) -> pd.DataFrame:
    """
    Add a binary event flag column based on a date range.
    """
    pdf[flag_name] = (
        (pdf["Date"] >= pd.Timestamp(start)) &
        (pdf["Date"] <= pd.Timestamp(end))
    ).astype(int)
    return pdf
