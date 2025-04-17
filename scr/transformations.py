import numpy as np
import math


def rotation_x_matrix(angle_degrees: float):
    """
    Returns a 4x4 matrix rotating points around the x-axis by angle (degrees).
    
    Mathematical Explanation:
    The x-axis rotation matrix for angle θ (radians) is:
        [ 1    0     0    0 ]
        [ 0  cosθ  -sinθ  0 ]
        [ 0  sinθ   cosθ  0 ]
        [ 0    0     0    1 ]
    Rotates the y and z coordinates around the x-axis.

    Visual Effect:
    Applying this matrix tilts the scene up/down as if looking up or down over the X-axis.

    Parameters:
        angle_degrees (float): The rotation angle around the x-axis in degrees.

    Returns:
        numpy.ndarray: A 4x4 rotation matrix about the x-axis.
    """
    θ = math.radians(angle_degrees)
    cos = math.cos(θ)
    sin = math.sin(θ)
    return np.array([
        [1, 0,  0, 0],
        [0, cos, -sin, 0],
        [0, sin,  cos, 0],
        [0, 0,  0, 1],
    ])


def rotation_y_matrix(angle_degrees: float):
    """
    Returns a 4x4 matrix rotating points around the y-axis by angle (degrees).
    
    Mathematical Explanation:
    The y-axis rotation matrix for angle θ is:
        [ cosθ   0  sinθ  0 ]
        [   0    1    0   0 ]
        [ -sinθ  0  cosθ  0 ]
        [   0    0    0   1 ]
    Rotates the x and z coordinates around the y-axis.

    Visual Effect:
    Applying this matrix pivots the scene left/right as if turning your head side to side.

    Parameters:
        angle_degrees (float): The rotation angle around the y-axis in degrees.

    Returns:
        numpy.ndarray: A 4x4 rotation matrix about the y-axis.
    """
    θ = math.radians(angle_degrees)
    cos = math.cos(θ)
    sin = math.sin(θ)
    return np.array([
        [ cos, 0, sin, 0],
        [ 0, 1, 0, 0],
        [-sin, 0, cos, 0],
        [ 0, 0, 0, 1],
    ])


def rotation_z_matrix(angle_degrees: float):
    """
    Returns a 4x4 matrix rotating points around the z-axis by angle (degrees).
    
    Mathematical Explanation:
    The z-axis rotation matrix for angle θ is:
        [ cosθ  -sinθ   0   0 ]
        [ sinθ   cosθ   0   0 ]
        [  0      0     1   0 ]
        [  0      0     0   1 ]
    Rotates the x and y coordinates in the xy-plane.

    Visual Effect:
    Applying this matrix spins the scene clockwise or counterclockwise around the view axis.

    Parameters:
        angle_degrees (float): The rotation angle around the z-axis in degrees.

    Returns:
        numpy.ndarray: A 4x4 rotation matrix about the z-axis.
    """
    θ = math.radians(angle_degrees)
    c, s = math.cos(θ), math.sin(θ)
    return np.array([
        [c, -s, 0, 0],
        [s,  c, 0, 0],
        [0,  0, 1, 0],
        [0,  0, 0, 1],
    ])


def translation_matrix(tx: float, ty: float, tz: float):
    """
    Returns a 4x4 translation matrix that moves points by (tx, ty, tz).
    
    Mathematical Explanation:
    The homogeneous translation matrix is:
        [ 1   0   0  tx ]
        [ 0   1   0  ty ]
        [ 0   0   1  tz ]
        [ 0   0   0   1 ]
    It adds tx to the x-coordinate, ty to the y-coordinate of a point and tz to the z-coordinate.
    
    Visual Effect:
    This matrix moves (or "slides") the entire scene in 3D space without rotation or scaling.
    
    Parameters:
        tx (float): Translation along the x-axis.
        ty (float): Translation along the y-axis.
        tz (float): Translation along the z-axis.
    
    Returns:
        numpy.ndarray: A 4x4 translation matrix.
    """
    return np.array([
        [1, 0, 0, tx],
        [0, 1, 0, ty],
        [0, 0, 1, tz],
        [0, 0, 0,  1],
    ])


def scaling_matrix(sx: float, sy: float, sz: float):
    """
    Returns a 4x4 scaling matrix that scales points by (sx, sy, sz).
    
    Mathematical Explanation:
    The homogeneous scaling matrix is:
        [ sx   0    0    0 ]
        [  0   sy   0    0 ]
        [  0    0   sz   0 ]
        [  0    0    0   1 ]
    Each point (x, y, z, 1) is transformed to (sx*x, sy*y, sz*z, 1).
    
    Visual Effect:
    Enlarges or shrinks the scene along each axis.
    Values >1 zoom in, values <1 zoom out.
    
    Parameters:
        sx (float): Scaling factor for the x-axis.
        sy (float): Scaling factor for the y-axis.
        sz (float): Scaling factor for the z-axis.
    
    Returns:
        numpy.ndarray: A 4x4 scaling matrix.    
    """
    return np.array([
        [sx,  0,  0, 0],
        [ 0, sy,  0, 0],
        [ 0,  0, sz, 0],
        [ 0,  0,  0, 1],
    ])


