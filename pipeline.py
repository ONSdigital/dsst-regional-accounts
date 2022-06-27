""" Run DSST Regional Accounts project. """
import pandas as pd 
import yaml 

def load_config(yaml_path: str):

    """

    """

    with open(yaml_path, 'r') as f:
        return yaml.safe_load(f)

config = load_config("config\config.yaml")

def run(data, file)-> pd.DataFrame:
    """

    """

    df = pre_processing(data)

    start_year = config["timeseries"]["start_year"]
    end_year = config["timeseries"]["end_year"] + 1

    years = create_years(start_year, end_year)

    df = P_calculation(df, years, file)
 
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
    
if __name__=='__main__':

    data_P1 = pd.read_excel(config["input_data"]["input_path"], sheet_name="P1", skiprows=config["input_data"]["P1_delete_top_rows"])
    print(data_P1)
    data_P2 = pd.read_excel(config["input_data"]["input_path"], sheet_name="P2", skiprows=config["input_data"]["P2_delete_top_rows"])
    P1 = run(data_P1, "P.1")
    P2 = run(data_P2, "P.2")

with pd.ExcelWriter(config["output_file"]["output_path"],) as writer:
        P1.to_excel(writer, sheet_name=config["output_file"]["sheet_1_name"], index=False)
        P2.to_excel(writer, sheet_name=config["output_file"]["sheet_2_name"], index=False)
