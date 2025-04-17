import pygame
from stars.stars import load_stars
from constellations.constellations import load_constellations
from renderer.draw import draw_stars, draw_constellations
from scr.transformations import compose_transformations


# SCREEN SEETINGS
WIDTH = 800
HEIGHT = 600
FPS = 60

# Initial view parameters
CENTER = (WIDTH // 2, HEIGHT // 2)
SCALE = 50  # Pixels per map unit

# Example starting operations (empty = no transform)
opertions = []


def handle_events(operations):
    """
    Process user input and update the list of transformations.
    """
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False, operations    # ????
        elif event.type == pygame.KEYDOWN:
            # RESET
            if event.key == pygame.K_r:
                operations = []
            # CONTROLS: add rotation, zoom, translation, reflection, shear controls
    return True, operations


def main():
    # Initialize Pygame
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()

    # Load and bind data
    stars = load_stars()
    star_lookup = {star.hr: star for star in stars}
    constellations = load_constellations(star_lookup)

    running = True
    operations = []

    while running:
        # Handle input events
        running, operations = handle_events(operations)

        # Compose composite transform matrix
        transform_matrix = compose_transformations(operations)

        # Apply transformation to all stars
        for star in stars:
            star.apply_transformation(transform_matrix)

        # Clear screen
        screen.fill((0, 0, 0))

        # Draw constellations (lines first)
        draw_constellations(screen, constellations, CENTER, SCALE)
        # Draw stars (on top)
        draw_stars(screen, stars, CENTER, SCALE)

        # Update display
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()    


if __name__ == '__main__':
    main()