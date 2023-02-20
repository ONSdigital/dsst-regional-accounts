import pandas as pd
import os
from helper import create_years_sum

from data_import import load_data 

def export_data_p1_p2(P1: pd.DataFrame, P2: pd.DataFrame, output_path: str,
                sheet_name_1: str, sheet_name_2: str):
    """
    Exports df_1 and df_2 to excel file.

    Parameters:
        P1 (pd.DataFrame): df with P.1 data.
        P2 (pd.DataFrame): df with P.2 data.
        output_path (str): file path to save excel document.
        sheet_name_1 (str): name of sheet for P.1 data.
        sheet_name_2 (str): name of sheet for P.2 data  

    Returns:
        None: exports excel file.
    """
    with pd.ExcelWriter(output_path) as writer:
        P1.to_excel(writer, sheet_name = sheet_name_1, index=False)
        P2.to_excel(writer, sheet_name = sheet_name_2, index=False)
    
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

def run_p1_p2(config: str) -> None:
    """
    Runs the main functions to calculate and output the P1_P2 sheet

    Parameters:
        config (str): config.yaml

    Returns:
        None.
    """

    df_1 = load_data(
        config["p1_p2_input_file"]["path"], 
        "P1", 
        config["p1_p2_input_file"]["P1_delete_top_rows"]
    )
    df_2 = load_data(
        config["p1_p2_input_file"]["path"], 
        "P2", 
        config["p1_p2_input_file"]["P2_delete_top_rows"]
    )

    df_1 = pre_processing(df_1)
    df_2 = pre_processing(df_2)

    start_year = config["p1_p2_timeseries"]["start_year"]
    end_year = config["p1_p2_timeseries"]["end_year"] 

    years = create_years_sum(start_year, end_year)

    df_1 = P_calculation(df_1, years, "P.1")
    df_2 = P_calculation(df_2, years, "P.2")

    export_data_p1_p2(df_1, df_2, 
        config["p1_p2_output_file"]["path"], 
        config["p1_p2_output_file"]["sheet_1_name"], 
        config["p1_p2_output_file"]["sheet_2_name"]
    )

    # Get current working directory and add to output file path
    out = os.getcwd() + '\\' + config["p1_p2_output_file"]["path"]

    print("P1_P2 Output data: ", out)

    return None