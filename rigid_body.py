
import pygame as pg
import numpy
import math

class Rigid_body:
    def __init__(self, app, shape, pos, vel, rot, angular_vel, mass, inertia, immoveable):
        self.app = app

        # Relative position of points where 0,0 is center of mass 
        self.shape = shape

        self.pos = pos.copy()
        self.vel = vel.copy()

        self.rotation = rot
        self.angular_vel = angular_vel

        self.mass = mass
        self.inertia = inertia
        self.immoveable = immoveable

        self.last_pos = pos.copy()
        self.last_rotation = rot

    def update(self):

        # Rotation
        self.last_pos = self.pos.copy()
        self.last_rotation = self.rotation

        self.d_rot = self.angular_vel * self.app.dt
        self.rotation += self.d_rot
        # Velocity
        self.d_pos = self.vel * self.app.dt
        self.pos += self.d_pos
        # Update shape
        self.shape.update(self.pos, self.rotation)

    def apply_force_local(self, force, relative_pos):
        pos = relative_pos.rotate_rad(self.rotation)
        n_force = force.rotate_rad(self.rotation)
        self.apply_force_external(n_force, pos)

    def apply_force_external(self, force, pos):

        impulse = force * self.app.dt
        self.vel += impulse / self.mass

        d_angular_momentum = cross(pos, impulse)
        self.angular_vel += d_angular_momentum / self.inertia

    def render(self):
        self.shape.render()

def rigid_body_collision(body_a, body_b, collision_point, normal, elasticity):
    # Using code from https://www.myphysicslab.com/engine2D/collision-en.html

    # Masses
    mass_a = body_a.mass
    mass_b = body_b.mass
    # Inertia
    inertia_a = body_a.inertia
    inertia_b = body_b.inertia
    # Relative position vectors
    relative_a_p = collision_point - body_a.pos
    relative_b_p = collision_point - body_b.pos
    # Initial angular velocities
    angular_a1 = body_a.angular_vel
    angular_b1 = body_b.angular_vel
    # Initital velocities of center of mass
    velocity_a1 = body_a.vel
    velocity_b1 = body_b.vel
    
    # Calculate velocity of collision point
    velocity_ap1 = velocity_a1 + (angular_a1 * pg.Vector2(-relative_a_p.y, relative_a_p.x))
    velocity_bp1 = velocity_b1 + (angular_b1 * pg.Vector2(-relative_b_p.y, relative_b_p.x))

    # Velocity of points approaching each other
    velocity_p1 = velocity_ap1 - velocity_bp1

    # Calculating impulse
    numerator = -(1 + elasticity) * (velocity_p1.dot(normal))
    masses = 0
    if not body_a.immoveable: masses += (1 / mass_a)
    if not body_b.immoveable: masses += (1 / mass_b)
    component_a = (cross(relative_a_p, normal) ** 2) / inertia_a
    component_b = (cross(relative_b_p, normal) ** 2) / inertia_b
    # If bodies are immoveable
    if body_a.immoveable: component_a = 0
    if body_b.immoveable: component_b = 0


    impulse = numerator / (masses + component_a + component_b)
    # Final linear velocities
    velocity_a2 = velocity_a1 + (impulse * normal) / mass_a
    velocity_b2 = velocity_b1 - (impulse * normal) / mass_b
    if body_a.immoveable: velocity_a2 = velocity_a1.copy()
    if body_b.immoveable: velocity_b2 = velocity_b1.copy()

    # Final angular velocities
    angular_a2 = angular_a1 + cross(relative_a_p, impulse * normal) / inertia_a
    angular_b2 = angular_b1 - cross(relative_b_p, impulse * normal) / inertia_b
    if body_a.immoveable: angular_a2 = angular_a1
    if body_b.immoveable: angular_b2 = angular_b1

    return velocity_a2, velocity_b2, angular_a2, angular_b2

def cross(v1, v2):
    return v1.x * v2.y - v1.y * v2.x
    


