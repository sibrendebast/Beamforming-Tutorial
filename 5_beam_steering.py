import numpy as np
from util import tx
# import util
import const
import matplotlib.pyplot as plt
import matplotlib.animation as animation

num_frames = 100
max_angle = 120/180*np.pi


rxs = np.empty((500*500, 2))
for i in range(500):
    for j in range(500):
        rxs[i*500+j] = [-5 + 0.02*i, 0.02*j]

result = np.empty((500, 500))


def update(frame):
    field = np.zeros((500, 500), dtype=(np.complex128))
    num_sources = 16
    sources = []
    if frame < 100:
        theta = 2*frame/num_frames - 1
    else:
        theta = 2*(2*num_frames - frame)/num_frames - 1
    if theta != 0:
        phases = np.arange(-max_angle*theta, max_angle*theta, 2*max_angle*theta/(num_sources))
    else:
        phases = np.zeros(num_sources)
    for i in range(num_sources):
        wl = const.c / const.f
        array_size = (num_sources - 1)*wl/2
        sources.append(tx(np.array([-array_size/2 + i*wl/2, -0.01]), const.f, 1/num_sources, phases[i]))
    for source in sources:
        result = source.get_phasor_at_rx(rxs, 1000e-10)
        result = np.reshape(result, (500, 500))
        field += result
    field = np.rot90(np.abs(field))
    # field /= np.max(field)
    # field = 10*np.log10(field)
    im.set_array(field)


fig = plt.figure()
plt.axis('equal')
plt.axis('off')

im = plt.imshow(result, vmin=0, vmax=0.5)

anim = animation.FuncAnimation(fig, update, frames=num_frames*2, interval=50)
writergif = animation.PillowWriter(fps=20)
anim.save('./gifs/beam_steering.gif', writer=writergif)
