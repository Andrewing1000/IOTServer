import numpy as np
from collections import deque
from scipy.signal import firwin

class FIRFilter:
    def __init__(self, fs, cutoff, order=51, filter_type='low', window='hamming'):
        """
        Initializes the FIR filter and designs the filter coefficients.

        Args:
            fs (float): Initial sampling frequency in Hz.
            cutoff (float or list): Cutoff frequency (Hz) for lowpass/highpass,
                                    or [low, high] for bandpass/bandstop filters.
            order (int): Order of the filter (number of coefficients).
            filter_type (str): Type of filter: 'low', 'high', 'bandpass', or 'bandstop'.
            window (str or tuple): Desired window to use. See scipy.signal.get_window.
        """
        self.order = order
        self.filter_type = filter_type
        self.window = window
        self.cutoff = cutoff

        # Initialize with the initial sampling frequency
        self.fs = fs
        self.coefficients = self._design_filter(self.fs)
        self.buffer_size = len(self.coefficients)
        self.buffer = deque([np.zeros(3)] * self.buffer_size, maxlen=self.buffer_size)
        self.last_filtered = np.zeros(3)

    def _design_filter(self, fs):
        """
        Designs the FIR filter coefficients using the specified parameters.

        Args:
            fs (float): Sampling frequency in Hz.

        Returns:
            numpy.array: The designed FIR filter coefficients.
        """
        nyquist = 0.5 * fs  # Nyquist frequency
        if isinstance(self.cutoff, (list, tuple, np.ndarray)):
            normal_cutoff = [freq / nyquist for freq in self.cutoff]
        else:
            normal_cutoff = self.cutoff / nyquist

        # Determine pass_zero parameter based on filter type
        if self.filter_type == 'low':
            pass_zero = True
        elif self.filter_type == 'high':
            pass_zero = False
        elif self.filter_type == 'bandpass':
            pass_zero = False
        elif self.filter_type == 'bandstop':
            pass_zero = True
        else:
            raise ValueError("Invalid filter_type. Must be 'low', 'high', 'bandpass', or 'bandstop'.")

        # Design the filter using firwin
        coefficients = firwin(
            numtaps=self.order,
            cutoff=normal_cutoff,
            window=self.window,
            pass_zero=pass_zero
        )
        return coefficients

    def update_sampling_frequency(self, fs):
        """
        Updates the sampling frequency and redesigns the filter coefficients.

        Args:
            fs (float): New sampling frequency in Hz.
        """
        self.fs = fs
        self.coefficients = self._design_filter(self.fs)
        # Update buffer size if necessary
        old_buffer = list(self.buffer)
        self.buffer_size = len(self.coefficients)
        self.buffer = deque(old_buffer, maxlen=self.buffer_size)
        # Pad buffer with zeros if necessary
        while len(self.buffer) < self.buffer_size:
            self.buffer.appendleft(np.zeros(3))

    def filter(self, data_point):
        """
        Filters a single 3D data point.

        Args:
            data_point (numpy.array): A 3D vector data point (shape: [3]).

        Returns:
            numpy.array: The filtered 3D data point.
        """
        self.buffer.append(data_point)
        buffer_array = np.array(self.buffer)
        # Check if buffer is filled enough
        if len(self.buffer) < self.order:
            # Not enough data yet, return zero or initial value
            filtered_point = np.zeros(3)
        else:
            # Apply FIR filter: element-wise multiplication and sum across the buffer
            filtered_point = np.sum(buffer_array * self.coefficients[:, None], axis=0)
        self.last_filtered = filtered_point
        return filtered_point

    def get_last_filtered(self):
        """
        Returns the last filtered data point.

        Returns:
            numpy.array: The last filtered 3D data point.
        """
        return self.last_filtered
