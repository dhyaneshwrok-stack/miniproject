import numpy as np
from scipy.signal import find_peaks


def detect_r_peaks(ecg_signal, sample_rate):
    """Detect R peaks using a simple educational QRS-enhancement method."""
    values = np.asarray(ecg_signal, dtype=float)
    if len(values) < 100:
        return np.array([], dtype=int)

    derivative = np.gradient(values)
    squared = derivative * derivative

    window = max(1, int(0.12 * sample_rate))
    integrated = np.convolve(
        squared,
        np.ones(window) / window,
        mode="same",
    )

    distance = max(1, int(0.25 * sample_rate))
    prominence = max(np.std(integrated) * 0.5, np.finfo(float).eps)

    candidates, _ = find_peaks(
        integrated,
        distance=distance,
        prominence=prominence,
    )

    # Move each detected QRS candidate back to the strongest local ECG peak.
    search_radius = max(1, int(0.08 * sample_rate))
    r_peaks = []

    for candidate in candidates:
        start = max(0, candidate - search_radius)
        end = min(len(values), candidate + search_radius + 1)
        local = values[start:end]
        if len(local) == 0:
            continue
        peak = start + int(np.argmax(np.abs(local)))
        r_peaks.append(peak)

    if not r_peaks:
        return np.array([], dtype=int)

    r_peaks = np.unique(np.asarray(r_peaks, dtype=int))

    # Keep only peaks separated by the minimum physiological search distance.
    final_peaks = [int(r_peaks[0])]
    for peak in r_peaks[1:]:
        if peak - final_peaks[-1] >= distance:
            final_peaks.append(int(peak))

    return np.asarray(final_peaks, dtype=int)
