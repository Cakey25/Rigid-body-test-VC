
import pygame as pg
import math

from config import PIXEL_PER_METER, WINDOW_SIZE

class Spring:
    def __init__(self, app):
        
        self.app = app
        # Position of the anchors
        self.pos_1 = pg.Vector2(0, 0)
        self.pos_2 = pg.Vector2(0, -1)

        self.vel = pg.Vector2(0, 0)
        # Spring values
        self.tension = pg.Vector2(0, 0)
        self.tension_mag = 0

        self.natural_length = 1
        self.extension = self.pos_1.distance_to(self.pos_2) - self.natural_length

        self.elasticity = 10
        self.damping = 0

    def calculate_critical_damping(self, mass):
        self.damping = 2 * math.sqrt(mass * self.elasticity / self.natural_length)

    def calculate_tension(self):
        
        self.extension = self.pos_1.distance_to(self.pos_2) - self.natural_length
        self.tension_mag = (self.extension * self.elasticity / self.natural_length) - self.damping * self.vel
        self.tension = (self.pos_1 - self.pos_2).normalize() * self.tension_mag

    def set_anchors(self, pos_1, pos_2):
        # Set positions
        self.pos_1 = pos_1
        self.pos_2 = pos_2

        # Calculate velocity of spring
        dx = float(self.extension)
        self.extension = self.pos_1.distance_to(self.pos_2) - self.natural_length
        dx -= self.extension
        self.vel = dx / self.app.dt

    def update(self, pos_1, pos_2):
        self.set_anchors(pos_1, pos_2)
        self.calculate_tension()

    def render(self):
        # Convert points to world space
        p1 = self.pos_1.copy()
        p2 = self.pos_2.copy()
        p1.y = -p1.y
        p2.y = -p2.y
        p1 = (p1 * PIXEL_PER_METER) + (WINDOW_SIZE / 2)
        p2 = (p2 * PIXEL_PER_METER) + (WINDOW_SIZE / 2)

        # Draw spring
        pg.draw.circle(self.app.window, (20, 200, 30), p1, 5)
        pg.draw.circle(self.app.window, (20, 200, 30), p2, 5)
        pg.draw.line(self.app.window, (20, 200, 30), p1, p2, 4)
