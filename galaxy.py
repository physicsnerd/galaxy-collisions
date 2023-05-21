"""Galaxy module.

Classes:
    Galaxy

Methods:
    rand_type: returns random galaxy type.
    gravity_force: calculates force between two galaxies.
"""

import random
import numpy as np
#import scipy.constants as c

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
    #G = c.G
    dist = galaxy_one.distance(galaxy_two)
    force = (galaxy_one.mass * galaxy_two.mass)/dist**2
    angle = galaxy_one.angle(galaxy_two)
    x_force = force * np.cos(angle)
    y_force = force * np.sin(angle)
    return x_force, y_force

class Galaxy:
    """Galaxy class.

    Parameters:
        id_ (int): convenient way to ID a specific galaxy.
        x_pos (float): x component of position.
        y_pos (float): y component of position.
        mass (int): mass of galaxy.
        gal_type (string): either spiral or elliptical.
        v_x (float): x component of velocity.
        v_y (float): y component of velocity.
        active (bool): convenient tool to check if collided.
        in_visible_universe (bool): within bounds of universe.
        color (string): convenient way to plot gal_type - matplotlib color.

    Methods:
        __init__: initializes Galaxy object.
        __repr__: custom print.
        __str__: custom print.
        distance_x: x distance between two galaxies.
        distance_y: y distance between two galaxies.
        angle: angle between two galaxies.
        distance: euclidean distance between two galaxies.
        visible: checks whether galaxy still in visible universe.
        collide: handles galaxy collisions.
        time_update: evolves the galaxy in time based on forces from other galaxies.
    """

    def __init__(self, id_, x_pos, y_pos, mass, gal_type):
        """Initializes Galaxy object.

        Args:
            id_ (int): convenient way to ID a specific galaxy.
            x_pos (float): x component of position.
            y_pos (float): y component of position.
            mass (int): mass of galaxy.
            gal_type (string): either spiral or elliptical.
        """
        self.id_ = id_
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.v_x = 0
        self.v_y = 0
        self.mass = mass
        self.gal_type = gal_type
        self.active = True
        self.in_visible_universe = True
        if gal_type == 'elliptical':
            self.color = 'r'
        else:
            self.color = 'b'

    def __repr__(self):
        return f'Galaxy #{self.id_}:\n\t mass: {self.mass}\n\t coordinates\n\t ({self.x_pos}, \
            {self.y_pos})\n\t velocity: ({self.v_x}, {self.v_y})\n\t type: {self.gal_type}\n'

    def __str__(self):
        return f'Galaxy #{self.id_}:\n\t mass: {self.mass}\n\t coordinates\n\t ({self.x_pos}, \
            {self.y_pos})\n\t velocity: ({self.v_x}, {self.v_y})\n\t type: {self.gal_type}\n'

    def distance_x(self, other_galaxy):
        """Signed x distance between galaxy object and another galaxy.

        Args:
            other_galaxy (Galaxy): other galaxy being compared with self.

        Returns:
            float: signed x distance. Uses self as reference point.
        """
        return other_galaxy.x_pos - self.x_pos

    def distance_y(self, other_galaxy):
        """Signed y distance between galaxy object and another galaxy.

        Args:
            other_galaxy (Galaxy): other galaxy being compared with self.

        Returns:
            float: signed y distance. Uses self as reference point.
        """
        return other_galaxy.y_pos - self.y_pos

    def angle(self, other_galaxy):
        """Angle between self and another galaxy.

        Args:
            other_galaxy (Galaxy): other galaxy of interest.

        Returns:
            float: signed angle between galaxies.
        """
        x_dist = self.distance_x(other_galaxy)
        y_dist = self.distance_y(other_galaxy)
        return np.arctan2(y_dist, x_dist)

    def distance(self, other_galaxy):
        """Euclidean distance between self and another galaxy.

        Args:
            other_galaxy (Galaxy): other galaxy of interest.

        Returns:
            float: positive euclidean distance.
        """
        return np.sqrt((self.x_pos - other_galaxy.x_pos)**2 + (self.y_pos - other_galaxy.y_pos)**2)

    def visible(self, universe_size):
        """Checks whether galaxy still in observable universe.

        Args:
            universe_size (int): size of observable universe.

        Returns:
            bool: whether or not the galaxy has moved outside observable universe.
        """
        if self.x_pos <= universe_size and self.y_pos <= universe_size:
            return True
        return False

    def collide(self, other_galaxy):
        """Handles collisions between self and other galaxy. Makes other galaxy inactive,
        Changes type of self to elliptical (and color correspondingly).
        Changes mass and velocity of self appropriately using conservation of momentum.

        Args:
            other_galaxy (Galaxy): other galaxy of interest.
        """
        other_galaxy.active = False
        self.gal_type = 'elliptical'
        self.color = 'r'
        total_mass = self.mass + other_galaxy.mass
        self.v_x = (self.mass * self.v_x + other_galaxy.mass * other_galaxy.v_x) / total_mass
        self.v_y = (self.mass * self.v_y + other_galaxy.mass * other_galaxy.v_y) / total_mass
        self.mass += total_mass

    def time_update(self, other_galaxy_list, universe_size, time_step):
        """Updates the galaxy (position, velocity) in time by finding forces on galaxy.
        Recognizes when collision has occurred.

        Args:
            other_galaxy_list (list): list of Galaxy objects.
            universe_size (int): size of observable universe.
            time_step (float): size of time step in simulation.
        """
        self.in_visible_universe = self.visible(universe_size)
        for galaxy in other_galaxy_list:
            if (galaxy != self) and (galaxy.active):
                collision_distance = self.mass/galaxy.mass
                force_x, force_y = gravity_force(self, galaxy)
                a_x, a_y = force_x/self.mass, force_y/self.mass
                self.v_x += a_x * time_step
                self.v_y += a_y * time_step
                self.x_pos += self.v_x * time_step
                self.y_pos += self.v_y * time_step
                if self.distance(galaxy) < collision_distance:
                    self.collide(galaxy)
            elif (galaxy == self) and (galaxy.active):
                self.x_pos += self.v_x * time_step
                self.y_pos += self.v_y * time_step

def simulate_initialize(universe_size, galaxy_number, initial_type_ratio):
    """Creates 

    Args:
        universe_size (int): size of observable universe.
        galaxy_number (int): number of galaxies to simulate.
        initial_type_ratio (float): decimal between 0 and 1 giving initial ratio
            of elliptical to spiral galaxies.

    Returns:
        list: list of Galaxy objects that were generated.
    """
    galaxies = []

    x_positions = np.random.randint(0, universe_size, galaxy_number)
    y_positions = np.random.randint(0, universe_size, galaxy_number)
    masses = np.random.randint(100, 1000, galaxy_number)

    for i, x_pos in enumerate(x_positions):
        gal_type = rand_type(initial_type_ratio)
        galaxies.append(Galaxy(i, x_pos, y_positions[i], masses[i], gal_type))

    return galaxies

def elliptical_ratio(galaxy_list, universe_size):
    """Finds ratio of elliptical galaxies to total visible galaxies.

    Args:
        galaxy_list (list): list of Galaxy objects.
        universe_size (int): size of visible universe.

    Returns:
        float: ratio of elliptical to total visible galaxies.
    """
    total_visible_galaxies = 0
    elliptical_galaxies = 0

    for galaxy in galaxy_list:
        if galaxy.visible(universe_size):
            total_visible_galaxies += 1
            if galaxy.gal_type == 'elliptical':
                elliptical_galaxies += 1

    return round(elliptical_galaxies/total_visible_galaxies, 4)
