from constellations.constellations_parser import read_constellations

class Constellation():
    """
    Represents a constellation defined by a sequence of star HR numbers,
    with associated Star instances holding 3D homogeneous coordinates.

    Attributes:
        name (str): Name of the constellation.
        hr_sequence (List[int]): Sequence of HR numbers defining star order.
        stars (List[Star]): Bound Star objects (with .homogeneous attributes).  
    """
    def __init__(self, name: str, hr_sequence: list):
        self.name = name
        self.hr_sequence = hr_sequence
        self.stars = []

    def __repr__(self):
        return (f"Constellation {self.name}: ({self.hr_sequence})")

    def bind_stars(self, star_lookup: dict):
        """
        Populate "stars" list with Star instances from the lookup dict.

        Paramenters:
            star_lookup (dict): Mappping HR (int) -> Star instance
        """
        self.stars = []
        for hr in self.hr_sequence:
            star = star_lookup.get(hr)
            if star is not None:
                self.stars.append(star)
        # After this, self.stars contains the Star objects in the same order as hr_sequence


def load_constellations(star_lookup):
    """"
    Read raw constellation definitions and bind Star objects.

    Parameters:
        star_lookup (dict): Mapping HR (int) -> Star instance

    Return:
        constellations (list): list of Constellation instances.
    """
    raw_list = read_constellations()
    constellations = []
    for entry in raw_list:
        name = entry["Name"]
        hr_seq = entry["HR_sequence"]
        c = Constellation(name, hr_seq)
        c.bind_stars(star_lookup)
        constellations.append(c)
    return constellations