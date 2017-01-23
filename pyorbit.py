from pygame.locals import *
from random import randint
from os import urandom
from math import sqrt
import pygame

pygame.init()
screen = pygame.display.set_mode([500, 500])
clock = pygame.time.Clock()
# World object that controls all the planets orbiting the main body (star)
class World():
    def __init__(self, planets, iterations, mass = 10000000000000, gravityConstant = (6.6 * 10 ** -11)):
        # self.planets is a list of the planet objects which will be orbiting the main star
        # self.iterations is the number of iterations we will do per game loop on the physics loop
        # self.mass is the mass of the main body (star) that the objects will be orbiting
        # self.gravityConstant is the gravity constant 6.6 * 10^-11 Nm^2/kg
        self.planets = planets[:]
        size = screen.get_size()
        self.position = [int(size[0] / 2), int(size[1] / 2)]
        self.iterations = iterations
        self.mass = mass
        self.gravityConstant = gravityConstant

    # This function is called every game loop to calculate the forces between the bodies in the simulation
    def update(self):
        for i in range(self.iterations):
            for planet in self.planets:
                # Calculate the distance between the orbiting planet and the main star using pythagoras a^2 = b^2 +
                # c^2 Use the distance to then calculate the gravitational force between the object using
                # Gforce = (GConstant * massOfBody1 * massOfBody2)/(distanceBetweenObject^2)
                distanceX = planet.position[0] - self.position[0]
                distanceY = planet.position[1] - self.position[1]
                distance = sqrt(distanceX ** 2 + distanceY ** 2)
                GravForce = (-self.gravityConstant * self.mass * planet.mass) / (distance ** 2)
                GravForce = GravForce / planet.mass

                # VBBodies = Vector Between Bodies
                # Normalise the vector between the two bodies by dividing it by the distance between the two bodies
                # Add the vector to the planets velocity
                VBBodies = [distanceX / distance, distanceY / distance]
                VBBodies = [VBBodies[0] * GravForce, VBBodies[1] * GravForce]
                planet.velocity[0] += VBBodies[0]
                planet.velocity[1] += VBBodies[1]

                # This nested loop does the same as above but is between the orbiting planets and not the fixed point
                for planet2 in self.planets:
                    if planet.id != planet2.id:
                        distanceX = planet.position[0] - planet2.position[0]
                        distanceY = planet.position[1] - planet2.position[1]
                        distance = (distanceX ** 2 + distanceY ** 2)
                        GravForce = (-self.gravityConstant * planet.mass * planet2.mass) / (distance ** 2)
                        GravForce = GravForce / planet.mass

                        VBBodies = [distanceX / distance, distanceY / distance]
                        VBBodies = [VBBodies[0] * GravForce, VBBodies[1] * GravForce]
                        planet.velocity[0] += VBBodies[0]
                        planet.velocity[1] += VBBodies[1]
                planet.update()

    # This is called to draw the fixed body and the orbitting bodies to the pygame surface
    def draw(self):
        pygame.draw.circle(screen, [0, 0, 0], self.position, 10)
        for planet in self.planets:
            pygame.draw.rect(screen, [0, 0, 0], [planet.position[0], planet.position[1], 2, 2])
            pygame.draw.aalines(screen, [0, 0, 0], False, planet.path)

class planet():
    def __init__(self, velocity, startPosition, mass = 100000, pathLength = 100):
        # self.id is a unique id to be able to distinguish between different planets when
        # calculating forces between them
        # self.velocity is the velocity of the body in a vector format
        # self.position is the coordinates of the location of the body in the pygame surface
        # self.mass is the mass of the body
        # self.pathLength is the number of points the path (trail) of the body can have, the path can become short if
        # the number of iterations is larger than the default. Make sure to change this if you
        # want a similar length trail
        # self.path is the list of points in the path
        self.id = urandom(20)
        self.velocity = velocity[:]
        self.position = startPosition[:]
        self.mass = mass
        self.pathLength = pathLength
        self.path = [self.position[:]]

    # This is called every time the physics loop is iterated through, it adds the velocity of the object to the position
    # And updates the path list
    def update(self):
        self.position[0] += self.velocity[0]
        self.position[1] += self.velocity[1]
        self.path.append(self.position[:])
        if len(self.path) > self.pathLength:
            self.path.pop(0)

# Simple test to run, mouse wheel speed up/slows down simulation, left mouse click creates a new orbitting body at the
# Cursor location
def test():
    iterations = 10
    a = planet([0.7, 0.8], [350, 50], 100000, 100 * iterations)
    W = World([a], iterations)


    while 1:
        screen.fill([255, 255, 255])

        W.update()
        W.draw()

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    mousePosition = pygame.mouse.get_pos()
                    a = planet([randint(-200, 200) / 100, randint(-200, 200) / 100], [mousePosition[0], mousePosition[1]], randint(100000, 100000))
                    W.planets.append(a)




                if event.button == 4:
                    W.iterations -= 2
                    if W.iterations < 1:
                        W.iterations = 1
                elif event.button == 5:
                    W.iterations += 2
        pygame.display.update()
        clock.tick(60)
    pygame.quit()


test()
