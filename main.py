import pygame
from stars.stars import load_stars
from constellations.constellations import load_constellations
from renderer.draw import draw_stars, draw_constellations
from scr.transformations import compose_transformations
from input.events import handle_events, build_operations


# SCREEN SEETINGS
WIDTH = 800
HEIGHT = 600
FPS = 60

# Initial view parameters
CENTER = (WIDTH // 2, HEIGHT // 2)
SCALE = 50  # Pixels per map unit


def main():
    # Initialize Pygame
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()

    # Load and bind data
    stars = load_stars()
    star_lookup = {star.hr: star for star in stars}
    constellations = load_constellations(star_lookup)

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
        pygame.display.flip()

    pygame.quit()    


if __name__ == '__main__':
    main()