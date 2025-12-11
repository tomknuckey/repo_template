import pandas as pd

def with_date_features(pdf: pd.DataFrame) -> pd.DataFrame:
    """
    Adds date-based features to a DataFrame, including year, month, weekday,
    and a weekend flag.

    Args:
        pdf (pd.DataFrame): DataFrame containing a 'date' column.

    Returns:
        pd.DataFrame: DataFrame with additional date-related columns.
    """
    pdf["date"] = pd.to_datetime(pdf["date"])
    pdf["month"] = pdf["date"].dt.month
    pdf["year"] = pdf["date"].dt.year
    pdf["weekday"] = pdf["date"].dt.weekday
    pdf["weekday_name"] = pdf["date"].dt.day_name()
    pdf["year_month"] = pdf["year"].astype(str) + "_" + pdf["month"].astype(str)
    pdf["weekend_flag"] = pdf["weekday"].isin([5, 6]).astype(int)  # 5=Saturday, 6=Sunday

    return pdf