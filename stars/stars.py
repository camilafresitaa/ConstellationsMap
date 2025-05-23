import numpy as np
from stars.stars_coords_2d import stars_coords

class Star():
    """
    A star in the 2D projection space, with its properties and support for transformation using homogeneous coordinates.
    """
    def __init__(self, HR: int, name: str, vmag: float, x: float, y: float, homogeneous: np.array, ra_deg: float, dec_deg: float):
        self.hr = HR
        self.name = name
        self.vmag = vmag
        self.x = x
        self.y = y
        self.base_homogeneous = homogeneous.copy()  # To reset if needed
        self.homogeneous = homogeneous.copy()
        self.ra_deg = ra_deg
        self.dec_deg = dec_deg

    def __repr__(self):
        return(f"Star {self.hr}: ({self.x}, {self.y})")
    
    def apply_transformation(self, matrix: np.array):
        """
        Applies a transformation matrix to this star's base homogeneous coordinate.
        Updates its current position accordingly.

        Parameters:
            matrix (np.ndarray): 3x3 transformation matrix.
        """
        new_homogeneous = matrix @ self.base_homogeneous
        self.homogeneous = new_homogeneous
        self.x, self.y = float(new_homogeneous[0]), float(new_homogeneous[1])
    

def load_stars():
    """
    Load star catalog and return list of Star objects with 2D coordinates and homogeneous vectors ready for transformation.
    """
    stars_2d, RA0, Dec0 = stars_coords()
    stars = []
    for s in stars_2d:
        star = Star(HR=
            int(s["HR"]), 
            name=s["Name"], 
            vmag=float(s["Vmag"]), 
            x=s["x"],
            y=s["y"],
            homogeneous=s["Homogeneous"],
            ra_deg=s["RA_deg"],
            dec_deg=s["Dec_deg"]
        )
        stars.append(star)

    return stars, RA0, Dec0