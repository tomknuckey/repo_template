import pandas as pd
def null_check(pdf: pd.DataFrame, cols: list[str]):
    """
    Checks if there are any null values in the specified column of the DataFrame.
    """
    print(f"Checking {cols} are not null")

    assert ~pdf[cols].isnull().values.any(), "There are null columns"