import numpy as np
import math
from stars.bsc_parser import read_bsc_file


def convert_to_2d(ra_deg, dec_deg, RA0, Dec0):
    """
    Convert spherical coordinates (RA, Dec in degrees) to 2D Cartesian coordinates
    using an equirectangular projection.

    Parameters:
        ra_deg (float): Right Ascension in degrees.
        dec_deg (float): Declination in degrees.
        RA0 (float): Reference Right Ascension in degrees (center of the map).
        Dec0 (float): Reference Decliantion in degrees (center of the map).

    Returns:
        tuple: (x, y) coordinates in 2D.        
    """

    # Adjust the x coordinate by the cosine of the central declination (reduce distortion)
    x = (ra_deg - RA0) * math.cos(math.radians(Dec0))

    # y coordinate is simply the difference in declination
    y = dec_deg - Dec0

    return x, y


def add_homogeneous_coord(x, y):
    """
    Convert 2D Cartesian coordinates to homogeneous coordinates [x, y, 1].

    Parameters:
        x (float): x-coordinate.
        y (float): y-coordinate.

    Returns:
        numpy.array: Homogeneous coordinate as a 3-element vector.
    """

    return np.array([x, y, 1])


def stars_coords():
    filepath = "data/ybsc5"
    stars = read_bsc_file(filepath)

    # Use the RA_deg and Dec_deg returned by the parser
    ra_list = []
    dec_list = []
    for star in stars:
        ra_list.append(star["RA_deg"])
        dec_list.append(star["Dec_deg"])

    # Calculate the center of the map (RA0, Dec0) as the average values of the star catalog
    RA0 = sum(ra_list) / len(ra_list)
    Dec0 = sum(dec_list) / len(dec_list)

    # Process each star: convert spherical coordinates to 2D and then compute homogeneous coordinates
    stars_2d = []
    for star in stars:
        x, y = convert_to_2d(star["RA_deg"], star["Dec_deg"], RA0, Dec0)
        star["x"] = x
        star["y"] = y
        # Add homogeneous coordinate representation [x, y, 1] 
        star["Homogeneous"] = add_homogeneous_coord(x, y)
        stars_2d.append(star)

    return stars_2d

    # Display the first 5 stars with their 2D and homogeneous coordinates for verification
    print("First 5 stars with 2D coordinates (x, y) and homogeneous coordinates:")
    for star in stars_2d[:5]:
        print(f"{star["HR"]}: x = {star["x"]}, y = {star["y"]}, Homogeneous = {star['homogeneous']}")


# if __name__ == "__main__":
#     stars_coords()