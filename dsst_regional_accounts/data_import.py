import pandas as pd 
import yaml

def load_config(yaml_path: str):

    with open(yaml_path, 'r') as f:
        return yaml.safe_load(f)

def load_data(input_path: str, sheet_name: str, delete_rows: int) -> pd.DataFrame:
    """
    Reads in the input file (excel) into a pd.DataFrame

    Parameters:
        input_path (str): location of input file.
        sheet_name (str): name of the excel sheet to read in. 
        delete_rows (int): number of empty rows at the top of the file. 

    Returns:
        pd.DataFrame: input data as df.
    """
    
    return pd.read_excel(input_path, sheet_name=sheet_name, 
                            skiprows=delete_rows)
