import pygame


def handle_events(state, dt):
    """
    Process user input to update transformation state.

    Parameters:
        state (dict): Camera state, expects keys:
            - cam_x, cam_y, cam_z (float): camera position
            - yaw, pitch, roll (float): camera orientation angles in degrees
            - move_speed (float): movement speed units per second
            - mouse_sens (float): mouse sensitivity for looking around
        dt (float): Time delta in seconds since last frame.
    
    Returns:
        bool: False if user requests quit, True otherwise.
    """
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            state['moving'] = True
            # Start capturing relative mouse movement
            pygame.mouse.get_rel()
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            state['moving'] = False

    # Always fetch mouse delta to clear internal queue
    mx, my = pygame.mouse.get_rel()
    
    if state.get('moving', False):
        # Keyboard movement
        keys = pygame.key.get_pressed()
        # Forward/back
        if keys[pygame.K_w]: state['cam_z'] += state['move_speed'] * dt
        if keys[pygame.K_s]: state['cam_z'] -= state['move_speed'] * dt
        # Left/right
        if keys[pygame.K_a]: state['cam_x'] -= state['move_speed'] * dt
        if keys[pygame.K_d]: state['cam_x'] += state['move_speed'] * dt
        # Up/down
        if keys[pygame.K_q]: state['cam_y'] -= state['move_speed'] * dt
        if keys[pygame.K_e]: state['cam_y'] += state['move_speed'] * dt

        # Mouse look (yaw/pitch)
        state['yaw']   += mx * state['mouse_sens']
        state['pitch'] -= my * state['mouse_sens']

        # Clamp pitch to avoid flip
        state['pitch'] = max(-89.9, min(89.9, state['pitch']))

    return True


def build_operations(state):
    """
    Build the list of 4x4 transformation dicts representing the inverse camera transform.
    
    The operations, in order, are:
      1) Translate by (-cam_x, -cam_y, -cam_z)
      2) Rotate around X by -pitch
      3) Rotate around Y by -yaw
      4) Rotate around Z by -roll

    Returns:
        list: List of dicts for compose_transformations.
    """
    operations = []
    operations.append({'type': 'rotate_y', 'angle': -state['yaw']})
    operations.append({'type': 'rotate_x', 'angle': -state['pitch']})
    operations.append({'type': 'rotate_z', 'angle': -state.get('roll', 0.0)})

    operations.append({
        'type': 'translate',
        'tx': -state['cam_x'],
        'ty': -state['cam_y'],
        'tz': -state['cam_z'],
    })
    return operations

