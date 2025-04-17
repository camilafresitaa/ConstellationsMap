import numpy as np
from stars_coords_2d import stars_coords

class Star():
    """
    Represents a star with...
    """
    def __init__(self, HR: int, name: str, vmag: float, x: float, y: float, homogeneous: np.array):
        self.hr = HR
        self.name = name
        self.vmag = vmag
        self.x = x
        self.y = y
        self.homogeneous = homogeneous

    def __repr__(self):
        return(f"Star {self.hr}: ({self.x}, {self.y})")
    
    def apply_transformation(self, matrix: np.array):
        """
        Apply a 3x3 transformation matrix to this star's homogeneous coordinate.
        Updates x, y and the coordinate in place.

        Parameters:
            matrix (np.ndarray): Composite 3x3 transformation.
        """
        new_homogeneous = matrix @ self.homogeneous
        self.homogeneous = new_homogeneous
        self.x, self.y = float(new_homogeneous[0]), float(new_homogeneous[1])
    

def load_stars():
    """
    Return list of Star instances.
    """
    stars_2d = stars_coords()
    stars = []

    for s in stars_2d:
        star = Star(HR=
            int(s["HR"]), 
            name=s["Name"], 
            vmag=float(s["Vmag"]), 
            x=s["x"],
            y=s["y"],
            homogeneous=s["Homogeneous"]
            )
        stars.append(star)

    return stars