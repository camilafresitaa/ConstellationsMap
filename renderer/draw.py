import pygame
import math


def draw_stars(surface, stars, center, scale, zoom_level=1.0, color=(255, 255, 255), min_size=1, max_size=3.5, min_alpha=50, max_alpha=255):
    """
    Render stars as filled circles with brightness and size based on their magnitude.
    Stars farther away or with low brightness are faded out.

    Parameters:
        surface (pygame.Surface): Target surface where stars will be drawn.
        stars (list): List of Star instances with x, y, and vmag attributes.
        center (tuple): Pixel coordinates (cx, cy) of the center of the map.
        scale (float): Factor to convert star coordinates into pixels.
        zoom_level (float): Zoom factor to control visibility range and size.
        color (tuple): RGB color of the stars.
        min_size (int): Minimum pixel size (radius) for the faintest stars.
        max_size (float): Maximum pixel size (radius) for the brightest stars.
        min_alpha (int): Minimum alpha (transparency) value for faint stars.
        max_alpha (int): Maximum alpha value for bright stars.
    """
    # Center of the screen
    cx, cy = center

    # Get magnitude range to normalize brightness
    vmag_values = [star.vmag for star in stars]
    if not vmag_values:
        return
    min_v, max_v = min(vmag_values), max(vmag_values)
    dv = max_v - min_v if max_v > min_v else 1

    for star in stars:
        # Determine whether star should be visible based on zoom and magnitude
        DEFAULT_SCALE = 0.3
        zoom_relative = zoom_level / DEFAULT_SCALE
        visibility_limit = 5 + 7 * math.log10(zoom_relative + 1e-5)

        fade_range = 1
        fade_factor = max(0.0, min(1.0, (visibility_limit - star.vmag) / fade_range))
        if star.vmag > visibility_limit and fade_factor <= 0.001:
            continue    

        # Normalize brightness based on magnitude
        norm = (max_v - star.vmag) / dv

        # Simulate depth by reducing size/brightness for distant stars
        distance = math.sqrt(star.x**2 + star.y**2)
        depth_factor = 1 / (1 + (distance * 0.15)**2)

        size = int((min_size + norm * (max_size - min_size)) * depth_factor)
        size = max(size, 1)

        alpha = int((min_alpha + norm * (max_alpha - min_alpha)) * depth_factor)
        alpha = max(alpha, 1)
        alpha = int(alpha * fade_factor)

        # Convert to pixel coordinates
        px = cx - star.x * scale
        py = cy - star.y * scale

        # Create circle with per-star alpha value
        surf = pygame.Surface((size*2, size*2), pygame.SRCALPHA)
        draw_color = (color[0], color[1], color[2], alpha)
        pygame.draw.circle(surf, draw_color, (size, size), size)
        surface.blit(surf, (int(px - size), int(py - size)))


def draw_constellations(surface, constellations, center, scale, color=(200, 200, 200), width=1):
    """
    Draw lines between stars that form each constellation.

    Parameters:
        surface (pygame.Surface): Surface where the lines will be drawn.
        constellations (list): List of Constellation instances with .stars attribute.
        center (tuple): Pixel coordinates (cx, cy) of the center of the screen.
        scale (float): Factor to convert star coordinates to pixels.
        color (tuple): RGB color for the constellation lines.
        width (int): Pixel thickness of the lines.
    """
    # Center of the screen
    cx, cy = center
    for constellation in constellations:
        stars = constellation.stars
        if len(stars) < 2:
            continue

        # Connect each star to the next in sequence
        for a, b in zip(stars, stars[1:]):
            # Convert endpoints to screen pixels
            x1 = cx - a.x * scale
            y1 = cy - a.y * scale
            x2 = cx - b.x * scale
            y2 = cy - b.y * scale
            # Draw a line between the two points
            pygame.draw.line(surface, color, (int(x1), int(y1)), (int(x2), int(y2)), width)


def draw_labels(surface, constellations, center, scale, font, color=(255,255,0)):
    """
    Draw the name of each constellation at the centroid of its stars.
    """
    # Center of the screen
    cx, cy = center
    for constellation in constellations:
        if not constellation.stars:
            continue

        avg_x = sum(star.x for star in constellation.stars) / len(constellation.stars)
        avg_y = sum(star.y for star in constellation.stars) / len(constellation.stars)
        px = cx - avg_x * scale
        py = cy - avg_y * scale

        name_surf = font.render(constellation.name, True, color)
        w, h = name_surf.get_size()
        surface.blit(name_surf, (int(px - w/2), int(py - h/2)))


def draw_hr_labels(surface, stars, center, scale, zoom_level, font, color=(160, 160, 160)):
    """
    Show the HR (catalog) number of visible stars near their position.
    """
    # Center of the screen    
    cx, cy = center
    for star in stars:
        DEFAULT_SCALE = 0.3
        zoom_relative = zoom_level / DEFAULT_SCALE
        visibility_limit = 5 + 7 * math.log10(zoom_relative + 1e-5)
        if star.vmag > visibility_limit:
            continue

        px = cx - star.x * scale
        py = cy - star.y * scale
        label = str(star.hr)
        label_surf = font.render(label, True, color)
        surface.blit(label_surf, (int(px + 5), int(py - 5)))