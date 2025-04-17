import numpy as np
from stars.stars_coords_3d import stars_coords_3d

class Star():
    """
    Represents a star with 3D homogeneous coordinates.

    Attributes:
        hr (int): Harvard Revised number.
        name (str): Star designation.
        vmag (float): Visual magnitude.
        base_homogeneous (np.ndarray): Original [x,y,z,1].
        homogeneous (np.ndarray): Transformed [x,y,z,1].
        x, y, z (float): Current Cartesian coordinates.
    """
    def __init__(self, HR: int, name: str, vmag: float, homogeneous: np.array):
        self.hr = HR
        self.name = name
        self.vmag = vmag
        self.base_homogeneous = homogeneous.copy()
        self.homogeneous = homogeneous.copy()

    def __repr__(self):
        return(f"Star {self.hr}: ({self.base_homogeneous})")
    
    def apply_transformation(self, matrix: np.array):
        """
        Apply a 4x4 transformation matrix to this star's homogeneous coordinate.
        Updates x, y, z and homogeneous in place.

        Parameters:
            matrix (np.ndarray): Composite 4x4 transformation.
        """
        new_homogeneous = matrix @ self.base_homogeneous
        self.homogeneous = new_homogeneous
        self.x = float(new_homogeneous[0])
        self.y = float(new_homogeneous[1])
        self.z = float(new_homogeneous[2])
    

def load_stars():
    """
    Return list of Star instances with 3D coords.
    """
    stars_data = stars_coords_3d()
    stars = []

    for s in stars_data:
        star = Star(
            HR=int(s["HR"]), 
            name=s["Name"], 
            vmag=float(s["Vmag"]),
            homogeneous=s["homogeneous"]
            )
        stars.append(star)

    return stars