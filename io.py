def load_config(yaml_path: str):

    """

    """

    with open(yaml_path, 'r') as f:
        return yaml.safe_load(f)

def load_data(input_path: str, sheet_name: str, delete_rows: int):
    df = pd.read_excel(input_path, sheet_name=sheet_name, skiprows=delete_rows)

    return df

def export_data(P1, P2, output_path, sheet_name_1, sheet_name_2):
    with pd.ExcelWriter(output_path) as writer:
        P1.to_excel(writer, sheet_name = sheet_name_1, index=False)
        P2.to_excel(writer, sheet_name = sheet_name_2, index=False)

    return None