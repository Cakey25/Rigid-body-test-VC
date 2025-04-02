
import pygame as pg
import math

from rigid_body import Rigid_body
from shape import Shape_Convex

class Player:
    def __init__(self, app, pos):
        self.app = app

        self.shape = Shape_Convex(
            app=app,
            position=pg.Vector2(0, 0),
            vertex_layout=[
                pg.Vector2(0.6, 0),
                pg.Vector2(0.3, 0.5),
                pg.Vector2(-0.3, 0.5),
                pg.Vector2(-0.35, 0),
                pg.Vector2(-0.3, -0.5),
                pg.Vector2(0.3, -0.5)
            ]
        )
        self.rigid = Rigid_body(
            app=app,
            shape=self.shape,
            pos=pos,
            vel=pg.Vector2(0, 0),
            rot=math.pi / 2,
            angular_vel=0,
            mass=2,
            inertia=2,
            immoveable=False,
        )

        self.shape.rotation = self.rigid.rotation

    def update(self):
        
        # Moving forwards and backwards
        if self.app.keys[pg.K_w] and not self.app.keys[pg.K_s]:
            self.rigid.apply_force_local(
                force=pg.Vector2(20, 0),
                relative_pos=pg.Vector2(0 , 0))

        if self.app.keys[pg.K_s] and not self.app.keys[pg.K_w]:
            self.rigid.apply_force_local(
                force=pg.Vector2(-20, 0),
                relative_pos=pg.Vector2(0, 0))

        # Rotating clockwise and anticlockwise 
        if self.app.keys[pg.K_d] and not self.app.keys[pg.K_a]:
            self.rigid.apply_force_local(
                force=pg.Vector2(0, 10),
                relative_pos=pg.Vector2(-1, 0))
            self.rigid.apply_force_local(
                force=pg.Vector2(0, -10),
                relative_pos=pg.Vector2(1, 0))

        if self.app.keys[pg.K_a] and not self.app.keys[pg.K_d]:
            self.rigid.apply_force_local(
                force=pg.Vector2(0, -10),
                relative_pos=pg.Vector2(-1, 0))
            self.rigid.apply_force_local(
                force=pg.Vector2(0, 10),
                relative_pos=pg.Vector2(1, 0))

        # Linear drag
        if self.rigid.vel.length_squared() != 0:
            linear_drag = pg.Vector2(0, 0)
            velocity_normalized = self.rigid.vel.normalize()
            # Calculate the linear drag
            linear_drag += 1 * -velocity_normalized * self.rigid.vel.dot(self.rigid.vel)
            linear_drag += 0 * -velocity_normalized * self.rigid.vel.length()
            linear_drag += 0.2 * -velocity_normalized
            # Apply drag force
            self.rigid.apply_force_external(linear_drag, pg.Vector2(0, 0))

        # Angular drag 
        if self.rigid.angular_vel != 0:
            relative_point = pg.Vector2(-1, 0)
            drag_direction = self.rigid.angular_vel / abs(self.rigid.angular_vel)
            angular_drag = 0
            # Calculate the angular drag
            angular_drag += 0.5 * -drag_direction * self.rigid.angular_vel ** 2
            angular_drag += 0 * -drag_direction * self.rigid.angular_vel
            angular_drag += 0.2 * -drag_direction
            # Apply drag force
            rotational_force = pg.Vector2(0, angular_drag)
            self.rigid.apply_force_local(rotational_force, -relative_point)
            self.rigid.apply_force_local(-rotational_force, relative_point)
        
        self.rigid.update()

    def render(self):
        self.shape.render()
