from constellations.constellations_parser import read_constellations
from stars.stars_coords_2d import angular_distance

MAX_ANGULAR_DISTANCE = 120

class Constellation():
    """
    A constellation defined by a sequence of star HR numbers.
    """
    def __init__(self, name, hr_sequence):
        self.name = name
        self.hr_sequence = hr_sequence
        self.stars = []

    def __repr__(self):
        return (f"Constellation {self.name}: ({self.hr_sequence})")

    def bind_stars(self, star_lookup, RA0=None, Dec0=None):
        """
        Populate self.stars with Star objects from the lookup dict.

        Paramenters:
            star_lookup (dict): mappping HR -> Star instance
        """
        self.stars = []
        total_expected = len(self.hr_sequence)
        for hr in self.hr_sequence:
            star = star_lookup.get(hr)
            if star:
                if RA0 is not None and Dec0 is not None:
                    ad = angular_distance(star.ra_deg, star.dec_deg, RA0, Dec0)
                    if ad > MAX_ANGULAR_DISTANCE:
                        continue
                self.stars.append(star)
        if len(self.stars) != total_expected:
            self.stars = []


def load_constellations(star_lookup, RA0=None, Dec0=None):
    """"
    Read raw constellations data and return list of Constallion instances
    with their "stars" list bound to Star objects.

    Parameters:
        star_lookup (dict): dict mapping HR (int) to Star

    Return:
        constellations (list): list of Constellation instances.
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