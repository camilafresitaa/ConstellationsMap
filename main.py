import sys
import pygame
from stars.stars import load_stars
from constellations.constellations import load_constellations
from renderer.draw import draw_stars, draw_constellations, draw_labels
from scr.transformations import compose_transformations, perspective_matrix
from input.events import handle_events, build_operations


# Frames per second
FPS = 60
# Base scale (pixels per map unit)
SCALE = 50
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
}
state = default_state.copy()


def main():
    pygame.init()
    font = pygame.font.SysFont(None, 20)
    info = pygame.display.Info()
    WIDTH = info.current_w
    HEIGHT = info.current_h
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()

    # Calculate center based on window size
    CENTER = (WIDTH // 2, HEIGHT // 2)

    # Load data
    stars = load_stars()
    star_lookup = {star.hr: star for star in stars}
    constellations = load_constellations(star_lookup)

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
        P = perspective_matrix(state['fov'], WIDTH/HEIGHT, state['near'], state['far'])
        M_final = P @ M_modelview

        # 4) Transform and project stars
        projected = {}
        for star in stars:
            v = star.homogeneous
            vt = M_final @ v
            # Cull behind near plane or w<=0
            if vt[3] <= 0:
                continue
            ndc = vt[:3] / vt[3]
            # Convert NDC [-1..1] to pixel coords
            px = (ndc[0] + 1) * 0.5 * WIDTH
            py = (1 - ndc[1]) * 0.5 * HEIGHT
            projected[star.hr] = (px, py)

        # 5) Draw
        screen.fill((0, 0, 0))

        # Draw constellations
        for con in constellations:
            pts = [projected.get(st.hr) for st in con.stars]
            # Connect only existing projected points
            for a, b in zip(pts, pts[1:]):
                if a and b:
                    pygame.draw.line(screen, (200, 200, 200), a, b, 1)

        # Draw stars
        for hr, (px, py) in projected.items():
            pygame.draw.circle(screen, (255, 255, 255), (int(px), int(py)), 2)

        # # Render constellations and stars
        # draw_constellations(screen, constellations, CENTER, SCALE)
        # draw_stars(screen, stars, CENTER, SCALE)
        # draw_labels(screen, constellations, CENTER, SCALE, font)
        pygame.display.flip()

    pygame.quit()    
    sys.exit()

if __name__ == '__main__':
    main()