import matplotlib.pyplot as plt
import numpy as np
import galaxy as g

def simulate_ratio(universe_size, galaxy_number, initial_type_ratio, time_step, time_max):
    time = 0
    galaxies = []

    x = np.random.randint(0, universe_size, galaxy_number)
    y = np.random.randint(0, universe_size, galaxy_number)
    masses = np.random.randint(100, 1000, galaxy_number)

    for i in range(len(x)):
        gal_type = g.rand_type(initial_type_ratio)
        galaxies.append(g.Galaxy(i, x[i], y[i], masses[i], gal_type))

    while time <= time_max:
        for galaxy in galaxies:
            if galaxy.active:
                galaxy.time_update(galaxies, universe_size, time_step)

        time += time_step

    total = 0
    elliptical = 0
    for galaxy in galaxies:
        if galaxy.visible:
            total += 1
            if galaxy.gal_type == 'elliptical':
                elliptical += 1
    
    return round(elliptical/total, 4)

universe_size = 1000
galaxy_number = 20
initial_type_ratios = np.arange(0, 0.5, 0.01)
time_step = 0.05
time_max = 120

ellip_fractions = [simulate_ratio(universe_size, galaxy_number, i, time_step, time_max) for i in initial_type_ratios]

plt.scatter(initial_type_ratios, ellip_fractions)
plt.xlabel('Initial ratio of elliptical to spiral galaxies')
plt.ylabel('Final ratio of elliptical to spiral galaxies')
plt.title(f'Ratio of galaxy types after {time_max} time steps at step size of {time_step}')
plt.show()