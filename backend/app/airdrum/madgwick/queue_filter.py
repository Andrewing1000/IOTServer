import numpy as np
from scipy.interpolate import interp1d
from scipy.signal import filtfilt, firwin, lfilter, savgol_coeffs, savgol_filter
from collections import deque

from typing import Literal

class FilteredBuffer:
    def __init__(self, cutoff, size=200, fs = 190,
                type: Literal['lowpass', 'highpass'] ='lowpass'):
        self.cutoff = cutoff
        self.size = size
        self.fs = fs
        self.buffer = deque(iterable=np.zeros((size, 4), dtype=np.float64), maxlen=size)
        self.fir_filter = firwin(numtaps=31, cutoff=cutoff, pass_zero=type, fs=fs)
        #self.fir_filter = savgol_coeffs(window_length=31, polyorder=4, deriv=2, )
        self.last_ts = 0

    def update(self, point, period):
        self.last_ts += period
        point = np.insert(point, 0, self.last_ts)
        self.buffer.appendleft(point)

        #return point[1:]

        if self.last_ts/(1e6/self.fs) < 200:
            return point

        sampled_data = np.array(self.buffer)
        sampled_time = sampled_data[:, 0]
        sampled_values = sampled_data[:, 1:]

        interpolator = interp1d(sampled_time, sampled_values, kind='linear', axis=0)
        uniform_time = np.arange(sampled_time.min(), sampled_time.max(), step=1e6/self.fs)
        uniform_sampled = interpolator(uniform_time)
        
        #return savgol_filter(uniform_sampled, window_length=200, polyorder=3, axis=0, mode='interp')[-1]
        #return filtfilt(self.fir_filter, [1.0], uniform_sampled, axis=0)[-1]
        return lfilter(self.fir_filter, [1.0], uniform_sampled, axis=0, )[-1]

