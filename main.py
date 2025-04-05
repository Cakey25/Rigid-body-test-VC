
# Imports
import pygame as pg
import sys
import numpy
import time
import math
# Modules
from config import WINDOW_SIZE, FPS_TARGET, PIXEL_PER_METER
from rigid_body import Rigid_body, rigid_body_collision
from spring import Spring
from shape import Shape_Convex
from collision import seperating_axis, bounding_box, polygon_polygon 
from collision import find_collision_points, find_normals, calc_midpoint
from player import Player
from rendering import Camera2D, world_to_camera


class Game_Engine:
    def __init__(self):
        self.window = pg.display.set_mode(WINDOW_SIZE, display=0)
        self.clock = pg.Clock()

        self.running = True
        self.dt = 0.01
        self.unfocused = False
        
        self.shape_scene()

    def shape_scene(self):

        self.camera = Camera2D(self)
        self.camera.update(pg.Vector2(0, 0), 0)
        self.camera.scale = 0.5

        # Convension that point orders will always go anticlockwise
        self.shape1 = Shape_Convex(
            app=self,
            position=pg.Vector2(-1, 0.25),
            vertex_layout=[
                pg.Vector2(-0.5, -0.5),
                pg.Vector2(-0.25, -0.5),
                pg.Vector2(0.4, 0),
                pg.Vector2(-0.25, 0.5),
                pg.Vector2(-0.5, 0.5)
        ])

        # Convension that point orders will always go anticlockwise
        self.shape2 = Shape_Convex(
            app=self, 
            position=pg.Vector2(1, 0),
            vertex_layout=[
                pg.Vector2(0.125, 0.5),
                pg.Vector2(-0.125, 0.5),
                pg.Vector2(-0.125, -0.5),
                pg.Vector2(0.125, -0.25)
        ])

        self.rigid1 = Rigid_body(self, self.shape2, pg.Vector2(1, 0), pg.Vector2(0, 0), 0, 4, 2, 0.5, True)
        self.player = Player(self, pg.Vector2(0, 0))

    def events(self):
        
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.running = False

            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.running = False

            if event.type == pg.WINDOWLEAVE:
                self.unfocused = True
            if event.type == pg.WINDOWENTER:
                self.unfocused = False
                engine.clock.tick()

        self.mouse_pos = pg.mouse.get_pos()
        self.mouse_pos = pg.Vector2(WINDOW_SIZE / 2)

        self.keys = pg.key.get_pressed()

    def update(self):

        self.rigid1.update()
        self.player.update()

        self.camera.update(self.player.rigid.pos, self.player.rigid.rotation - math.pi / 2)

        # Doing collisions between 2 shapes
        if bounding_box(self.rigid1.shape, self.player.shape): #0.01
            if seperating_axis(self.rigid1.shape, self.player.shape): #0.21
                collisions = polygon_polygon(self.rigid1.shape, self.player.shape) # 0.22
                points = find_collision_points(collisions) # saved 0.05
                normal = find_normals(collisions, points)
                # Constrain points
                if len(points) == 2:
                    point = calc_midpoint(points[0], points[1])
                else:
                    point = points[0]
                # Could do collisions between the lines conserned if want more accurate collisions
                # The one that contains the point must be rigid1

                v1, v2, a1, a2 = rigid_body_collision(self.rigid1, self.player.rigid, point, normal, 1)
                self.rigid1.vel = v1.copy()
                self.player.rigid.vel = v2.copy()
                self.rigid1.angular_vel = a1
                self.player.rigid.angular_vel = a2

                self.rigid1.pos = self.rigid1.last_pos.copy()
                self.player.rigid.pos = self.player.rigid.last_pos.copy()

                self.rigid1.rotation = self.rigid1.last_rotation
                self.player.rigid.rotation = self.player.rigid.last_rotation

        pg.display.set_caption(f'{self.clock.get_fps() :.0f}')
                
    def render(self):
        self.window.fill((20, 40, 60))

        ##### Bad line code to show how player is moving with camera
        pos = self.player.rigid.pos
        x_trunc = math.floor(pos.x)
        y_trunc = math.floor(pos.y)
        x_min = x_trunc - 8
        x_max = x_trunc + 8
        y_min = y_trunc - 8
        y_max = y_trunc + 8
        step = 1
        colour = (10, 10, 10)

        for x in range(x_min, x_max, step):
            p1 = world_to_camera(pg.Vector2(x, y_min), self.camera)
            p2 = world_to_camera(pg.Vector2(x, y_max), self.camera)
            pg.draw.line(self.window, colour, p1, p2)

        for y in range(y_min, y_max, step):
            p1 = world_to_camera(pg.Vector2(x_min, y), self.camera)
            p2 = world_to_camera(pg.Vector2(x_max, y), self.camera)
            pg.draw.line(self.window, colour, p1, p2)
        #### End of bad code

        self.player.render()
        self.rigid1.render()

        pg.display.flip()

        


if __name__ == '__main__':

    engine = Game_Engine()

    while engine.running:
        
        engine.events()
        if not engine.unfocused:
            # To fix this issue with focus, I can take a snapshot when the mouse leaves
            # The window and check if the window has moved since then and if it has
            # Set the simulation to the snapshot otherwise it can continue to run
            engine.update()
            # Physics needs to have a constant delta time really
            engine.dt = engine.clock.tick(FPS_TARGET) / 1000
            engine.dt = 1 / FPS_TARGET
            engine.render()
    pg.quit()
    sys.exit()


# Want to have important objects in the world class
# could create new classes for different worlds that inherit the world class and define new objects
# the world classes would contain the chunks of the world that should have the tiles. 
# Can have a list of physical objects that dont move in the chunk class like fences or trees that have collision
# List of things that are interactable
# List of things that enemies and npcs in the world class as they would decide what chunks are updated
# other classes that aren't world class would be ones for the menu and classes to handle assets and render things

