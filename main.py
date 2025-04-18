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
        'shy': 0.0,
        'overlay': True,
        'constellations': True,
        'labels': True
    }

    dragging = False
    last_mouse_pos = (0, 0)
    scroll_delta_y = 0.0

    rotating = False
    last_rotation_pos = 0

    running = True
    while running:
        # Compute delta time (seconds)
        dt = clock.tick(FPS) / 1000.0

        # Process events and update state
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEWHEEL:
                scroll_delta_y += event.y

        # Procesar teclas y estado continuo
        running = handle_events(state, dt, events)




        # Obtener posición del mouse
        mouse_buttons = pygame.mouse.get_pressed()
        mouse_pos = pygame.mouse.get_pos()


        

        # Translation with mouse
        if mouse_buttons[0]:
            if not dragging:
                dragging = True
                last_mouse_pos = mouse_pos
            else:
                dx = mouse_pos[0] - last_mouse_pos[0]
                dy = mouse_pos[1] - last_mouse_pos[1]
                state['tx'] -= dx / (SCALE * state['scale'])  # adaptar al mapa
                state['ty'] -= dy / (SCALE * state['scale'])
                last_mouse_pos = mouse_pos
        else:
            dragging = False


        # Rotación con botón derecho
        if mouse_buttons[2]:  # botón derecho
            if not rotating:
                rotating = True
                last_rotation_pos = mouse_pos[0]
            else:
                dx = mouse_pos[0] - last_rotation_pos
                # Ajuste del ángulo (ajustable: más grande → más sensible)
                state['angle'] += dx * 0.2
                last_rotation_pos = mouse_pos[0]
        else:
            rotating = False

            

        # Build and compose transformation matrix
        operations = build_operations(state)
        if scroll_delta_y != 0.0:
            zoom_factor = 1.0 + scroll_delta_y * 0.05  # ajuste fino
            state['scale'] *= zoom_factor
            scroll_delta_y = 0.0
        matrix = compose_transformations(operations)

        # Apply transformation to all stars
        for star in stars:
            star.apply_transformation(matrix)

        # Clear screen
        screen.fill((0, 0, 0))

        # Render constellations and stars
        draw_stars(screen, stars, CENTER, SCALE)
        if state["constellations"]:
            draw_constellations(screen, constellations, CENTER, SCALE)
        if state["labels"]:
            draw_labels(screen, constellations, CENTER, SCALE, font)

        # Show overlay if active
        if state["overlay"]:
            overlay_surf = pygame.Surface((130, 280), pygame.SRCALPHA)
            overlay_surf.fill((0, 0, 0, 180))

            lines = [
                "Constellations Map",
                "----------------------------------",
                "Controls:",
                "[H] Toggle Help",
                "[R] Reset",
                "[F] Reflect",
                "[Q/E] Rotate",
                "[WASD] Move",
                "[+/-] Zoom",
                "[Z/X/C/V] Shear",
                "----------------------------------",
                "Values:",
                f"Constellations: {'On' if state['constellations'] else 'Off'}",
                f"Labels: {'On' if state['labels'] else 'Off'}",
                f"Angle: {state['angle']:.1f}",
                f"Scale: {state['scale']:.2f}",
                f"TX: {state['tx']:.2f}   TY: {state['ty']:.2f}",
                f"SHX: {state['shx']:.2f}  SHY: {state['shy']:.2f}",
                f"Reflect: {'Yes' if state['reflect'] else 'No'}"
            ]

            for i, text in enumerate(lines):
                text_surf = font.render(text, True, (255, 255, 255))
                overlay_surf.blit(text_surf, (10, 10 + i * 15))

            screen.blit(overlay_surf, (0, 0))

        pygame.display.flip()

    pygame.quit()    


if __name__ == '__main__':
    main()