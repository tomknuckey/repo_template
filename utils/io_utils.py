import pandas as pd
import os

def append_to_table(pdf_output: pd.DataFrame, output_path) -> None:

    """
    Appends a DataFrame to a CSV file, creating the file if it doesn't exist.
    """
    # Check if files exist
    output_exists = os.path.isfile(output_path)

    # Append header-level output
    pdf_output.to_csv(output_path, mode="a", index=False, header=not output_exists)