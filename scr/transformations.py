import numpy as np
import math


def rotation_matrix(angle_degrees):
    """
    Returns a 3x3 rotation matrix that rotates points about the origin.
    
    Mathematical Explanation:
    The standard 2D ration matrix for an angle θ (in radians) is:
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


def compose_transformations(angle, tx, ty, sx, sy, shx, shy, reflection_axis=None):
    """
    
    """

    # Get transformation matrices
    scale = scaling_matrix(sx, sy)
    rotate = rotation_matrix(angle)
    shear = shearing_matrix(shx, shy)
    translate = translation_matrix(tx, ty)

    if reflection_axis:
        reflection = reflection_matrix(reflection_axis)
    else:
        reflection = np.eye(3) # If reflection_axis is not provided, use the identity matrix.

    
    # Compose the transformations
    # Multiply matrices in order: scale -> rotate -> reflection -> translate
    composite_matrix = translate @ reflection @ shear @ rotate @ scale

    return composite_matrix



