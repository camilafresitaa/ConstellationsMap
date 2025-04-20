import numpy as np
import math
from stars.bsc_parser import read_bsc_file


def angular_distance(ra1, dec1, ra2, dec2):
    """
    Compute angular distance between two coordinates: (ra1, dec1) and (ra2, dec2) in degrees.
    This uses the spherical law of cosines.
    """
    ra1, ra2 = math.radians(ra1), math.radians(ra2)
    dec1, dec2 = math.radians(dec1), math.radians(dec2)

    cos_angle = math.sin(dec1)*math.sin(dec2) + math.cos(dec1)*math.cos(dec2)*math.cos(ra1 - ra2)
    
    return math.degrees(math.acos(min(1, max(-1, cos_angle))))


def convert_to_2d(ra_deg, dec_deg, RA0, Dec0):
    """
    Project (RA, Dec) onto a 2D plane using stereographic projection centered at (RA0, Dec0).
    """
    # Convert all angles to radians
    ra = math.radians(ra_deg)
    dec = math.radians(dec_deg)
    ra0 = math.radians(RA0)
    dec0 = math.radians(Dec0)

    # Angular distance between star and center
    cos_c = math.sin(dec0)*math.sin(dec) + math.cos(dec0)*math.cos(dec)*math.cos(ra - ra0)
    c = math.acos(min(1, max(-1, cos_c)))   # Clamp for safety

    if c == 0:
        return 0, 0

    # Stereographic projection formula
    k = 2 / (1 + cos_c)
    x = k * math.cos(dec) * math.sin(ra - ra0)
    y = k * (math.cos(dec0)*math.sin(dec) - math.sin(dec0)*math.cos(dec)*math.cos(ra - ra0))
    
    return x, y


def add_homogeneous_coord(x, y):
    """
    Add homogeneous coordinate to (x, y), returning [x, y, 1].
    This enables matrix-based transformations.
    """
    return np.array([x, y, 1])


def stars_coords():
    """
    Load star data and project to 2D space using stereographic projection.
    Also compute homogeneous coordinates for matrix transformation support.

    Returns:
    - List of stars with projected coordinates and homogeneous form.
    """
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

        # Optional radial stretch to spread dense central region outward.
        # This improves visual clarity by making the center less cluttered.
        r = math.sqrt(x**2 + y**2)
        r_max = 10
        stretch_factor = 3

        # Calculate stretch factor: closer points are stretched more.
        stretch = 1 + (1 - min(r / r_max, 1)) * stretch_factor
        x *= stretch
        y *= stretch

        # Store transformed coordinates and homogeneous form
        star["x"] = x
        star["y"] = y
        star["Homogeneous"] = add_homogeneous_coord(x, y)
        stars_2d.append(star)

    return stars_2d, RA0, Dec0