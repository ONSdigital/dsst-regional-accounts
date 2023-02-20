""" Run DSST Regional Accounts project. """
import pandas as pd

#from dsst_regional_accounts.P1_P2 import run_p1_p2
from p1_p2 import run_p1_p2
from data_import import load_config

def run(config_path: str)-> pd.DataFrame:
    """
    Runs all necessary functions to create and export output file.

    Parameters:
        config_path (str): path for config.yaml.

    Returns:
        None: pd.DataFrames exported to excel file.

    """
    config = load_config(config_path)

    # Run pipelines
    # TODO: Create console menu to select which sheets to run
    run_p1_p2(config)

    # TODO: Create script to import, process and output the RA_D29_BB22 sheet.
    # Screenshots are avialable of expected output on the DSST Project page

    return None

if __name__=='__main__':

    config_path = "config\config.yaml"

    df = run(config_path)
