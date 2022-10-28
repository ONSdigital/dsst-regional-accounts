def create_years_sum(start_year: int, end_year: int) -> dict:
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