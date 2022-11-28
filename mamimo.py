import numpy as np
from util import tx
# import util
import const
import matplotlib.pyplot as plt
import matplotlib.animation as animation


# num_sources = 16
num_frames = 100

rxs = np.empty((500*500, 2))
for i in range(500):
    for j in range(500):
        rxs[i*500+j] = [-5 + 0.02*i, 0.02*j]

trajectory = np.zeros((num_frames, 2))
for i in range(len(trajectory)):
    trajectory[i] = [2-0.04*i, 5+0.02*i]


wl = const.c / const.f
num_sources = 16
num_sides = 4
source_loc = []
for i in range(num_sources):
    source_loc.append([-4.95 + wl/2*i, -0.5])
# for i in range(num_sources):
#     source_loc[num_sources + i] = [-4.95 + wl/2*i, 10.5]
# for i in range(num_sources):
#     source_loc[2*num_sources + i] = [-5.5, 0.05 + wl/2*i]
for i in range(num_sources):
    source_loc.append([5.5, 0.05 + wl/2*i])


def update(frame):
    print(f'\r{frame+1}/{num_frames*2}', end='')
    if frame < num_frames:
        rx = np.reshape(trajectory[frame], (1, 2))
    else:
        rx = np.reshape(trajectory[num_frames*2-frame-1], (1, 2))
    sources = []
    channel = np.zeros(len(source_loc), dtype=np.complex128)
    for i in range(len(source_loc)):
        sources.append(tx(source_loc[i], const.f, 1/len(source_loc), 0))
    for i, source in enumerate(sources):
        channel[i] = source.get_phasor_at_rx(rx, 1)
    channel /= np.sqrt(np.linalg.norm(channel))

    field = np.zeros((500, 500), dtype=(np.complex128))
    # num_sources = 16
    sources = []
    for i in range(len(source_loc)):
        sources.append(tx(source_loc[i], const.f, np.abs(channel[i]), np.angle(channel[i])))
    for source in sources:
        result = source.get_phasor_at_rx(rxs, 1)
        result = np.reshape(result, (500, 500))
        field += result
    field = np.abs(field)
    im.set_array(np.rot90(field))
    # print(np.max(field))
    # im.set_array(field.T)


fig = plt.figure()
plt.axis('equal')
plt.axis('off')

field = np.empty((500, 500))
im = plt.imshow(field, vmin=0, vmax=0.8)

anim = animation.FuncAnimation(fig, update, frames=10, interval=50)
writergif = animation.PillowWriter(fps=20)
anim.save('./gifs/mamimo.gif', writer=writergif)
# plt.close()

print()


# plt.show()
