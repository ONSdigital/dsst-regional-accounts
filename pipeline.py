""" Run DSST Regional Accounts project. """
import pandas as pd 
import yaml 

def load_config(yaml_path: str):

    """

    """

    with open(yaml_path, 'r') as f:
        return yaml.safe_load(f)

config = load_config("config\config.yaml")

# Define empty rows at the top of the spreadsheet to exclude
emptyrows = list(range(config["input_data"]["start_empty_rows"],config["data"]["end_empty_rows"]))

# Import data 
input_file_P1 = pd.read_excel(config["input_data"]["input_path"], sheet_name="P1", skiprows=emptyrows)
input_file_P2 = pd.read_excel(config["input_data"]["input_path"], sheet_name="P2")

def pre_processing(df):
    df.rename(columns={"Unnamed: 0": "tax_code",
                   "Unnamed: 1": "industry_code",
                   "Unnamed: 2": "SIC_code"}, inplace=True)
    df.drop(df[df["SIC_code"]  == "TOTAL"].index, inplace=True)

    return df 

input_file_P1 = pre_processing(input_file_P1)
input_file_P2 = pre_processing(input_file_P2)

def create_years(start_year, end_year):
    # Create a list of years 
    years = list(range(start_year, end_year))

    # Create a dictionary with years as key and "sum" as value as we want to sum each column 
    years_dict = {}
    for year in years:
        years_dict[year] = "sum"
    print(years_dict)

    return years_dict

start_year = config["timeseries"]["start_year"]
end_year = config["timeseries"]["end_year"]

years = create_years(start_year, end_year)

def P_calculation(df, file):
    df = df.groupby(by = "SIC_code").agg(years)

    # Add back in a total column
    df = df.append(df.sum().rename('Total'))

    # Ensure industry code is a column and not the index 
    df.reset_index(inplace=True)

    df.insert(0, "Transaction", file)

    return df
    
output_file_P1 = P_calculation(input_file_P1, "P.1")
output_file_P2 = P_calculation(input_file_P2, "P.2")

with pd.ExcelWriter(config["output_file"]["output_path"],) as writer:
    output_file_P1.to_excel(writer, sheet_name=config["output_file"]["sheet_1_name"], index=False)
    output_file_P2.to_excel(writer, sheet_name=config["output_file"]["sheet_2_name"], index=False)