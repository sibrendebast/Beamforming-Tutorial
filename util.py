import numpy as np
import const


def distance(tx, rx):
    tx_loc = tx.get_loc()
    return np.sqrt(((rx - tx_loc)**2).sum(axis=1))


class tx():

    def __init__(self, loc, freq, amplitude, phase=0):
        self.loc = loc
        self.freq = freq
        self.amplitude = amplitude
        self.phase = phase

    def get_loc(self):
        return self.loc

    def get_phasor_at_rx(self, rx, t):
        dist = distance(self, rx)
        A = (np.where(dist < t*const.c, self.amplitude/np.sqrt(dist), 0))
        phi = -2*np.pi*self.freq*t + dist*self.freq/const.c + self.phase
        return A*np.exp(phi*1j)
