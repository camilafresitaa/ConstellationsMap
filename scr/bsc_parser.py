def parse_catalog_line(line):
    """
    Parse a catalog line and extract the relevant fields.

    Parameters:
        line (str): The catalog line to parse.

    Returns:
        dict: Dictionary containing the extracted fields (HR, Name, RA_J2000, Dec_J2000, Vmag).    
    """

    if len(line) < 107:
        raise ValueError("Line does not meet the minimum required length.")
    
    HR = line[0:4].strip()
    Name = line[4:14].strip()
    RAh = line[75:77].strip()
    RAm = line[77:79].strip()
    RAs = line[79:83].strip()
    DEsign = line[83:84].strip()
    DEd = line[84:86].strip()
    DEm = line[86:88].strip()
    DEs = line[88:90].strip()
    Vmag = line[102:107].strip()

    RA_J2000 = f"{RAh} {RAm} {RAs}"
    Dec_J2000 = f"{DEsign}{DEd}° {DEm}' {DEs}''"

    return {
        "HR": HR,
        "Name": Name,
        "RA_J2000": RA_J2000,
        "Dec_J2000": Dec_J2000,
        "Vmag": Vmag
    }


def read_bsc_file(filepath):
    """
    Read the catalog file and process each line to extract star information.

    Parameters:
        filepath (str): Path to the data file.

    Returns:
        list: List of dictionaries with information for each star.
    """

    stars = []
    try:
        with open(filepath, "r") as file:
            for line in file:
                if not line.strip():
                    continue
                try:
                    star = parse_catalog_line(line)
                    stars.append(star)
                except ValueError as e:
                    print(f"Error parsing line: {e}")
    except FileNotFoundError:
        print(f"File {filepath} not found.")

    return stars


def main():
    filepath = "data/ybsc5"
    stars = read_bsc_file(filepath)

    # Display the first 5 records to verify
    for star in stars[:5]:
        print(star)


if __name__ == "__main__":
    main()