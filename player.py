
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
        
        if self.app.keys[pg.K_w] and not self.app.keys[pg.K_s]:
            self.rigid.apply_force_local(
                force=pg.Vector2(20, 0),
                relative_pos=pg.Vector2(0 , 0))
        if self.app.keys[pg.K_s] and not self.app.keys[pg.K_w]:
            self.rigid.apply_force_local(
                force=pg.Vector2(-20, 0),
                relative_pos=pg.Vector2(0, 0))
        
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

        # Drag
        if self.rigid.vel.length() != 0:
            proportional_drag = -self.rigid.vel.normalize() * self.rigid.vel.dot(self.rigid.vel) * 1
        else:
            proportional_drag = pg.Vector2(0, 0)

        self.rigid.apply_force_external(proportional_drag, pg.Vector2(0, 0))

        if self.rigid.vel.length() != 0:
            linear_drag = -self.rigid.vel.normalize() * 0.2 # Drag coefficient
        else:
            linear_drag = pg.Vector2(0, 0)

        self.rigid.apply_force_external(linear_drag, pg.Vector2(0, 0))

        # Angular drag
        relative_point = pg.Vector2(1, 0)
        if self.rigid.angular_vel != 0:
            proportional_angular_drag = -0.5 * self.rigid.angular_vel ** 3 / abs(self.rigid.angular_vel)
        else:
            proportional_angular_drag = 0
        rotational_force = pg.Vector2(0, 1) * proportional_angular_drag

        self.rigid.apply_force_local(rotational_force, relative_point)
        self.rigid.apply_force_local(rotational_force * -1, relative_point * -1)

        if self.rigid.angular_vel != 0:
            linear_angular_vel = -0.2 * self.rigid.angular_vel / abs(self.rigid.angular_vel)
        else:
            linear_angular_vel = 0
        rotational_force = pg.Vector2(0, 1) * linear_angular_vel

        self.rigid.apply_force_local(rotational_force, relative_point)
        self.rigid.apply_force_local(rotational_force * -1, relative_point * -1)

        # This is bad code
        
        self.rigid.update()

    def render(self):
        self.shape.render()
