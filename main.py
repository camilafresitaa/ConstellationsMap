import pygame
from stars.stars import load_stars
from constellations.constellations import load_constellations
from renderer.draw import draw_stars, draw_constellations, draw_labels, draw_hr_labels
from scr.transformations import compose_transformations
from input.events import handle_events, build_operations


# Simulation constants
FPS = 60
SCALE = 1000
DEFAULT_ZOOM = 0.4
MOUSE_TRANSLATION_SPEED = 2.0 


def main():
    """
    Entry point for the constellation visualizer.
    Initializes the window, loads data, and runs the main loop.
    """
    # INITIALIZE PYGAME
    pygame.init()
    pygame.display.set_caption("Constellations Map")

    # FONTS
    font_title = pygame.font.SysFont(None, 20)
    font_text = pygame.font.SysFont(None, 17)
    font_const = pygame.font.SysFont(None, 17)
    font_hr = pygame.font.SysFont(None, 14)

    info = pygame.display.Info()
    WIDTH = info.current_w
    HEIGHT = info.current_h
    CENTER = (WIDTH // 2, HEIGHT // 2)
    screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
    clock = pygame.time.Clock()

    # LOAD DATA
    stars, RA0, Dec0 = load_stars()
    star_lookup = {star.hr: star for star in stars}
    constellations = load_constellations(star_lookup, RA0, Dec0)

    # INITIAL STATE
    state = {
        "angle": 0.0,
        "tx": 0.0,
        "ty": 0.0,
        "scale": DEFAULT_ZOOM,
        "reflect_x": False,
        "reflect_y": False,
        "shx": 0.0,
        "shy": 0.0,
        "overlay": True,
        "constellations": True,
        "labels": True,
        "show_hr": False
    }

    dragging = False
    last_mouse_pos = (0, 0)
    scroll_delta_y = 0.0

    rotating = False
    last_rotation_pos = 0

    running = True
    while running:
        # TIME
        dt = clock.tick(FPS) / 1000.0

        # INPUT
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEWHEEL:
                scroll_delta_y += event.y

        running = handle_events(state, dt, events)

        # MOUSE INTERACTION
        mouse_buttons = pygame.mouse.get_pressed()
        mouse_pos = pygame.mouse.get_pos()

        # Drag to translate
        if mouse_buttons[0]:
            if not dragging:
                dragging = True
                last_mouse_pos = mouse_pos
            else:
                dx = mouse_pos[0] - last_mouse_pos[0]
                dy = mouse_pos[1] - last_mouse_pos[1]

                dx_sign = -1 if state.get("reflect_y", False) else 1
                dy_sign = -1 if state.get("reflect_x", False) else 1

                state["tx"] -= dx * dx_sign * MOUSE_TRANSLATION_SPEED / (SCALE * state["scale"])
                state["ty"] -= dy * dy_sign * MOUSE_TRANSLATION_SPEED / (SCALE * state["scale"])

                last_mouse_pos = mouse_pos
        else:
            dragging = False


        # Drag right mouse to rotate
        if mouse_buttons[2]:
            if not rotating:
                rotating = True
                last_rotation_pos = mouse_pos[0]
            else:
                dx = mouse_pos[0] - last_rotation_pos
                state["angle"] += dx * 0.2  # Sensitivity
                last_rotation_pos = mouse_pos[0]
        else:
            rotating = False

        # TRANSFORM
        operations = build_operations(state)
        if scroll_delta_y != 0.0:
            zoom_factor = 1.0 + scroll_delta_y * 0.05
            state["scale"] *= zoom_factor
            scroll_delta_y = 0.0
        matrix = compose_transformations(operations)

        for star in stars:
            star.apply_transformation(matrix)

        # DRAW
        screen.fill((0, 0, 0))

        draw_stars(screen, stars, CENTER, SCALE * state["scale"], zoom_level=state["scale"])
        if state["show_hr"]:
            draw_hr_labels(screen, stars, CENTER, SCALE * state["scale"], state["scale"], font_hr)
        if state["labels"]:
            draw_labels(screen, constellations, CENTER, SCALE * state["scale"], font_const)
        if state["constellations"]:
            draw_constellations(screen, constellations, CENTER, SCALE * state["scale"])

        # OVERLAY
        if state["overlay"]:
            overlay_surf = pygame.Surface((150, 480), pygame.SRCALPHA)
            overlay_surf.fill((0, 0, 0, 180))

            lines = [
                "Constellations Map",
                "----------------------------------",
                "Controls:",
                "[H] Toggle Help",
                "[.] Show Constellations",
                "[L] Show Names",
                "[K] Show Stars HRs",
                "[R] Reset",
                "[+/-] Zoom",
                "[Q/E] Rotate",
                "[WASD] Move",
                "[Z/X] Shear X",
                "[C/V] Shear Y",
                "[F] Reflect X",
                "[G] Reflect Y",
                "----------------------------------",
                "Values:",
                f"Constellations: {"On" if state["constellations"] else "Off"}",
                f"Names: {"On" if state["labels"] else "Off"}",
                f"Stars HRs: {"On" if state["show_hr"] else "Off"}",
                f"Zoom: {state["scale"] / DEFAULT_ZOOM:.2f}x",
                f"Angle: {state["angle"]:.1f}",
                f"TX: {state["tx"]:.2f}   TY: {state["ty"]:.2f}",
                f"SHX: {state["shx"]:.2f}  SHY: {state["shy"]:.2f}",
                f"Reflect X: {"Yes" if state["reflect_x"] else "No"}",
                f"Reflect Y: {"Yes" if state["reflect_y"] else "No"}",
            ]

            for i, text in enumerate(lines):
                y = 15 + i * 18
                if text == "Constellations Map":
                    font = font_title
                    color = (255, 255, 255)
                elif text.strip().endswith(":"):
                    font = font_text
                    color = (255, 255, 255)
                elif text.startswith("["):
                    font = font_text
                    color = (190, 190, 190)
                else:
                    font = font_text
                    color = (190, 190, 190)
                text_surf = font.render(text, True, color)
                overlay_surf.blit(text_surf, (15, y))

            screen.blit(overlay_surf, (0, 0))

        pygame.display.flip()

    pygame.quit()    


if __name__ == '__main__':
    main()