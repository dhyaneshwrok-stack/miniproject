import numpy as np
from scipy import signal


def clean_ecg(ecg_signal, sample_rate):
    """Remove baseline drift and common high-frequency noise."""
    values = np.asarray(ecg_signal, dtype=float)
    if len(values) < 20:
        raise ValueError("ECG signal is too short to process.")

    nyquist = sample_rate / 2.0
    low = max(0.5 / nyquist, 0.001)
    high = min(40.0 / nyquist, 0.99)

    if low >= high:
        raise ValueError("Sampling rate is too low for ECG filtering.")

    b, a = signal.butter(3, [low, high], btype="bandpass")
    cleaned = signal.filtfilt(b, a, values)
    return cleaned
