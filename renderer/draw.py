import pygame


def draw_stars(surface, stars, center, scale, color=(255, 255, 255), size=2):
    """
    Draw each star as a filled circle on the given surface.

    Parameters:
        surface (pygame.Surface): The target surface to draw on.
        stars (list): List of Star instances with .x and .y attributes.
        center (tuple): (center_x, center_y) pixel coordinates of map origin.
        scale (float): Scaling factor from star coordinates to pixels.
        color (tuple): RGB clor of the stars.
        size (int): Radius in pixels of each drawn star.
    """
    # Unpack center pixel coordinates (origin of star map)
    cx, cy = center
    for star in stars:
        # Convert star.x, star.y (map coords) to screen pixels
        px = cx + star.x * scale
        py = cy - star.y * scale
        # Draw a small circle at (px, py)
        pygame.draw.circle(surface, color, (int(px), int(py)), size)


def draw_constellations(surface, constellations, center, scale, color=(200, 200, 200), width=1):
    """
    Draw lines connecting stars in each constellation.

    Parameters:
        surface (pygame.Surface): The target surface to draw on.
        constellations (list): List of Constellation instances with .stars lists.
        center (tuple): (center_x, center_y) pixel coordinates of map origin.
        scale (float): Scaling factor from star coordinates to pixels.
        color (tuple): RGB color of constellation lines.
        width (int): Line thickness in pixels.
    """
    # Unpack center pixel coordinates
    cx, cy = center
    for constellation in constellations:
        stars = constellation.stars
        if len(stars) < 2:
            continue

        # Connect each star to the next in sequence
        for a, b in zip(stars, stars[1:]):
            # Convert endpoints to screen pixels
            x1 = cx + a.x * scale
            y1 = cy - a.y * scale
            x2 = cx + b.x * scale
            y2 = cy - b.y * scale
            # Draw a line between the two points
            pygame.draw.line(surface, color, (int(x1), int(y1)), (int(x2), int(y2)), width)