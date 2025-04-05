
import pygame as pg
import math
import numpy as np

from config import PIXEL_PER_METER, WINDOW_SIZE

def camera_to_window(point):
    return pg.Vector2(
        (point.x * PIXEL_PER_METER) + (WINDOW_SIZE.x / 2),
        (-point.y * PIXEL_PER_METER) + (WINDOW_SIZE.y / 2)
    )

def world_to_camera(point, camera):
    image = np.dot(camera.matrix, (point - camera.pos) * camera.scale)
    image = pg.Vector2(image[0], image[1])
    return camera_to_window(image)

class Camera2D:
    def __init__(self, app):
        self.app = app

        self.pos = pg.Vector2(0, 0)
        self.rot = 0
        self.scale = 1

        self.matrix = [[1, 0], [0, 1]] # Identity

    def update(self, pos, rot):
        # Update position
        self.pos = pos
        self.rot = rot
        # Calculate new matrix
        self.matrix = [
            [math.cos(-self.rot), -math.sin(-self.rot)],
            [math.sin(-self.rot), math.cos(-self.rot)]
        ]
        
