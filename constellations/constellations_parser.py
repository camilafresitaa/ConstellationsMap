import csv

def read_constellations():
    """
    Read the constellations dataset from a CSV file.

    Expected CSV format per row:
        name, count, HR1, HR2, ..., HRn

    Parameters:
        filepath (str): Path to the constellations CSV file.

    CSV format (one constellation per row):
        name, count, HR1, HR2, ..., HRn

    Returns:
        list: List of dictionaries with keys:
            - "Name" (str): Constellation name
            - "HR_sequence" (list of int): Sequence of HR numbers defining the constellation
    """
    constellations = []
    filepath = "data/constellations.csv"

    try:
        with open(filepath, newline="") as f:
            reader = csv.reader(f)
            for row in reader:
                if not row or len(row) < 2:
                    continue
                name = row[0]
                try:
                    count = int(row[1])
                except ValueError:
                    continue

                hr_seq = []
                for hr in row[2:2 + count]:
                    if hr:
                        try:
                            hr_seq.append(int(hr))
                        except ValueError:
                            continue
    
                constellations.append({"Name": name, "HR_sequence": hr_seq})
    except FileNotFoundError:
        print(f"File {filepath} not found.")

    return constellations