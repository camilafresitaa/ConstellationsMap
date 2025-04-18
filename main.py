import pygame
from stars.stars import load_stars
from constellations.constellations import load_constellations
from renderer.draw import draw_stars, draw_constellations, draw_labels
from scr.transformations import compose_transformations
from input.events import handle_events, build_operations


# Frames per second
FPS = 60
# Base scale (pixels per map unit)
SCALE = 1000

def main():
    # Initialize Pygame
    pygame.init()
    font = pygame.font.SysFont(None, 15)
    info = pygame.display.Info()
    WIDTH = info.current_w
    HEIGHT = info.current_h
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()

    # Calculate center based on window size
    CENTER = (WIDTH // 2, HEIGHT // 2)

    # Load and bind data
    stars, RA0, Dec0 = load_stars()
    star_lookup = {star.hr: star for star in stars}
    constellations = load_constellations(star_lookup, RA0, Dec0)

    # Initial transformation state
    state = {
        'angle': 0.0,
        'tx': 0.0,
        'ty': 0.0,
        'scale': 1.0,
        'reflect': False,
        'shx': 0.0,
        'shy': 0.0
    }

    running = True
    while running:
        # Compute delta time (seconds)
        dt = clock.tick(FPS) / 1000.0

        # Process events and update state
        running = handle_events(state, dt)

        # Build and compose transformation matrix
        operations = build_operations(state)
        matrix = compose_transformations(operations)

        # Apply transformation to all stars
        for star in stars:
            star.apply_transformation(matrix)

        # Clear screen
        screen.fill((0, 0, 0))

        # Render constellations and stars
        draw_constellations(screen, constellations, CENTER, SCALE)
        draw_stars(screen, stars, CENTER, SCALE)
        draw_labels(screen, constellations, CENTER, SCALE, font)
        pygame.display.flip()

    pygame.quit()    


if __name__ == '__main__':
    main()