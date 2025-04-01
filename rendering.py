
import pygame as pg
from config import PIXEL_PER_METER, WINDOW_SIZE

def world_to_camera(point):
    return pg.Vector2(
        (point.x * PIXEL_PER_METER) + (WINDOW_SIZE.x / 2),
        (-point.y * PIXEL_PER_METER) + (WINDOW_SIZE.y / 2)
    )