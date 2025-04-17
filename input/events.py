import pygame


def handle_events(state):
    """
    Update "state" dict based on key presses/releases.
    Returns False if we must quit, else True.
    """
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            return False
        
        if e.type == pygame.KEYDOWN:
            
            # Rotation
            if e.key == pygame.K_LEFT:
                state["angle"] -= 5
            elif e.key == pygame.K_RIGHT:
                state["angle"] += 5

            # Zoom
            elif e.key in (pygame.K_PLUS, pygame.K_EQUALS):
                state["scale"] *= 1.1
            elif e.key == pygame.K_MINUS:
                state["scale"] /= 1.1

            # Translation
            elif e.key == pygame.K_w:
                state["ty"] += 10
            elif e.key == pygame.K_s:
                state["ty"] -= 10
            elif e.key == pygame.K_a:
                state["tx"] -= 10
            elif e.key == pygame.K_d:
                state["tx"] += 10

            # Reflect toggle
            elif e.key == pygame.K_f:
                state["reflect"] = not state["reflect"]

            # Shear
            elif e.key == pygame.K_LEFTBRACKET:
                state["shx"] -= 0.1
            elif e.key == pygame.K_RIGHTBRACKET:
                state["shx"] += 0.1
            elif e.key == pygame.K_LEFTBRACE:
                state["shy"] -= 0.1
            elif e.key == pygame.K_RIGHTBRACE:
                state["shy"] += 0.1          

            # Reset
            elif e.key == pygame.K_r:
                for k in ("angle","tx","ty","scale","reflect","shx","shy"):
                    state[k] = 0.0 if k not in ("reflect",) else False

    return True


def build_operations(state):
    """
    From `state`, produce the list of ops for compose_transformations().
    """
    ops = []
    ops.append({"type":"rotate", "angle": state["angle"]})
    ops.append({"type":"translate", "tx": state["tx"], "ty": state["ty"]})
    ops.append({"type":"scale", "sx": state["scale"], "sy": state["scale"]})
    if state["reflect"]:
        ops.append({"type":"reflect", "axis":"both"})
    if state["shx"] or state["shy"]:
        ops.append({"type":"shear", "shx": state["shx"], "shy": state["shy"]})
    return ops


