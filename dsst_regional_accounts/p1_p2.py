import pandas as pd
from helper import create_years_sum

from data_import import (
    load_data, 
    export_data_p1_p2
)

def run_p1_p2(config: str):
    
    df_1 = load_data(
        config["input_data"]["input_path"], 
        "P1", 
        config["input_data"]["P1_delete_top_rows"]
    )
    df_2 = load_data(
        config["input_data"]["input_path"], 
        "P2", 
        config["input_data"]["P2_delete_top_rows"]
    )

    df_1 = pre_processing(df_1)
    df_2 = pre_processing(df_2)

    start_year = config["timeseries"]["start_year"]
    end_year = config["timeseries"]["end_year"] 

    years = create_years_sum(start_year, end_year)

    df_1 = P_calculation(df_1, years, "P.1")
    df_2 = P_calculation(df_2, years, "P.2")

    export_data_p1_p2(df_1, df_2, 
        config["output_file"]["output_path"], 
        config["output_file"]["sheet_1_name"], 
        config["output_file"]["sheet_2_name"]
    )

    return None

def pre_processing(df: pd.DataFrame) -> pd.DataFrame:

    """
    Processes the data - renames columns, 
    drops total and aggregate rows (avoid double counting)

    Parameters:
        df (pd.DataFrame): input df.

    Returns:
        df (pd.DataFrame): cleaned df. 
    """
    df.rename(columns={"Unnamed: 0": "tax_code",
        "Unnamed: 1": "sector_code",
        "Unnamed: 2": "SIC_code"}, 
        inplace=True
    )
    df.drop(df[df["SIC_code"]  == "TOTAL"].index, inplace=True)
    invalid = (df["tax_code"]  == "P.13") & (df["sector_code"]  == "S.13")
    df.drop(df[invalid].index, inplace=True)

    return df

def P_calculation(df: pd.DataFrame, 
                    years: dict, tax_code: str) -> pd.DataFrame:
    """
    Aggregates (sum) data based on SIC code. 

    Parameters:
        df (pd.DataFrame): first year of the time series.
        years (dict): (key: year, value: "sum")
        tax_code (str): either P.1 or P.2

    Returns:
        df(pd.DataFrame): output dataframe.
    """
    df = df.groupby(by = "SIC_code").agg(years)

    # Add back in a total row
    df = df.append(df.sum().rename('Total'))

    # Ensure sector code is a column and not the index 
    df.reset_index(inplace=True)

    # Insert tax code column 
    df.insert(0, "Transaction", tax_code)

    return df