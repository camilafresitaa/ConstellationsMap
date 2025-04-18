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
                state["reflect"] = not state["reflect"]
            # Reset
            elif event.key == pygame.K_r:
                state.update({
                    'angle': 0.0,
                    'tx': 0.0,
                    'ty': 0.0,
                    'scale': 1.0,
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
            elif event.key == pygame.K_l:
                state["labels"] = not state["labels"]
            

    # Continuos key state for smooth transforms
    keys = pygame.key.get_pressed()

    # Rotation (degrees per second)
    ROT_SPEED = 30
    if keys[pygame.K_q]:
        state["angle"] -= ROT_SPEED * dt
    if keys[pygame.K_e]:
        state['angle'] += ROT_SPEED * dt

    # Zoom (scale factor per second)
    ZOOM_SPEED = 1.005
    if keys[pygame.K_PLUS] or keys[pygame.K_EQUALS]:
        state['scale'] *= 1 + ZOOM_SPEED * dt
    if keys[pygame.K_MINUS]:
        state['scale'] /= 1 + ZOOM_SPEED * dt

    # Translation (units per second)
    TRANSLATION_SPEED = 2
    if keys[pygame.K_a]:
        state['tx'] -= TRANSLATION_SPEED * dt
    if keys[pygame.K_d]:
        state['tx'] += TRANSLATION_SPEED * dt
    if keys[pygame.K_w]:
        state['ty'] -= TRANSLATION_SPEED * dt
    if keys[pygame.K_s]:
        state['ty'] += TRANSLATION_SPEED * dt

    # Shear (factor per second)
    SHEAR_SPEED = 1.0
    if keys[pygame.K_z]:
        state['shx'] -= SHEAR_SPEED * dt
    if keys[pygame.K_x]:
        state['shx'] += SHEAR_SPEED * dt
    if keys[pygame.K_c]:
        state['shy'] -= SHEAR_SPEED * dt
    if keys[pygame.K_v]:
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
    if state['reflect']:
        operations.append({'type': 'reflect', 'axis': 'both'})
    if state['shx'] or state['shy']:
        operations.append({'type': 'shear', 'shx': state['shx'], 'shy': state['shy']})
    return operations

