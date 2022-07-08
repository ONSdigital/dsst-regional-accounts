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


def export_data(P1: pd.DataFrame, P2: pd.DataFrame, output_path: str,
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