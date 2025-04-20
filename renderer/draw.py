import pygame
import math


def draw_stars(surface, stars, center, scale, zoom_level=1.0, color=(255, 255, 255), min_size=1, max_size=3.5, min_alpha=50, max_alpha=255):
    """
    Draw each star as a filled circle on the given surface.

    Parameters:
        surface (pygame.Surface): The target surface to draw on.
        stars (list): List of Star instances with .x and .y attributes.
        center (tuple): (center_x, center_y) pixel coordinates of map origin.
        scale (float): Scaling factor from star coordinates to pixels.
        color (tuple): RGB color of the stars.
        min_size (int): Minimum radius in pixels for the faintest star.
        max_size (int): Maximum radius in pixels for the brightest star.
        min_alpha (int): Minimum alpha (0-255) for the faintest star.
        max_alpha (int): Maximum alpha (0-255) for the brightest star.
    """
    # Unpack center pixel coordinates (origin of star map)
    cx, cy = center

    # Determine vmag range
    vmag_values = [star.vmag for star in stars]
    if not vmag_values:
        return
    min_v, max_v = min(vmag_values), max(vmag_values)
    dv = max_v - min_v if max_v > min_v else 1

    for star in stars:

        # visibility_limit = 6.5 + 5.5 * math.log10(zoom_level + 1e-5)

        DEFAULT_SCALE = 0.3
        zoom_relative = zoom_level / DEFAULT_SCALE
        visibility_limit = 5 + 7 * math.log10(zoom_relative + 1e-5)
        if star.vmag > visibility_limit:
            continue    


        # Normalize brightness
        norm = (max_v - star.vmag) / dv

        # Compute dynamic size and alpha
        distance = math.sqrt(star.x**2 + star.y**2)
        depth_factor = 1 / (1 + (distance * 0.15)**2)  # Ajustable value

        size = int((min_size + norm * (max_size - min_size)) * depth_factor)
        size = max(size, 1)

        alpha = int((min_alpha + norm * (max_alpha - min_alpha)) * depth_factor)
        alpha = max(alpha, 1)

        # Convert star coords to screen pixels
        px = cx - star.x * scale
        py = cy - star.y * scale

        # Create temporary surface for per-star alpha
        surf = pygame.Surface((size*2, size*2), pygame.SRCALPHA)
        draw_color = (color[0], color[1], color[2], alpha)
        pygame.draw.circle(surf, draw_color, (size, size), size)

        # Blit at center offset by size
        surface.blit(surf, (int(px - size), int(py - size)))


def draw_constellations(surface, constellations, center, scale, color=(200, 200, 200), width=1, max_segment_frac=0.5):
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
            x1 = cx - a.x * scale
            y1 = cy - a.y * scale
            x2 = cx - b.x * scale
            y2 = cy - b.y * scale
            # Draw a line between the two points
            pygame.draw.line(surface, color, (int(x1), int(y1)), (int(x2), int(y2)), width)


def draw_labels(surface, constellations, center, scale, font, color=(255,255,0)):
    """
    """
    cx, cy = center
    for constellation in constellations:
        # Si la constelación no tiene estrellas, saltar
        if not constellation.stars:
            continue

        # 2. Dibujar el nombre de la constelación en su centroide
        avg_x = sum(star.x for star in constellation.stars) / len(constellation.stars)
        avg_y = sum(star.y for star in constellation.stars) / len(constellation.stars)
        px = cx - avg_x * scale
        py = cy - avg_y * scale
        name_surf = font.render(constellation.name, True, color)
        # Centrar el texto sobre el punto medio
        w, h = name_surf.get_size()
        surface.blit(name_surf, (int(px - w/2), int(py - h/2)))


def draw_hr_labels(surface, stars, center, scale, zoom_level, font, color=(160, 160, 160)):
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