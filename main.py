#Imports
import pygame
import math

#Initializes pygame
pygame.init()

WIDTH, HEIGHT = 600, 600 #Width & Height of the pygame screen
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Planet Simulator")


class Planet:
    AU = 149.6e6 * 1000
    G = 6.67428e-11
    SCALE = 150 / AU #1 AU = 100 pixels
    TIMESTEP = 60*60*24 # 1 day

    def __init__(self, x, y, radius, color, mass):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.mass = mass
        
        self.orbit = []
        self.sun = False
        self.distance_to_sun = 0

        self.x_vel = 0
        self.y_vel = 0

    def draw(self, win):
        x = self.x * self.SCALE + WIDTH/2
        y = self.y * self.SCALE + HEIGHT/2
        pygame.draw.circle(win, self.color, (x, y), self.radius)

        if len(self.orbit) > 2:        
            updatedPoints = []
            for point in self.orbit:
                x,y = point
                x = x*self.SCALE + WIDTH/2
                y = y*self.SCALE + HEIGHT/2
                updatedPoints.append((x,y))

            pygame.draw.lines(win, self.color, False, updatedPoints, 2)

    def attraction(self, other):
        ox, oy = other.x, other.y
        distance_x = ox - self.x
        distance_y = oy - self.y
        distance = math.sqrt(distance_x**2 + distance_y**2)

        if other.sun:
            self.distance_to_sun = distance
        
        force = self.G * self.mass * other.mass / distance**2
        theta = math.atan2(distance_y, distance_x)
        
        force_x = math.cos(theta)*force
        force_y = math.sin(theta)*force

        return force_x, force_y

    def updatePosition(self, planets):
        total_fx = total_fy = 0
        for planet in planets:
            if self == planet:
                continue
            
            fx, fy = self.attraction(planet)
            total_fx += fx
            total_fy += fy
        
        self.x_vel += total_fx / self.mass * self.TIMESTEP #Increasing velocity by acceleration each day
        self.y_vel += total_fy / self.mass * self.TIMESTEP

        self.x += self.x_vel * self.TIMESTEP
        self.y += self.y_vel * self.TIMESTEP
        self.orbit.append((self.x, self.y))
    
    def drawDistance(self, planets, win):
        for planet in planets:
            if self == planet:
                continue
            
            d = math.sqrt((self.x - planet.x)**2 + (self.y-planet.y)**2)
            pygame.draw.line(win, self.color, (self.x, self.y), (planet.x, planet.y), 2)


def main():
    run = True
    clock = pygame.time.Clock()

    sun = Planet(0.003*Planet.AU, 0, 30, (255, 224, 46), 1.98892*10**30)
    #sun.y_vel = -.0023 * 1000
    sun.sun = True

    earth = Planet(-1*Planet.AU, 0, 16, (140, 226, 255), 5.9742*10**24)
    earth.y_vel = 29.783 * 1000
    mars = Planet(-1.524*Planet.AU, 0, 12, (212, 28, 28), 6.39*10**23)
    mars.y_vel = 24.077 * 1000
    mercury = Planet(0.387*Planet.AU, 0, 8, (174, 155, 199), 0.330*10**24)
    mercury.y_vel = -47.4*1000
    venus = Planet(0.723 * Planet.AU, 0, 14, (212, 255, 255), 4.8685*10**24)
    venus.y_vel = -35.02*1000

    planets = [sun, earth, mars, mercury, venus]

    while run:
        clock.tick(60)
        WIN.fill((0,0,0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        for planet in planets:
#            planet.drawDistance(planets, WIN)
            planet.updatePosition(planets)
            planet.draw(WIN)
        
        pygame.display.update()

    pygame.quit()


main()