import numpy as np
from util import tx
# import util
import const
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# Define the number of frames in the animation
num_frames = 100
# The number of radiating antennas
num_sources = 16

global sources
sources = []
for i in range(num_sources):
    wl = const.c / const.f
    array_size = (num_sources - 1)*wl/2
    sources.append(tx(np.array([-array_size/2 + i*wl/2, -1]), const.f, 1/num_sources, 0))

# create all the locations at which you want to plot the power
# We choose for a 500 by 500 grid
rxs = np.empty((500*500, 2))
for i in range(500):
    for j in range(500):
        rxs[i*500+j] = [-5 + 0.02*i, 0.02*j]


# Define the trajectory of the receiver which we want to serve using MRT precoding
trajectory = np.zeros((num_frames, 2))
for i in range(len(trajectory)):
    trajectory[i] = [2-0.04*i, 5+0.02*i]
trajectory = np.append(trajectory, np.flipud(trajectory), axis=0)


# The computation of one frame
# arg:
#   frame:
#       The number of the frame in the animation. this relates to the time
def update(frame, sources):
    print(f'\r{frame+1}/{num_frames*2}', end='')
    # Move the user along the defined trajectory
    rx = np.reshape(trajectory[frame], (1, 2))
    ax.set_offsets(trajectory[frame]*[-50, -50] + [250, +500])
    # Define an ampty array tp store the channel of the user
    channel = np.zeros(len(sources), dtype=np.complex128)
    # Send a pilot to measure the channel at a random time
    for i, source in enumerate(sources):
        channel[i] = source.get_phasor_at_rx(rx, 1000e-10)
    # normalise the channel
    channel /= np.sqrt(np.linalg.norm(channel))
    # Define the array to store the electric field
    field = np.zeros((500, 500), dtype=(np.complex128))
    wl = const.c / const.f
    for i in range(num_sources):
        array_size = (num_sources - 1)*wl/2
        # Apply the MRT precoder to the sources
        source = tx(np.array([-array_size/2 + i*wl/2, -1]), const.f, np.abs(channel[i]), np.angle(channel[i]))
        result = source.get_phasor_at_rx(rxs, 1000e-10)
        result = np.reshape(result, (500, 500))
        field += result
    field = np.abs(field)
    im.set_array(np.rot90(field))


# Set up the figure
fig = plt.figure()
plt.axis('equal')
plt.axis('off')
fig.tight_layout()

# define an empty area to initialise th efigure
field = np.empty((500, 500))
im = plt.imshow(field, vmin=0, vmax=0.8)
ax = plt.scatter(25, 50, s=20, c='red', marker='o')

# set up the animation
anim = animation.FuncAnimation(fig, update, frames=num_frames*2, fargs=(sources,), interval=50)
writergif = animation.PillowWriter(fps=20)
anim.save('./gifs/mrt.gif', writer=writergif)
