import random
import matplotlib.pyplot as plt
from matplotlib import animation
import numpy as np
import scipy.constants as c

def rand_type(initial_type_ratio):
    """Returns random galaxy type based on desired initial ratio.

    Args:
        initial_type_ratio (float): ratio of elliptical to spiral galaxies

    Returns:
        string: either 'elliptical' or 'spiral'.
    """
    val = random.random()
    if val < initial_type_ratio:
        return 'elliptical'
    return 'spiral'

def gravity_force(galaxy_one, galaxy_two):
    """Calculates force of gravity between two galaxies. Dimensionless.

    Args:
        galaxy_one (Galaxy): first galaxy.
        galaxy_two (Galaxy): second galaxy.

    Returns:
        tuple of floats: x component and y component of force.
    """    
    G = c.G
    dist = galaxy_one.distance(galaxy_two)
    force = (galaxy_one.mass * galaxy_two.mass) / dist**2
    angle = galaxy_one.angle(galaxy_two)
    xforce = force * np.cos(angle)
    yforce = force * np.sin(angle)
    return xforce, yforce

class Galaxy:

    def __init__(self, id_, x, y, mass, gal_type):
        """Initializes Galaxy object.

        Args:
            id_ (int): convenient way to ID a specific galaxy.
            x (float): x component of position.
            y (float): y component of position.
            mass (int): mass of galaxy.
            gal_type (string): either spiral or elliptical.
        """        
        self.id_ = id_
        self.x = x
        self.y = y
        self.vx = 0
        self.vy = 0
        self.mass = mass
        self.gal_type = gal_type
        if gal_type == 'elliptical':
            self.color = 'r'
        else:
            self.color = 'b'

    def __repr__(self):      
        return f'Galaxy #{self.id_}:\n\t mass: {self.mass}\n\t coordinates\n\t \
            ({self.x}, {self.y})\n\t velocity: ({self.vx}, {self.vy})\n\t type: \
            {self.gal_type}\n'

    def __str__(self):
        return f'Galaxy #{self.id_}:\n\t mass: {self.mass}\n\t coordinates\n\t \
            ({self.x}, {self.y})\n\t velocity: ({self.vx}, {self.vy})\n\t type: \
            {self.gal_type}\n'

    def distance_x(self, other_galaxy):
        """Signed x distance between galaxy object and another galaxy.

        Args:
            other_galaxy (Galaxy): other galaxy being compared with self.

        Returns:
            float: signed x distance. Uses self as reference point.
        """        
        return other_galaxy.x - self.x

    def distance_y(self, other_galaxy):
        """Signed y distance between galaxy object and another galaxy.

        Args:
            other_galaxy (Galaxy): other galaxy being compared with self.

        Returns:
            float: signed y distance. Uses self as reference point.
        """   
        return other_galaxy.y - self.y

    def angle(self, other_galaxy):
        x = self.distance_x(other_galaxy)
        y = self.distance_y(other_galaxy)
        return np.arctan2(y, x)

    def distance(self, other_galaxy):
        return np.sqrt((self.x - other_galaxy.x)**2 + (self.y - other_galaxy.y)**2)

    def collide(self, other_galaxy):
        print('collision')
        active_galaxies.remove(other_galaxy.id_)
        self.gal_type = 'elliptical'
        self.color = 'r'
        total_mass = self.mass + other_galaxy.mass
        self.vx = (self.mass * self.vx +
                   other_galaxy.mass * other_galaxy.vx) / total_mass
        self.vy = (self.mass * self.vy +
                   other_galaxy.mass * other_galaxy.vy) / total_mass
        self.mass += other_galaxy.mass

    def time_update(self, other_galaxy_list):
        for galaxy in other_galaxy_list:
            if (galaxy != self) and (galaxy.id_ in active_galaxies):
                collision_distance = self.mass / galaxy.mass
                if self.distance(galaxy) < collision_distance:
                    self.collide(galaxy)
                force_x, force_y = gravity_force(self, galaxy)
                ax, ay = force_x / self.mass, force_y / self.mass
                self.vx += ax * TIME_STEP
                self.vy += ay * TIME_STEP

        self.x += self.vx * TIME_STEP
        self.y += self.vy * TIME_STEP

UNIVERSE_SIZE = 1000
GALAXY_NUMBER = 50
INITIAL_TYPE_RATIO = 0.0
TIME_STEP = 0.05
TIME_MAX = 5
time = 0

active_galaxies = []
galaxies = []
positions = []

x = np.random.randint(0, UNIVERSE_SIZE, GALAXY_NUMBER)
y = np.random.randint(0, UNIVERSE_SIZE, GALAXY_NUMBER)
masses = np.random.randint(100, 1000, GALAXY_NUMBER)

for i in range(len(x)):
    gal_type = rand_type(INITIAL_TYPE_RATIO)
    galaxies.append(Galaxy(i, x[i], y[i], masses[i], gal_type))
    active_galaxies.append(i)

fig, ax = plt.subplots()
scatter = ax.scatter([], [], c=[], s=[])
time_text = ax.text(0.02, 0.95, '', transform=ax.transAxes)
fraction_text = ax.text(0.02, 0.90, '', transform=ax.transAxes)

def update(frame):
    global time

    t_positions_x = []
    t_positions_y = []
    t_positions_c = []
    t_positions_m = []
    elliptical_galaxies = 0
    total_visible_galaxies = 0
    DOT_SCALE = 20

    for galaxy in galaxies:
        if galaxy.id_ in active_galaxies:
            galaxy.time_update(galaxies)
            t_positions_x.append(galaxy.x)
            t_positions_y.append(galaxy.y)
            t_positions_c.append(galaxy.color)
            t_positions_m.append(galaxy.mass / DOT_SCALE)
            if galaxy.x < UNIVERSE_SIZE and galaxy.y < UNIVERSE_SIZE:
                total_visible_galaxies += 1
                if galaxy.gal_type == 'elliptical':
                    elliptical_galaxies += 1

    scatter.set_offsets(np.column_stack((t_positions_x, t_positions_y)))
    scatter.set_color(t_positions_c)
    scatter.set_sizes(t_positions_m)

    time_text.set_text(f'Time: {time:.2f}')
    fraction_text.set_text(f'Elliptical Fraction: \
        {elliptical_galaxies / total_visible_galaxies:.2f}')

    # Update axis limits
    ax.set_xlim(0, UNIVERSE_SIZE)
    ax.set_ylim(0, UNIVERSE_SIZE)

    time += TIME_STEP

    return scatter, time_text, fraction_text

ani = animation.FuncAnimation(fig, update, frames=int(TIME_MAX / TIME_STEP), interval=50, blit=True)

plt.show()
