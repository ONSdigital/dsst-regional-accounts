""" Run DSST Regional Accounts project. """
import pandas as pd
#from dsst_regional_accounts.P1_P2 import pre_processing
from p1_p2 import run_p1_p2

from data_import import (
    load_config, 
    load_data, 
    export_data_p1_p2
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
    run_p1_p2(config)
    return None

if __name__=='__main__':

    config_path = "config\config.yaml"

    df = run(config_path)

