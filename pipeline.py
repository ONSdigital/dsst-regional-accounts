""" Run DSST Regional Accounts project. """
import pandas as pd 
import yaml 

def load_config(yaml_path: str):

    """

    """

    with open(yaml_path, 'r') as f:
        return yaml.safe_load(f)


def run(config_path)-> pd.DataFrame:
    """

    """
    config = load_config(config_path)

    df_1 = load_data(config["input_data"]["input_path"], "P1", config["input_data"]["P1_delete_top_rows"])
    df_2 = load_data(config["input_data"]["input_path"], "P2", config["input_data"]["P2_delete_top_rows"])

    df_1 = pre_processing(df_1)
    df_2 = pre_processing(df_2)

    start_year = config["timeseries"]["start_year"]
    end_year = config["timeseries"]["end_year"] + 1

    years = create_years(start_year, end_year)

    df_1 = P_calculation(df_1, years, "P.1")
    df_2 = P_calculation(df_2, years, "P.2")

    export_data(df_1, df_2, config["output_file"]["output_path"], config["output_file"]["sheet_1_name"], config["output_file"]["sheet_2_name"])
 
    return df_1, df_2

def load_data(input_path, sheet_name, delete_rows):
    df = pd.read_excel(input_path, sheet_name=sheet_name, skiprows=delete_rows)

    return df

def pre_processing(df):
    df.rename(columns={"Unnamed: 0": "tax_code",
                   "Unnamed: 1": "industry_code",
                   "Unnamed: 2": "SIC_code"}, inplace=True)
    df.drop(df[df["SIC_code"]  == "TOTAL"].index, inplace=True)
    df.drop(df[(df["tax_code"]  == "P.13") & (df["industry_code"]  == "S.13")].index, inplace=True)

    return df 


def create_years(start_year, end_year):
    # Create a list of years 
    years = list(range(start_year, end_year))

    # Create a dictionary with years as key and "sum" as value as we want to sum each column 
    years_dict = {}
    for year in years:
        years_dict[year] = "sum"
    print(years_dict)

    return years_dict


def P_calculation(df, years, file):
    df = df.groupby(by = "SIC_code").agg(years)

    # Add back in a total column
    df = df.append(df.sum().rename('Total'))

    # Ensure industry code is a column and not the index 
    df.reset_index(inplace=True)

    df.insert(0, "Transaction", file)

    return df

def export_data(P1, P2, output_path, sheet_name_1, sheet_name_2):
    with pd.ExcelWriter(output_path) as writer:
        P1.to_excel(writer, sheet_name = sheet_name_1, index=False)
        P2.to_excel(writer, sheet_name = sheet_name_2, index=False)
    
    return None
    
if __name__=='__main__':

    config_path = "config\config.yaml"

    df = run(config_path)

