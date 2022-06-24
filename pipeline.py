""" Run DSST Regional Accounts project. """
import pandas as pd 

# Define empty rows at the top of the spreadsheet to exclude
emptyrows = list(range(0,6))

# Import data 
input_file_P1 = pd.read_excel(r"C:\Users\murrec\DSST\Input P1 AND P2.xlsx", sheet_name="P1", skiprows=emptyrows)
input_file_P2 = pd.read_excel(r"C:\Users\murrec\DSST\Input P1 AND P2.xlsx", sheet_name="P2")

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

start_year = 1997
end_year = 2021

years = create_years(start_year, end_year)

def P_calculation(df, file):
    df = df.groupby(by = "SIC_code").agg(years)

    # Add back in a total column
    df = df.append(df.sum().rename('Total'))

    # Ensure industry code is a column and not the index 
    df.reset_index(inplace=True)

    #df["Transaction"] = file 
    df.insert(0, "Transaction", file)

    return df
    
output_file_P1 = P_calculation(input_file_P1, "P.1")
output_file_P2 = P_calculation(input_file_P2, "P.2")

with pd.ExcelWriter(r"C:\Users\murrec\DSST\Python Output P1_P2_RA_BB21.xlsx") as writer:
    output_file_P1.to_excel(writer, sheet_name="P1_RA_BB21", index=False)
    output_file_P2.to_excel(writer, sheet_name="P2_RA_BB21", index=False)