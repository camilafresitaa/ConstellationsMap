from constellations.constellations_parser import read_constellations

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

    def bind_stars(self, star_lookup):
        """
        Populate self.stars with Star objects from the lookup dict.

        Paramenters:
            star_lookup (dict): mappping HR -> Star instance
        """
        self.stars = []
        for hr in self.hr_sequence:
            star = star_lookup.get(hr)
            if star:
                self.stars.append(star)
        # After this, self.stars contains the Star objects in the same order as hr_sequence


def load_constellations(star_lookup):
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
        c.bind_stars(star_lookup)
        constellations.append(c)
    return constellations