""" Run DSST Regional Accounts project. """
import pandas as pd 
import yaml 
from dsst_regional_accounts.io import *

def run(config_path: str)-> pd.DataFrame:
    """
    Runs all necessary functions to create and export output file.

    Parameters:
        config_path (str): path for config.yaml.

    Returns:
        None: pd.DataFrames exported to excel file.

    """ 

    config = io.load_config(config_path)

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

    years = create_years(start_year, end_year)

    df_1 = P_calculation(df_1, years, "P.1")
    df_2 = P_calculation(df_2, years, "P.2")

    export_data(df_1, df_2, 
        config["output_file"]["output_path"], 
        config["output_file"]["sheet_1_name"], 
        config["output_file"]["sheet_2_name"]
    )
 
    return None

def load_data(input_path: str, sheet_name: str, 
                delete_rows: int) -> pd.DataFrame:
    """
    Reads in the input excel file into a pd.DataFrame

    Parameters:
        input_path
        sheet_name
        delete_rows

    Returns:
        pd.DataFrame
    """
    
    return pd.read_excel(input_path, sheet_name=sheet_name, 
                            skiprows=delete_rows)

def pre_processing(df: pd.DataFrame) -> pd.DataFrame:
    df.rename(columns={"Unnamed: 0": "tax_code",
                    "Unnamed: 1": "sector_code",
                    "Unnamed: 2": "SIC_code"}, inplace=True)
    df.drop(df[df["SIC_code"]  == "TOTAL"].index, inplace=True)
    invalid = (df["tax_code"]  == "P.13") & (df["industry_code"]  == "S.13")
    df.drop(df[invalid].index, inplace=True)

    return df


def create_years(start_year: int, end_year: int) -> dict:
    # Create a list of years inclusive of end year. 
    years_list = list(range(start_year, end_year + 1))

    # Create a dictionary (key: years,  value: "sum") - sum each column 
    years_dict = {}
    for year in years_list:
        years_dict[year] = "sum"
    print(years_dict)

    return years_dict


def P_calculation(df: pd.DataFrame, 
                    years: dict, file: str) -> pd.DataFrame:
    df = df.groupby(by = "SIC_code").agg(years)

    # Add back in a total row
    df = df.append(df.sum().rename('Total'))

    # Ensure industry code is a column and not the index 
    df.reset_index(inplace=True)

    df.insert(0, "Transaction", file)

    return df

def export_data(P1: pd.DataFrame, P2: pd.DataFrame, output_path: str,
                sheet_name_1: str, sheet_name_2: str):
    with pd.ExcelWriter(output_path) as writer:
        P1.to_excel(writer, sheet_name = sheet_name_1, index=False)
        P2.to_excel(writer, sheet_name = sheet_name_2, index=False)
    
    return None
    
if __name__=='__main__':

    config_path = "config\config.yaml"

    df = run(config_path)

