def parse_catalog_line(line):
    """
    Parse a single line of the Bright Star Catalog (BSC) and extract fields.

    Parameters:
        line (str): Raw line from the catalog file.

    Returns:
        dict: Parsed star data with keys:
            - HR (str): Harvard Revised number
            - Name (str): Common name (if any)
            - RA_J2000 (str): Right Ascension in h m s format
            - Dec_J2000 (str): Declination in d m s format
            - RA_deg (float): Right Ascension in decimal degrees
            - Dec_deg (float): Declination in decimal degrees
            - Vmag (str): Apparent visual magnitude
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

    # Check that all the necessary fields for RA and Dec are present
    if not (RAh and RAm and RAs and DEd and DEm and DEs):
        return None

    RA_J2000 = f"{RAh} {RAm} {RAs}"
    Dec_J2000 = f"{DEsign}{DEd}° {DEm}' {DEs}''"

    # Convert RA to decimal degrees (1 hour = 15 degrees)
    try:
        RA_deg = (float(RAh) + float(RAm)/60 + float(RAs)/3600) * 15
    except ValueError as e:
        raise ValueError ("Error converting RA to float.") from e

    # Convert Dec to decimal degrees
    sign = 1 if DEsign != "-" else -1
    try:
        Dec_deg = sign * (float(DEd) + float(DEm)/60 + float(DEs)/3600)
    except ValueError as e:
        raise ValueError("Error converting Dec to float.") from e
    
    return {
        "HR": HR,
        "Name": Name,
        "RA_J2000": RA_J2000,
        "RA_deg": RA_deg,
        "Dec_J2000": Dec_J2000,
        "Dec_deg": Dec_deg,
        "Vmag": Vmag
    }


def read_bsc_file(filepath):
    """
    Read the Bright Star Catalog file and extract data for each line.

    Parameters:
        filepath (str): Path to the catalog file.

    Returns:
        list: List of star dictionaries parsed from the file.
    """
    stars = []
    try:
        with open(filepath, "r") as file:
            for line in file:
                if not line.strip():
                    continue
                try:
                    star = parse_catalog_line(line)
                    if star is not None:
                        stars.append(star)
                    else:
                        continue
                except ValueError as e:
                    print(f"Error parsing line: {e}")
    except FileNotFoundError:
        print(f"File {filepath} not found.")

    return stars