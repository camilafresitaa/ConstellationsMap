import pygame


def draw_stars(surface, stars, center, scale, color=(255, 255, 255), min_size=0.1, max_size=4, min_alpha=30, max_alpha=255):
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
        # Normalize brightness
        norm = (max_v - star.vmag) / dv

        # Compute dynamic size and alpha
        size = int(min_size + norm * (max_size - min_size))
        alpha = int(min_alpha + norm * (max_alpha - min_alpha))

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

        # 1. Para cada estrella, dibujar su HR
        for star in constellation.stars:
            px = cx - star.x * scale
            py = cy - star.y * scale
            label_surf = font.render(str(star.hr), True, color)  # star.hr está en Star :contentReference[oaicite:2]{index=2}&#8203;:contentReference[oaicite:3]{index=3}
            # Ajustar un poco la posición para que no solape la estrella
            surface.blit(label_surf, (int(px) + 4, int(py) - 4))

        # 2. Dibujar el nombre de la constelación en su centroide
        avg_x = sum(star.x for star in constellation.stars) / len(constellation.stars)
        avg_y = sum(star.y for star in constellation.stars) / len(constellation.stars)
        px = cx - avg_x * scale
        py = cy - avg_y * scale
        name_surf = font.render(constellation.name, True, color)
        # Centrar el texto sobre el punto medio
        w, h = name_surf.get_size()
        surface.blit(name_surf, (int(px - w/2), int(py - h/2)))