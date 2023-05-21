import matplotlib.pyplot as plt
import numpy as np
import galaxy as g

def simulate_ratio(universe_size, galaxy_number, initial_type_ratio, time_step, time_max):
    """Runs simulations to produce the predicted final ratio of elliptical to spiral galaxies
    given an initial ratio of elliptical to spiral.

    Args:
        universe_size (int): size of observable universe.
        galaxy_number (int): number of galaxies to simulate.
        initial_type_ratio (float): decimal between 0 and 1 giving initial ratio
            of elliptical to spiral galaxies.
        time_step (float): size of time steps in simulation.
        time_max (int): how many time steps to take in simulation.

    Returns:
        float: predicted final ratio of elliptical to spiral galaxies.
    """
    time = 0
    galaxies = g.simulate_initialize(universe_size, galaxy_number, initial_type_ratio)

    while time <= time_max:
        for galaxy in galaxies:
            if galaxy.active:
                galaxy.time_update(galaxies, universe_size, time_step)

        time += time_step

    final_elliptical_ratio = g.elliptical_ratio(galaxies, universe_size)

    return final_elliptical_ratio

UNIVERSE_SIZE = 1000
GALAXY_NUMBER = 20
initial_type_ratios = np.arange(0, 0.5, 0.01)
TIME_STEP = 0.05
TIME_MAX = 120

ellip_fractions = [simulate_ratio(UNIVERSE_SIZE, GALAXY_NUMBER, i, TIME_STEP, TIME_MAX) \
    for i in initial_type_ratios]

plt.scatter(initial_type_ratios, ellip_fractions)
plt.xlabel('Initial ratio of elliptical to spiral galaxies')
plt.ylabel('Final ratio of elliptical to spiral galaxies')
plt.title(f'Ratio of galaxy types after {TIME_MAX} time steps at step size of {TIME_STEP}')
plt.show()