def reflection_matrix(axis: str="xyz"):
    """
    Returns a 4x4 reflection matrix that mirrors points across the specified axis.
    
    Mathematical Explanation:
    Reflection across coordinate planes is given by -1 on the axis to mirror:
    - "x": reflect across YZ-plane [ -1, 1, 1 ]
    - "y": reflect across XZ-plane [ 1, -1, 1 ]
    - "z": reflect across XY-plane [ 1, 1, -1 ]
    
    Visual Effect:
    This matrix flips the scene along the chosen axis or axes, like a mirror.

    
    Parameters:
        axis (str): Specifies the axis of reflection; accepted values are "x", "y" or "z".
    
    Returns:
        numpy.ndarray: A 4x4 reflection matrix.
    """
    axes = {
        "x": np.array([-1,  1,  1]),
        "y": np.array([ 1, -1,  1]),
        "z": np.array([ 1,  1, -1]),
    }
    if axis not in axes:
        raise ValueError("Invalid axis. Use 'x', 'y' or 'z'.")
    rx, ry, rz = axes[axis]
    return np.array([
        [rx,  0,  0, 0],
        [ 0, ry,  0, 0],
        [ 0,  0, rz, 0],
        [ 0,  0,  0, 1],
    ])
    

def shearing_matrix(shxy: float=0, shxz: float=0,
                    shyx: float=0, shyz: float=0,
                    shzx: float=0, shzy: float=0):
    """
    Returns a 4x4 shearing matrix that skews the scene in 3D.

    Mathematical Explanation:
    Shear factors define how much one axis shifts proportionally to another:
        [ 1   shxy shxz  0 ]
        [ shyx 1   shyz  0 ]
        [ shzx shzy 1    0 ]
        [  0    0    0   1 ]
    For example, shxy shifts x by an amount proportional to y.
    
    Visual Effect:
    This matrix tilts and skews the scene, producing a slanted distortion along chosen planes.
    
    Parameters:
        shxy (float): Shear factor of x in proportion to y.
        shxz (float): Shear factor of x in proportion to z.
        shyx (float): Shear factor of y in proportion to x.
        shyz (float): Shear factor of y in proportion to z.
        shzx (float): Shear factor of z in proportion to x.
        shzy (float): Shear factor of z in proportion to y.

    Returns:
        numpy.ndarray: A 4x4 shearing matrix.
    """
    return np.array([
        [1,    shxy, shxz, 0],
        [shyx, 1,    shyz, 0],
        [shzx, shzy, 1,    0],
        [0,    0,    0,    1],
    ])


def perspective_matrix(fov_deg: float, aspect: float, near: float, far: float):
    """
    Returns a 4x4 perspective projection matrix.

    Mathematical Explanation:
    Given vertical field of view θ, aspect ratio a, near plane n, far plane f,
    the perspective matrix is:
        [ (1/tan(θ/2))/a     0               0               0     ]
        [      0          1/tan(θ/2)         0               0     ]
        [      0             0         (f+n)/(n-f)   (2*f*n)/(n-f) ]
        [      0             0              -1               0     ]
    This transforms 3D points into clip space for perspective division.

    Visual Effect:
    Creates depth and foreshortening: distant objects appear smaller and parallel lines converge.

    Parameters:
        fov_deg (float): Vertical field of view in degrees.
        aspect (float): Width divided by height of the viewport.
        near (float): Distance to near clipping plane.
        far (float): Distance to far clipping plane.

    Returns:
        numpy.ndarray: A 4x4 perspective projection matrix.
    """


def compose_transformations(transformations):
    """
    Compose a list of 4x4 transformation matrices in the given order.

    Each dict must have a 'type' key and corresponding parameters:
      - 'translate': {'tx', 'ty', 'tz'}
      - 'rotate_x':  {'angle'}
      - 'rotate_y':  {'angle'}
      - 'rotate_z':  {'angle'}
      - 'scale':     {'sx', 'sy', 'sz'}
      - 'reflect':   {'axis'}
      - 'shear':     {'shxy','shxz','shyx','shyz','shzx','shzy'}

    Returns:
        numpy.ndarray: The composite 4x4 transformation matrix.
    
    """
    composite = np.eye(4)
    for transformation in transformations:
        t_type = transformation["type"]
        if t_type == "rotate_x":
            M = rotation_x_matrix(transformation["angle"])
        elif t_type == "rotate_y":
            M = rotation_y_matrix(transformation["angle"])
        elif t_type == "rotate_z":
            M = rotation_z_matrix(transformation["angle"])
        elif t_type == "translate":
            M = translation_matrix(transformation["tx"], transformation["ty"], transformation["tz"])
        elif t_type == "scale":
            M = scaling_matrix(transformation["sx"], transformation["sy"], transformation["sz"])
        elif t_type == "shear":
            M = shearing_matrix(transformation["shxy"], transformation["shxz"], transformation["shyx"],
                                transformation["shyz"], transformation["shzx"], transformation["shzy"])
        elif t_type == "reflect":
            M = reflection_matrix(transformation["axis"])
        else:
            raise ValueError(f"Invalid transformation type: {t_type}")
        
        # Multiply the new matrix to the composite matrix.
        # Using M @ composite ensures that the transformation M is applied after the transformations
        # already in "composite", which corresponds to the user specified order.
        composite = M @ composite
    return composite
