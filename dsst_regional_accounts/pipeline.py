""" Run DSST Regional Accounts project. """
import pandas as pd 

from data_import import (
    load_config, 
    load_data, 
    export_data
)

def run(config_path: str)-> pd.DataFrame:
    """
    Runs all necessary functions to create and export output file.

    Parameters:
        config_path (str): path for config.yaml.

    Returns:
        None: pd.DataFrames exported to excel file.

    """ 

    config = load_config(config_path)

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


def create_years(start_year: int, end_year: int) -> dict:
    """
    Creates a dictionary (key: year, value: "sum") - sum each year

    Parameters:
        start_year (int): first year of the time series.
        end_year (int): last year to be included.

    Returns:
        years_dict (dict): year with sum operator for aggreagtion. 
    """
    # Create a list of years inclusive of end year. 
    years_list = list(range(start_year, end_year + 1))

    # Create a dictionary (key: years,  value: "sum") - sum each column 
    years_dict = {}
    for year in years_list:
        years_dict[year] = "sum"
    print(years_dict)

    return years_dict


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
    
if __name__=='__main__':

    config_path = "config\config.yaml"

    df = run(config_path)

