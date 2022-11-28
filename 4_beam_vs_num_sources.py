import numpy as np
from util import tx
import const
import matplotlib.pyplot as plt
import matplotlib.animation as animation

num_sources = 64
sources = []
for i in range(num_sources):
    wl = const.c / const.f
    array_size = (num_sources - 1)*wl/2
    sources.append(tx(np.array([-array_size/2 + i*wl/2, -0.01]), const.f, 1/num_sources, 0))
# sources.append(tx(np.array([0.075, -0.01]), const.f, 0.5, 0))
# source = tx(np.array([0, -0.01]), const.f, 1, 0)

rxs = np.empty((500*500, 2))
for i in range(500):
    for j in range(500):
        rxs[i*500+j] = [-5 + 0.02*i, 0.02*j]

result = np.empty((500, 500))


def update(frame):
    field = np.zeros((500, 500), dtype=(np.complex128))
    num_sources = frame + 1
    sources = []
    for i in range(num_sources):
        wl = const.c / const.f
        array_size = (num_sources - 1)*wl/2
        sources.append(tx(np.array([-array_size/2 + i*wl/2, -1]), const.f, 1/num_sources, 0))
    for source in sources:
        result = source.get_phasor_at_rx(rxs, 1000e-10)
        result = np.reshape(result, (500, 500))
        field += result
    field = np.rot90(np.abs(field))
    im.set_array(field)


fig = plt.figure()
plt.axis('equal')
plt.axis('off')

im = plt.imshow(result, vmin=0, vmax=0.5)

anim = animation.FuncAnimation(fig, update, frames=16, interval=500)
writergif = animation.PillowWriter(fps=2)
anim.save('./gifs/array.gif', writer=writergif)


def update_real(frame):
    field = np.zeros((500, 500), dtype=(np.complex128))
    num_sources = frame + 1
    sources = []
    for i in range(num_sources):
        wl = const.c / const.f
        array_size = (num_sources - 1)*wl/2
        sources.append(tx(np.array([-array_size/2 + i*wl/2, -1]), const.f, 1/num_sources, 0))
    for source in sources:
        result = source.get_phasor_at_rx(rxs, 1000e-10)
        result = np.reshape(result, (500, 500))
        field += result
    field = np.rot90(np.real(field))
    im.set_array(field)


fig = plt.figure()
plt.axis('equal')
plt.axis('off')

im = plt.imshow(result, vmin=0, vmax=0.5)

anim = animation.FuncAnimation(fig, update_real, frames=16, interval=500)
writergif = animation.PillowWriter(fps=2)
anim.save('./gifs/array_real.gif', writer=writergif)
# plt.show()
