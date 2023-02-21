from typing import Type

import random

import json
from pygame.math import Vector2
import pygame


class MasterParticle:
    def __init__(self, pos: Vector2, file, particle_name, shape='circle',screenWidth=1500,screenHeight=1500):
        self.playing = True
        self.particles = []
        self.counter = 0
        self.pos = pos

        self.screenWidth = screenWidth
        self.screenHeight = screenHeight

        with open(file) as f:
            properties = json.load(f)

        properties = properties[particle_name]

        self.gravity_horizontal = properties['gravity_horizontal']
        self.gravity_vertical = properties['gravity_vertical']
        self.horizontal_force = properties['horizontal_force']
        self.vertical_force = properties['vertical_force']
        self.particles_per_sec = properties['particles_per_sec']
        self.life = properties['life']
        self.life_span = properties['life_span']
        self.color1 = properties['color1']
        self.color2 = properties['color2']

        self.gravity = Vector2(self.gravity_horizontal, self.gravity_vertical)
        self.force = Vector2(self.horizontal_force, self.vertical_force)

        self.shape = shape

        self.particles = []

    def play(self):
        self.playing = True

    def stop(self):
        self.playing = False

    def is_playing(self):
        return self.playing

    def update(self, win):

        if self.playing:
            self.counter += 1

            if self.counter % self.particles_per_sec == 0:
                self.particles.append(
                    Particle(Vector2(self.pos), Vector2(0, 0), self.color1, life=self.life, life_span=self.life_span,
                             gravity=self.gravity, color2=self.color2, shape=self.shape))

        for _x, p in enumerate(self.particles):
            p.vel[0] = random.randint(int(-self.force.x), int(self.force.x)) / (p.life * 2) * 25
            p.vel[1] = random.randint(int(-self.force.y), int(self.force.y)) / (p.life * 2) * 25
            p.update()

            if len(self.particles) > _x:
                if p.loc.x <= -15:
                    self.particles.pop(_x)
                if p.loc.x >= self.screenWidth + 15:
                    self.particles.pop(_x)

                if p.loc.y <= -15:
                    self.particles.pop(_x)

                if p.loc.y >= self.screenHeight + 15:
                    self.particles.pop(_x)

            p.draw(win)

            if p.life <= 0:
                if len(self.particles) > _x:
                    self.particles.pop(_x)


class Particle:
    TRIANGLE = 'triangle'
    CIRCLE = 'circle'
    RECT = 'rect'

    def __init__(self, loc: Vector2, start_vel: Vector2, color, life, life_span=.1, gravity=Type[Vector2],
                 color2=(0, 0, 0), shape="" or pygame.Surface):
        self.life = life
        self.life_span = self.life / life_span / 60
        self.life_span *= 2
        self.loc = loc
        self.color = color
        self.color_ori = self.color
        self.color2 = color2
        self.vel = start_vel
        self.gravity = gravity
        self.shape = shape

    def draw(self, win):
        if self.shape == Particle.CIRCLE:
            pygame.draw.circle(win, self.color, (self.loc[0], self.loc[1]), self.life)
        elif self.shape == Particle.RECT:
            r = pygame.Rect(self.loc.x,self.loc.y,self.life,self.life)
            r.center = (self.loc.x,self.loc.y)
            pygame.draw.rect(win, self.color, r)

    def update(self):
        if not self.color2 == (0, 0, 0):
            percent = self.life / 10

            resultRed = self.color_ori[0] + percent * (self.color2[0] - self.color_ori[0])
            resultGreen = self.color_ori[1] + percent * (self.color2[1] - self.color_ori[1])
            resultBlue = self.color_ori[2] + percent * (self.color2[2] - self.color_ori[2])
            self.color = (resultRed, resultGreen, resultBlue)

        self.life -= self.life_span
        self.vel += self.gravity
        self.loc += self.vel

        if self.life <= 0:
            del self