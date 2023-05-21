import matplotlib.pyplot as plt
from matplotlib import animation
import numpy as np
import galaxy as g

UNIVERSE_SIZE = 1000
GALAXY_NUMBER = 50
INITIAL_TYPE_RATIO = 0.0
TIME_STEP = 0.02
TIME_MAX = 5
DOT_SCALE = 10
time = 0

galaxies = g.simulate_initialize(UNIVERSE_SIZE, GALAXY_NUMBER, INITIAL_TYPE_RATIO)
positions = []

fig, ax = plt.subplots()
scatter = ax.scatter([], [], c=[], s=[])
time_text = ax.text(0.02, 0.95, '', transform=ax.transAxes)
fraction_text = ax.text(0.02, 0.90, '', transform=ax.transAxes)

def update(frame):
    """Updates frame in matplotlib animation.

    Args:
        frame (_type_): _description_

    Returns:
        plot: current scatter plot of galaxies.
        string: current time in simulation.
        string: current elliptical to visible galaxy ratio.
    """    
    global time

    t_positions_x = []
    t_positions_y = []
    t_positions_c = []
    t_positions_m = []

    for galaxy in galaxies:
        if galaxy.active:
            galaxy.time_update(galaxies, UNIVERSE_SIZE, TIME_STEP)
            t_positions_x.append(galaxy.x_pos)
            t_positions_y.append(galaxy.y_pos)
            t_positions_c.append(galaxy.color)
            t_positions_m.append(galaxy.mass / DOT_SCALE)

    elliptical_fraction = g.elliptical_ratio(galaxies)

    scatter.set_offsets(np.column_stack((t_positions_x, t_positions_y)))
    scatter.set_color(t_positions_c)
    scatter.set_sizes(t_positions_m)

    time_text.set_text(f'Time: {time:.2f}')
    fraction_text.set_text(f'Elliptical Fraction: {elliptical_fraction:.2f}')

    # Update axis limits
    ax.set_xlim(0, UNIVERSE_SIZE)
    ax.set_ylim(0, UNIVERSE_SIZE)

    time += TIME_STEP

    return scatter, time_text, fraction_text

ani = animation.FuncAnimation(fig, update, frames=int(TIME_MAX / TIME_STEP), interval=50, blit=True)

plt.show()
