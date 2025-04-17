import sys
import pygame
import numpy as np
from stars.stars import load_stars
from constellations.constellations import load_constellations
from renderer.draw import draw_stars, draw_constellations
from input.events import handle_events, build_operations
from scr.transformations import (compose_transformations, perspective_matrix, translation_matrix, rotation_x_matrix, rotation_y_matrix, rotation_z_matrix,
scaling_matrix, reflection_matrix, shearing_matrix)


# Configuration & Initialization
FPS = 60
pygame.init()
info = pygame.display.Info()
WIDTH, HEIGHT = info.current_w, info.current_h
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
ASPECT = WIDTH / HEIGHT

# Camera and projection state
default_state = {
    'cam_x': 0.0,
    'cam_y': 0.0,
    'cam_z': 0.0,
    'pitch': 0.0,   # rotation around X
    'yaw': 0.0,     # rotation around Y
    'roll': 0.0,    # rotation around Z
    'fov': 30.0,
    'near': 0.1,
    'far': 1000.0,
    'move_speed': 10.0,  # Units per second
    'mouse_sens':  0.1,  # Degrees per pixel of mouse movement
}
state = default_state.copy()

# Load stars & constellations
stars = load_stars()
star_lookup = {star.hr: star for star in stars}
constellations = load_constellations(star_lookup)


# == Nuevo cálculo de 'far' basado en paralaje real ==
# Calculamos la distancia máxima de cualquier estrella al origen
max_dist = max(
    np.linalg.norm(star.base_homogeneous[:3])
    for star in stars
)
# Ajustamos el far plane a un poco más allá de la estrella más lejana
state['far'] = max_dist * 1.1


def main():
    running = True
    while running:
        # Compute delta time (seconds)
        dt = clock.tick(FPS) / 1000.0

        # 1) Handle input, update state
        running = handle_events(state, dt)

        # 2) Build model-view (camera) transformations
        SCALE = 3.0
        operations = []
        operations.append({'type':'scale', 'sx':SCALE, 'sy':SCALE, 'sz':SCALE})

        # 2) Construir matrices de transformaciones

        # 2a) Skybox de estrellas: SOLO rotaciones (ignora traslación)
        ops_sky = [
            {'type': 'rotate_y', 'angle': -state['yaw']},
            {'type': 'rotate_x', 'angle': -state['pitch']},
            {'type': 'rotate_z', 'angle': -state['roll']},
        ]
        M_sky = compose_transformations(ops_sky)

        # 2b) Escena completa: escalado, espejado, cizallamiento + inversa de cámara
        SCALE = 2.0       # ajusta para separar más o menos tus objetos
        SHEAR_XY = 0.3    # cizalla X en función de Y
        ops_scene = [
            # Escalado global
            {'type': 'scale', 'sx': SCALE, 'sy': SCALE, 'sz': SCALE},
            # Espejado en X (puedes usar 'y' o 'z')
            {'type': 'reflect', 'axis': 'x'},
            # Cizallamiento: x += shxy * y
            {'type': 'shear', 'shxy': SHEAR_XY, 'shxz': 0,
                             'shyx': 0,      'shyz': 0,
                             'shzx': 0,      'shzy': 0},
            # Invertir cámara: traslación inversa
            {'type': 'translate',
             'tx': -state['cam_x'], 'ty': -state['cam_y'], 'tz': -state['cam_z']},
            # Invertir rotaciones
            {'type': 'rotate_z', 'angle': -state['roll']},
            {'type': 'rotate_x', 'angle': -state['pitch']},
            {'type': 'rotate_y', 'angle': -state['yaw']},
        ]
        M_scene = compose_transformations(ops_scene)


        # 3) Perspective projection + culling + depth info
        P  = P     = perspective_matrix(state['fov'], ASPECT, state['near'], state['far'])
        # Primero proyectamos en espacio cámara (model-view) y guardamos la profundidad


        for star in stars:
            # 3a) Transformar con M_sky (solo rotaciones)
            view_hom = M_sky @ star.base_homogeneous
            # Frustum culling: solo si está entre near y far y delante (vz > 0)
            # if vz < state['near'] or vz > state['far']:
            #     star.visible = False
            #     continue


            # star.visible = True
            # star.view_z = vz



            # Ahora aplicamos P para obtener clip-space
            clip_hom = P @ view_hom
            x_h, y_h, _, w_h = clip_hom
            x_ndc = x_h / w_h
            y_ndc = y_h / w_h
            # NDC (-1..1) → coordenadas de pantalla
            star.x = ( x_ndc + 1) * 0.5 * WIDTH
            star.y = (1 - y_ndc) * 0.5 * HEIGHT

        # Render
        screen.fill((0,0,0))

        # Draw constellations
        draw_constellations(screen, constellations)

        # Draw stars
        visible = [s for s in stars if getattr(s, 'visible', False)]
        visible.sort(key=lambda s: s.view_z, reverse=True)
        draw_stars(screen, visible,
                   depth_near=state['near'], depth_far=state['far'])
        pygame.display.flip()

    pygame.quit()    
    sys.exit()

if __name__ == '__main__':
    main()