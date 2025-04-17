import pygame
import math


def draw_stars(surface, stars, color=(255, 255, 255), min_size=0.1, max_size=4, min_alpha=30, max_alpha=255):
    """
    Draw points for each star.

    Parameters:
        surface (pygame.Surface): The target surface to draw on.
        stars (list): List of Star instances, each must have x,y in pixel coords.
        center (tuple): Not used if stars already in pixel coords.
        color (tuple): RGB color of the stars.
        min_size (int): Minimum radius in pixels for the faintest star.
        max_size (int): Maximum radius in pixels for the brightest star.
        min_alpha (int): Minimum alpha (0-255) for the faintest star.
        max_alpha (int): Maximum alpha (0-255) for the brightest star.
    """
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

        # Create temporary surface for per-star alpha
        # surf = pygame.Surface((size*2, size*2), pygame.SRCALPHA)
        draw_color = (color[0], color[1], color[2], alpha)

        x, y = star.x, star.y
        pygame.draw.circle(surface, draw_color, (int(x), int(y)), size)


def draw_constellations(surface, constellations, max_length_px=None, color=(200, 200, 200), width=1):
    """
    Draw lines connecting stars in each constellation.

    Parameters:
        surface (pygame.Surface): The target surface to draw on.
        constellations (list): List of Constellation instances with .stars lists.
        color (tuple): RGB color of constellation lines.
        width (int): Line thickness in pixels.
    """
    for constellation in constellations:
        stars = constellation.stars
        for a, b in zip(stars, stars[1:]):
            # Convert endpoints to screen pixels
            x1, y1 = a.x, a.y
            x2, y2 = b.x, b.y
            # Draw a line between the two points
            if max_length_px is not None:
                dist = math.hypot(x2 - x1, y2 - y1)
                if dist > max_length_px:
                    continue
            pygame.draw.line(surface, color, (int(x1), int(y1)), (int(x2), int(y2)), width)


# def draw_labels(surface, constellations, center, scale, font, color=(255,255,0)):
#     """
#     """
#     cx, cy = center
#     for constellation in constellations:
#         # Si la constelación no tiene estrellas, saltar
#         if not constellation.stars:
#             continue

#         # 1. Para cada estrella, dibujar su HR
#         for star in constellation.stars:
#             px = cx - star.x * scale
#             py = cy - star.y * scale
#             label_surf = font.render(str(star.hr), True, color)  # star.hr está en Star :contentReference[oaicite:2]{index=2}&#8203;:contentReference[oaicite:3]{index=3}
#             # Ajustar un poco la posición para que no solape la estrella
#             surface.blit(label_surf, (int(px) + 4, int(py) - 4))

#         # 2. Dibujar el nombre de la constelación en su centroide
#         avg_x = sum(star.x for star in constellation.stars) / len(constellation.stars)
#         avg_y = sum(star.y for star in constellation.stars) / len(constellation.stars)
#         px = cx - avg_x * scale
#         py = cy - avg_y * scale
#         name_surf = font.render(constellation.name, True, color)
#         # Centrar el texto sobre el punto medio
#         w, h = name_surf.get_size()
#         surface.blit(name_surf, (int(px - w/2), int(py - h/2)))