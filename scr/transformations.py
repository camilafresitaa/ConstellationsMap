import numpy as np
import math


def rotation_matrix(angle_degrees):
    """
    Returns a 3x3 rotation matrix that rotates points about the origin.
    
    Mathematical Explanation:
    The standard 2D rotation matrix for an angle θ (in radians) is:
        [ cos(θ)  -sin(θ)   0 ]
        [ sin(θ)   cos(θ)   0 ]
        [   0        0      1 ]
    This matrix rotates a point (x, y) by the angle θ while preserving homogeneous coordinates.

    Visual Effect:
    Applying this matrix rotates the entire screen (or "sky") by the specified angle,
    effectively "spinning" the view of the star map.

    Parameters:
        angle_degrees (float): The rotation angle in degrees.

    Returns:
        numpy.array: A 3x3 rotation matrix.
    """

    # Get cos and sin of angle in radians
    angle_radians = math.radians(angle_degrees)
    cos_theta = math.cos(angle_radians)
    sin_theta = math.sin(angle_radians)

    return np.array([
        [cos_theta, -sin_theta, 0],
        [sin_theta, cos_theta, 0],
        [0, 0, 1]
    ])


def translation_matrix(tx, ty):
    """
    Returns a 3x3 translation matrix that shifts points by (tx, ty).
    
    Mathematical Explanation:
    The translation matrix in homogeneous coordinates is:
        [ 1   0   tx ]
        [ 0   1   ty ]
        [ 0   0   1  ]
    It adds tx to the x-coordinate and ty to the y-coordinate of a point.
    
    Visual Effect:
    This matrix moves (or "slides") the entire scene, allowing you to reposition 
    the star map within your view without altering its orientation or shape.
    
    Parameters:
        tx (float): Translation along the x-axis.
        ty (float): Translation along the y-axis.
    
    Returns:
        numpy.array: A 3x3 translation matrix.
    """

    return np.array([
        [1, 0, tx],
        [0, 1, ty],
        [0, 0, 1]
    ])


def scaling_matrix(sx, sy):
    """
    Returns a 3x3 scaling matrix that scales points along the x and y axes.
    
    Mathematical Explanation:
    The scaling matrix in homogeneous coordinates is:
        [ sx   0    0 ]
        [  0   sy   0 ]
        [  0   0    1 ]
    Each point (x, y) is transformed to (sx*x, sy*y).
    
    Visual Effect:
    Scaling enlarges or shrinks the scene. A factor greater than 1 zooms in (enlarging),
    while a factor between 0 and 1 zooms out (shrinking) the star map.
    
    Parameters:
        sx (float): Scaling factor for the x-axis.
        sy (float): Scaling factor for the y-axis.
    
    Returns:
        numpy.array: A 3x3 scaling matrix.    
    """

    return np.array([
        [sx, 0 ,0],
        [0, sy, 0],
        [0, 0, 1]
    ])


def reflection_matrix(axis="x"):
    """
    Returns a 3x3 reflection matrix that mirrors points across the specified axis.
    
    Mathematical Explanation:
    Reflection matrices in homogeneous coordinates are defined as:
    - For reflection across the x-axis:
          [ 1   0   0 ]
          [ 0  -1   0 ]
          [ 0   0   1 ]
    - For reflection across the y-axis:
          [ -1  0   0 ]
          [ 0   1   0 ]
          [ 0   0   1 ]
    - For reflection across both axes:
          [ -1  0   0 ]
          [ 0  -1   0 ]
          [ 0   0   1 ]
    
    Visual Effect:
    This matrix produces a mirror image of the scene along the specified axis or axes,
    effectively "flipping" the star map horizontally, vertically, or both.
    
    Parameters:
        axis (str): Specifies the axis of reflection; accepted values are "x", "y", or "both".
    
    Returns:
        numpy.array: A 3x3 reflection matrix.
    """

    if axis == "x":
        return np.array([
            [1, 0, 0],
            [0, -1, 0],
            [0, 0, 1]
        ])
    elif axis == "y":
        return np.array([
            [-1, 0, 0],
            [0, 1, 0],
            [0, 0, 1]
        ])
    elif axis == "both":
        return np.array([
            [-1, 0, 0],
            [0, -1, 0],
            [0, 0, 1]
        ])
    else:
        raise ValueError("Invalid axis. Use 'x', 'y', or 'both'.")
    

def shearing_matrix(shx, shy):
    """
    Returns a 3x3 shearing matrix that distorts the scene by shifting coordinates.
    
    Mathematical Explanation:
    The shearing (or skew) matrix in homogeneous coordinates is given by:
        [ 1   shx   0 ]
        [ shy  1    0 ]
        [ 0    0    1 ]
    Here, shx is the shear factor for x (which shifts x by an amount proportional to y),
    and shy is the shear factor for y (which shifts y by an amount proportional to x).
    
    Visual Effect:
    This matrix distorts the scene by "slanting" or "tilting" the positions of points in the star map,
    creating a skewed or sheared effect.
    
    Parameters:
        shx (float): Shear factor along the x-axis.
        shy (float): Shear factor along the y-axis.
    
    Returns:
        numpy.array: A 3x3 shearing matrix.
    """
    
    return np.array([
        [1, shx, 0],
        [shy, 1, 0],
        [0, 0, 1]
    ])


def compose_transformations(transformations):
    """
    Compose a series of 3x3 transformation matrices based on a user-specified order.

    Each transformation is defined as a dictionary with a "type" key and its parameters.
    The order of the transformations in the list corresponds to the order in which they are applied:
    the first in the list is applied first, then the next, and so on.

    Parameters:
        transformations (list): List of dictionaries. Each dictionary specifies a transformation. Supported types and parameters:
            - "rotate": {"angle": angle_in_degrees}
            - "translate": {"tx": value, "ty": value}
            - "scale": {"sx": value, "sy": value}
            - "shear": {"shx": value, "shy": value}
            - "reflect": {"axis": "x"|"y"|"both"}

    Returns:
        numpy.ndarray: The composite 3x3 transformation matrix.
    
    """

    composite = np.eye(3)
    for transformation in transformations:
        t_type = transformation["type"]
        if t_type == "rotate":
            M = rotation_matrix(transformation["angle"])
        elif t_type == "translate":
            M = translation_matrix(transformation["tx"], transformation["ty"])
        elif t_type == "scale":
            M = scaling_matrix(transformation["sx"], transformation["sy"])
        elif t_type == "shear":
            M = shearing_matrix(transformation["shx"], transformation["shy"])
        elif t_type == "reflect":
            M = reflection_matrix(transformation["axis"])
        else:
            raise ValueError(f"Invalid transformation type: {t_type}")
        
        # Multiply the new matrix to the composite matrix.
        # Using M @ composite ensures that the transformation M is applied after the transformations
        # already in "composite", which corresponds to the user specified order.
        composite = M @ composite
    return composite


# Example usage
if __name__ == "__main__":
    # Define example transformation parameters.
    transformations_list = [
        {"type": "rotate", "angle": 45},
        {"type": "translate", "tx": 10 , "ty": 5},
        {"type": "scale", "sx": 1.2, "sy": 1.2}
    ]

    # Generate composite matrix.
    composite_matrix = compose_transformations(transformations_list)
    # Print matrix for verification.
    print("Composite matrix:\n", composite_matrix)

