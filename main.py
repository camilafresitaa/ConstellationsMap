import sys
import pygame
import numpy as np
from stars.stars import load_stars
from constellations.constellations import load_constellations
from renderer.draw import draw_stars, draw_constellations
from scr.transformations import compose_transformations, perspective_matrix
from input.events import handle_events, build_operations


# Configuration & Initialization
FPS = 60
pygame.init()
info = pygame.display.Info()
WIDTH, HEIGHT = info.current_w, info.current_h
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
ASPECT = WIDTH / HEIGHT

# Camera and projection state
default_state = {
    'cam_x': 0.0,
    'cam_y': 0.0,
    'cam_z': 0.0,
    'pitch': 0.0,   # rotation around X
    'yaw': 0.0,     # rotation around Y
    'roll': 0.0,    # rotation around Z
    'fov': 60.0,
    'near': 0.1,
    'far': 1000.0,
    'move_speed': 10.0,  # Units per second
    'mouse_sens':  0.1,  # Degrees per pixel of mouse movement
}
state = default_state.copy()

# Load stars & constellations
stars = load_stars()
star_lookup = {star.hr: star for star in stars}
constellations = load_constellations(star_lookup)


# == Nuevo cálculo de 'far' basado en paralaje real ==
# Calculamos la distancia máxima de cualquier estrella al origen
max_dist = max(
    np.linalg.norm(star.base_homogeneous[:3])
    for star in stars
)
# Ajustamos el far plane a un poco más allá de la estrella más lejana
state['far'] = max_dist * 1.1


def main():
    running = True
    while running:
        # Compute delta time (seconds)
        dt = clock.tick(FPS) / 1000.0

        # 1) Handle input, update state
        running = handle_events(state, dt)

        # 2) Build model-view (camera) transformations
        operations = build_operations(state)
        M_modelview = compose_transformations(operations)

        # 3) Perspective projection
        P = perspective_matrix(state['fov'], ASPECT, state['near'], state['far'])
        M_final = P @ M_modelview

        # Apply transform and project to screen coords
        for star in stars:
            star.apply_transformation(M_final)
            x_h, y_h, z_h, w_h = star.homogeneous
            x_ndc = x_h / w_h
            y_ndc = y_h / w_h
            # NDC (-1..1) to pixel coords
            star.x = ( x_ndc + 1) * 0.5 * WIDTH
            star.y = (1 - y_ndc) * 0.5 * HEIGHT

        # Render
        screen.fill((0,0,0))
        draw_constellations(screen, constellations)
        draw_stars(screen, stars)
        pygame.display.flip()

    pygame.quit()    
    sys.exit()

if __name__ == '__main__':
    main()