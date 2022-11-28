import numpy as np
import const
import matplotlib.pyplot as plt


t = np.arange(0, 0.5e-8, 1e-11)

sin = 0.5*np.exp(2j*np.pi*const.f*t)


plt.figure(figsize=(9, 2.5))
plt.plot(t, np.real(sin))
plt.ylim([-1.1, 1.1])
plt.xlabel('Time [s]', fontsize=18)
plt.ylabel('Amplitude', fontsize=18)
plt.tight_layout()
plt.savefig('./plots/sin.png', bbox_inches="tight")


plt.figure(figsize=(9, 2.5))
plt.plot(t, np.real(-sin))
plt.ylim([-1.1, 1.1])
plt.xlabel('Time [s]', fontsize=18)
plt.ylabel('Amplitude', fontsize=18)
plt.tight_layout()
plt.savefig('./plots/sin_minus.png', bbox_inches="tight")


plt.figure(figsize=(9, 2.5))
plt.plot(t, np.real(sin) + np.real(sin))
plt.ylim([-1.1, 1.1])
plt.xlabel('Time [s]', fontsize=18)
plt.ylabel('Amplitude', fontsize=18)
plt.tight_layout()
plt.savefig('./plots/sin_const.png', bbox_inches="tight")


plt.figure(figsize=(9, 2.5))
plt.plot(t, np.real(sin) - np.real(sin))
plt.ylim([-1.1, 1.1])
plt.xlabel('Time [s]', fontsize=18)
plt.ylabel('Amplitude', fontsize=18)
plt.tight_layout()
plt.savefig('./plots/sin_dest.png', bbox_inches="tight")
