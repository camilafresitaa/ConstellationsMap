from constellations.constellations_parser import read_constellations
from stars.stars_coords_2d import angular_distance

MAX_ANGULAR_DISTANCE = 150  # Maximum angular distance (in degrees) from center for visibility

class Constellation():
    """
    Represents a constellation, defined by a sequence of HR star numbers.

    Attributes:
        name (str): Name of the constellation.
        hr_sequence (list of int): List of HR numbers defining the shape.
        stars (list): Populated later with actual Star objects.
    """
    def __init__(self, name, hr_sequence):
        self.name = name
        self.hr_sequence = hr_sequence
        self.stars = []  # Will hold Star instances after binding

    def __repr__(self):
        return (f"Constellation {self.name}: ({self.hr_sequence})")

    def bind_stars(self, star_lookup, RA0=None, Dec0=None):
        """
        Populate self.stars with actual Star instances from a lookup dictionary.
        Optionally filters stars based on angular distance from a center point.

        Paramenters:
            star_lookup (dict): Dictionary mapping HR number to Star object.
            RA0 (float): Optional RA center (for filtering)
            Dec0 (float): Optional Dec center (for filtering)
        """
        self.stars = []
        total_expected = len(self.hr_sequence)

        for hr in self.hr_sequence:
            star = star_lookup.get(hr)
            if star:
                if RA0 is not None and Dec0 is not None:
                    # Optionally filter stars by angular distance to avoid clutter
                    ad = angular_distance(star.ra_deg, star.dec_deg, RA0, Dec0)
                    if ad > MAX_ANGULAR_DISTANCE:
                        continue
                self.stars.append(star)

        # Invalidate constellation if any star couldn't be matched
        if len(self.stars) != total_expected:
            self.stars = []


def load_constellations(star_lookup, RA0=None, Dec0=None):
    """"
    Load constellation definitions and attach corresponding Star instances.

    Parameters:
        star_lookup (dict): Dictionary mapping HR numbers to Star instances.
        RA0, Dec0 (float): Optional center coordinates for filtering.

    Returns:
        list: List of Constellation instances with stars bound.
    """
    raw_list = read_constellations()
    constellations = []

    for entry in raw_list:
        name = entry["Name"]
        hr_seq = entry["HR_sequence"]
        c = Constellation(name, hr_seq)
        c.bind_stars(star_lookup, RA0, Dec0)
        constellations.append(c)

    return constellations