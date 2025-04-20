import pygame


def handle_events(state, dt, events):
    """
    Process user input to update transformation state.
    Returns False to quit, True to continue.

    state keys:
      - angle (float)
      - tx, ty (float)
      - scale (float)
      - reflect (bool)
      - shx, shy (float)
    dt: time delta in seconds since last frame
    """
    for event in events:
        if event.type == pygame.QUIT:
            return False

        if event.type == pygame.KEYDOWN:
            # Reflect toggle
            if event.key == pygame.K_f:
                state["reflect_x"] = not state["reflect_x"]
            elif event.key == pygame.K_g:
                state["reflect_y"] = not state["reflect_y"]
            # Reset
            elif event.key == pygame.K_r:
                state.update({
                    'angle': 0.0,
                    'tx': 0.0,
                    'ty': 0.0,
                    'scale': 0.3,
                    'reflect': False,
                    'shx': 0.0,
                    'shy': 0.0
                })
            # Overlay
            elif event.key == pygame.K_h:
                state["overlay"] = not state["overlay"]
            # Constelations on/off
            elif event.key == pygame.K_PERIOD:
                state["constellations"] = not state["constellations"]
            # Constellations names on/off
            elif event.key == pygame.K_l:
                state["labels"] = not state["labels"]
            # Stars HRs on/off
            elif event.key == pygame.K_k:
                state["show_hr"] = not state["show_hr"]
            

    # Continuos key state for smooth transforms
    keys = pygame.key.get_pressed()

    # Rotation (degrees per second)
    ROT_SPEED = 50
    rotation_sign = -1 if state.get("reflect_x") ^ state.get("reflect_y") else 1
    if keys[pygame.K_q] or keys[pygame.K_LEFT]:
        state["angle"] -= ROT_SPEED * dt * rotation_sign
    if keys[pygame.K_e] or keys[pygame.K_RIGHT]:
        state["angle"] += ROT_SPEED * dt * rotation_sign

    # Zoom (scale factor per second)
    ZOOM_SPEED = 1.005
    if keys[pygame.K_PLUS] or keys[pygame.K_EQUALS]:
        state['scale'] *= 1 + ZOOM_SPEED * dt
    if keys[pygame.K_MINUS]:
        state['scale'] /= 1 + ZOOM_SPEED * dt

    # Translation (units per second)
    TRANSLATION_SPEED = 5
    tx_sign = -1 if state.get("reflect_y") else 1
    ty_sign = -1 if state.get("reflect_x") else 1

    if keys[pygame.K_a]:
        state['tx'] -= TRANSLATION_SPEED * dt * tx_sign
    if keys[pygame.K_d]:
        state['tx'] += TRANSLATION_SPEED * dt * tx_sign
    if keys[pygame.K_w]:
        state['ty'] -= TRANSLATION_SPEED * dt * ty_sign
    if keys[pygame.K_s]:
        state['ty'] += TRANSLATION_SPEED * dt * ty_sign

    # Shear (factor per second)
    SHEAR_SPEED = 1.0
    if keys[pygame.K_x]:
        state['shx'] -= SHEAR_SPEED * dt
    if keys[pygame.K_z]:
        state['shx'] += SHEAR_SPEED * dt
    if keys[pygame.K_v]:
        state['shy'] -= SHEAR_SPEED * dt
    if keys[pygame.K_c]:
        state['shy'] += SHEAR_SPEED * dt    

    return True


def build_operations(state):
    """
    Build the list of transformation operations for compose_transformations().
    """
    operations = [
        {'type': 'rotate',    'angle': state['angle']},
        {'type': 'translate', 'tx': state['tx'], 'ty': state['ty']},
        {'type': 'scale',     'sx': state['scale'], 'sy': state['scale']},
    ]
    if state["reflect_x"] and state["reflect_y"]:
        operations.append({'type': 'reflect', 'axis': 'both'})
    elif state["reflect_x"]:
        operations.append({'type': 'reflect', 'axis': 'x'})
    elif state["reflect_y"]:
        operations.append({'type': 'reflect', 'axis': 'y'})
    if state['shx'] or state['shy']:
        operations.append({'type': 'shear', 'shx': state['shx'], 'shy': state['shy']})
    return operations

