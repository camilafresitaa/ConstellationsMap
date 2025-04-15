import pandas as pd

def read_constellations(filepath):
    """
    Reads the constellations dataset from a CSV file.

    Parameters:
        filepath (str): Path to the constellations CSV file.

    Returns:
        DataFrame: A pandas DataFrame containing the constellations data.
    """

    try:
        df = pd.read_csv(filepath)
        return df
    except FileNotFoundError:
        print(f"File {filepath} not found.")
        return None
    except pd.errors.EmptyDataError:
        print("File is empty.")
        return None
    except pd.errors.ParserError as e:
        print(f"Error parsing the file: {e}")
        return None
    

def main():
    filepath = "ConstellationsMap/data/constellations.csv"
    constellations_df = read_constellations(filepath)

    if constellations_df is not None:
        # Display the first rows to verify that it has been read correctly
        print(constellations_df.head())


if __name__ == "__main__":
    main()
