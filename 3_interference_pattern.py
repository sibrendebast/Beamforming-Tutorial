import numpy as np
from util import tx
# import util
import const
import matplotlib.pyplot as plt
import matplotlib.animation as animation

num_sources = 2
sources = []
for i in range(num_sources):
    # wl = const.c / const.f
    array_size = 5
    sources.append(tx(np.array([-array_size/2 + i*array_size/(num_sources-1), -0.01]), const.f, 1/num_sources, 0))
# sources.append(tx(np.array([0.075, -0.01]), const.f, 0.5, 0))
# source = tx(np.array([0, -0.01]), const.f, 1, 0)

rxs = np.empty((500*500, 2))
for i in range(500):
    for j in range(500):
        rxs[i*500+j] = [-5 + 0.02*i, 0.02*j]

result = np.zeros((500, 500))


def update(frame):
    field = np.zeros((500, 500), dtype=(np.complex128))
    for source in sources:
        result = source.get_phasor_at_rx(rxs, frame*1e-10)
        result = np.reshape(result, (500, 500))
        field += result
    im.set_array(np.rot90(np.real(field)))


fig = plt.figure()
plt.axis('equal')
plt.axis('off')
plt.tight_layout(pad=0)
im = plt.imshow(result, vmin=-2, vmax=2)

anim = animation.FuncAnimation(fig, update, frames=500)
# anim.save('./gifs/interference_real.gif', writer='imagemagick', fps=20)
writergif = animation.PillowWriter(fps=20)
anim.save('./gifs/interference_real.gif', writer=writergif)
plt.close()


def update_abs(frame):
    field = np.zeros((500, 500), dtype=(np.complex128))
    for source in sources:
        result = source.get_phasor_at_rx(rxs, frame*1e-10)
        result = np.reshape(result, (500, 500))
        field += result
    im.set_array(np.rot90(np.abs(field)))


result = np.zeros((500, 500))
fig = plt.figure()
plt.axis('equal')
plt.axis('off')
plt.tight_layout(pad=0)
im = plt.imshow(result, vmin=0, vmax=2)

anim = animation.FuncAnimation(fig, update_abs, frames=500)
# anim.save('./gifs/interference_real.gif', writer='imagemagick', fps=20)
writergif = animation.PillowWriter(fps=20)
anim.save('./gifs/interference_abs.gif', writer=writergif)
plt.close()

# plt.show()
