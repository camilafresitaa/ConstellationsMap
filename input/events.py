import pygame


def handle_events(state, dt, events):
    """
    Process user input (keyboard and quit events) to update the transformation state.

    Parameters:
        state (dict): Holds transformation state variables:
            - angle (float): rotation in degrees
            - tx, ty (float): translation offsets
            - scale (float): zoom level
            - reflect_x, reflect_y (bool): axis reflection flags
            - shx, shy (float): shear values
            - overlay (bool): help overlay toggle
            - constellations, labels, show_hr (bool): display toggles
        dt (float): Time delta since last frame (in seconds)
        events (list): List of Pygame events from pygame.event.get()

    Returns:
        bool: False if quitting, True otherwise.
    """
    for event in events:
        if event.type == pygame.QUIT:
            return False

        if event.type == pygame.KEYDOWN:
            # Reflection
            if event.key == pygame.K_f:
                state["reflect_x"] = not state["reflect_x"]
            elif event.key == pygame.K_g:
                state["reflect_y"] = not state["reflect_y"]
            # Reset all transformations
            elif event.key == pygame.K_r:
                state.update({
                    "angle": 0.0,
                    "tx": 0.0,
                    "ty": 0.0,
                    "scale": 0.4,
                    "reflect": False,
                    "shx": 0.0,
                    "shy": 0.0
                })
            # Help overlay
            elif event.key == pygame.K_h:
                state["overlay"] = not state["overlay"]
            # Constelations on/off
            elif event.key == pygame.K_PERIOD:
                state["constellations"] = not state["constellations"]
            # Constellations names on/off
            elif event.key == pygame.K_l:
                state["labels"] = not state["labels"]
            # Stars HR labels on/off
            elif event.key == pygame.K_k:
                state["show_hr"] = not state["show_hr"]

    # Continuos key state (held keys)
    keys = pygame.key.get_pressed()

    # Rotation (degrees per second)
    ROT_SPEED = 50
    # Reverse rotation direction if reflected
    rotation_sign = -1 if state.get("reflect_x") ^ state.get("reflect_y") else 1
    if keys[pygame.K_q] or keys[pygame.K_LEFT]:
        state["angle"] -= ROT_SPEED * dt * rotation_sign
    if keys[pygame.K_e] or keys[pygame.K_RIGHT]:
        state["angle"] += ROT_SPEED * dt * rotation_sign

    # Zoom (scale factor per second)
    ZOOM_SPEED = 1.005
    if keys[pygame.K_PLUS] or keys[pygame.K_EQUALS]:
        state["scale"] *= 1 + ZOOM_SPEED * dt
    if keys[pygame.K_MINUS]:
        state["scale"] /= 1 + ZOOM_SPEED * dt

    # Translation (units per second)
    TRANSLATION_SPEED = 5
    tx_sign = -1 if state.get("reflect_y") else 1
    ty_sign = -1 if state.get("reflect_x") else 1

    if keys[pygame.K_a]:
        state["tx"] -= TRANSLATION_SPEED * dt * tx_sign
    if keys[pygame.K_d]:
        state["tx"] += TRANSLATION_SPEED * dt * tx_sign
    if keys[pygame.K_w]:
        state["ty"] -= TRANSLATION_SPEED * dt * ty_sign
    if keys[pygame.K_s]:
        state["ty"] += TRANSLATION_SPEED * dt * ty_sign

    # Shear (factor per second)
    SHEAR_SPEED = 1.0
    if keys[pygame.K_x]:
        state["shx"] -= SHEAR_SPEED * dt
    if keys[pygame.K_z]:
        state["shx"] += SHEAR_SPEED * dt
    if keys[pygame.K_v]:
        state["shy"] -= SHEAR_SPEED * dt
    if keys[pygame.K_c]:
        state["shy"] += SHEAR_SPEED * dt    

    return True


def build_operations(state):
    """
    Construct the list of transformations to be composed in the correct order.

    Parameters:
        state (dict): Same as in handle_events.

    Returns:
        list: List of transformation operation dictionaries.
    """
    operations = [
        {"type": "rotate",    "angle": state["angle"]},
        {"type": "translate", "tx": state["tx"], "ty": state["ty"]},
        {"type": "scale",     "sx": state["scale"], "sy": state["scale"]},
    ]
    # Add reflections
    if state["reflect_x"] and state["reflect_y"]:
        operations.append({"type": "reflect", "axis": "both"})
    elif state["reflect_x"]:
        operations.append({"type": "reflect", "axis": "x"})
    elif state["reflect_y"]:
        operations.append({"type": "reflect", "axis": "y"})

    # Add shear if any
    if state["shx"] or state["shy"]:
        operations.append({"type": "shear", "shx": state["shx"], "shy": state["shy"]})

    return operations

