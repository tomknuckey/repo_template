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


def create_combined_output():

    pdf_output_header = pd.read_csv("data/output/header_output.csv")
    pdf_output_detail = pd.read_csv("data/output/detail_output.csv")


    return pdf_output_header.merge(pdf_output_detail, on="model_output_id")