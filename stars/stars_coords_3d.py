import numpy as np
import math
from stars.bsc_parser import read_bsc_file


def sph_to_cart(ra_deg: float, dec_deg: float, dist: float = 1.0):
    """
    Convert spherical coordinates (RA, Dec in degrees) to 3D Cartesian coordinates on a unit sphere.
    
    Given RA (a) and Dec (δ) in radians, the conversion to cartesian is:
        x = dist * cos(δ) * cos(a)
        y = dist * cos(δ) * sin(a)
        z = dist * sin(δ)
    where dist is the distance from the origin.

    Parameters:
        ra_deg (float): Right Ascension in degrees.
        dec_deg (float): Declination in degrees.
        dist (float): Distance to the star (default 1.0 for unit sphere).

    Returns:
        numpy.ndarray: Homogeneous 4D vector [x, y, z, 1].
    """
    ra = math.radians(ra_deg)
    dec = math.radians(dec_deg)
    x = dist * math.cos(dec) * math.cos(ra)
    y = dist * math.cos(dec) * math.sin(ra)
    z = dist * math.sin(dec)
    return np.array([x, y, z, 1.0])


def stars_coords_3d():
    """
    Return a list of stars with 3D homogeneous coordinates.

    Each star dict will include:
      - HR, Name, RA_J2000, Dec_J2000, Vmag (from parser)
      - x, y, z: Cartesian coordinates
      - Homogeneous: numpy.ndarray [x, y, z, 1]

    Returns:
        list: List of star dictionaries with added 3D coordinates.
    """
    filepath = "data/ybsc5"
    stars_raw = read_bsc_file(filepath)
    stars_3d = []
    for star in stars_raw:
        # Compute 4D homogeneous coordinate
        v = sph_to_cart(star["RA_deg"], star["Dec_deg"], star.get("dist", 1.0))
        # Unpack Cartesian components
        x, y, z,_ = v
        star["x"] = x
        star["y"] = y
        star["z"] = z
        star["homogeneous"] = v
        stars_3d.append(star)
    return stars_3d
