
import pygame as pg
import math
import numpy as np
from rendering import world_to_camera


class Shape_Convex:
    def __init__(self, app, position, vertex_layout):
        self.app = app

        # Rotation
        self.rotation = 0
        self.rotation_matrix = self.calculate_rot_matrix()
        # Scale 
        self.scale = 1

        # Starting position
        self.pos = position

        # Vertices
        self.layout = vertex_layout
        self.vertices = vertex_layout.copy()
        self.bounding_box = Bounding_Box(self)
        self.calculate_vertices()

        self.colour = (240, 0, 0)

    def update(self):

        self.rotation_matrix = self.calculate_rot_matrix()
        self.calculate_vertices()

    def calculate_vertices(self):
        min_x, min_y = 999999, 999999
        max_x, max_y = -999999, -999999
        for index, offset in enumerate(self.layout):
            vertex = np.dot(self.rotation_matrix, (offset * self.scale))
            vertex = pg.Vector2(vertex[0], vertex[1]) + self.pos
            self.vertices[index] = vertex
            if vertex.x < min_x: min_x = vertex.x
            if vertex.x > max_x: max_x = vertex.x
            if vertex.y < min_y: min_y = vertex.y
            if vertex.y > max_y: max_y = vertex.y

        self.bounding_box.left = min_x
        self.bounding_box.right = max_x
        self.bounding_box.bottom = min_y
        self.bounding_box.top = max_y

    def calculate_rot_matrix(self):
        return [
            [math.cos(self.rotation), -math.sin(self.rotation)],
            [math.sin(self.rotation), math.cos(self.rotation)]
        ]

    def render(self):
        offset_positions = [world_to_camera(point) for point in self.vertices]
        pg.draw.lines(self.app.window, self.colour, True, offset_positions)

        #self.bounding_box.render()
        pg.draw.circle(self.app.window, self.colour, world_to_camera(self.pos), 2)

class Bounding_Box:
    def __init__(self, shape):
        self.app = shape.app
        self.colour = (220, 140, 10)
        
        self.top = 0
        self.bottom = 0
        self.left = 0
        self.right = 0

    def render(self):
        # Calculate vertex positions
        self.vertices = [
            pg.Vector2(self.left, self.top),
            pg.Vector2(self.right, self.top),
            pg.Vector2(self.right, self.bottom),
            pg.Vector2(self.left, self.bottom)
        ]
        # Render vertices
        offset_positions = [world_to_camera(point) for point in self.vertices]
        pg.draw.lines(self.app.window, self.colour, True, offset_positions)
