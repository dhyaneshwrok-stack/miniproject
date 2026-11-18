import numpy as np


def calculate_rr_intervals(r_peaks, sample_rate):
    r_peaks = np.asarray(r_peaks, dtype=int)
    if len(r_peaks) < 2:
        return np.array([], dtype=float)
    return np.diff(r_peaks) / float(sample_rate)


def calculate_heart_rate(rr_intervals):
    rr = np.asarray(rr_intervals, dtype=float)
    rr = rr[np.isfinite(rr) & (rr > 0)]
    if len(rr) == 0:
        return None
    return float(60.0 / np.median(rr))


def find_irregular_beats(r_peaks, sample_rate, tolerance=0.20):
    """Flag beats whose RR interval differs noticeably from the median."""
    r_peaks = np.asarray(r_peaks, dtype=int)
    rr = calculate_rr_intervals(r_peaks, sample_rate)
    if len(rr) == 0:
        return []

    median_rr = float(np.median(rr))
    if median_rr <= 0:
        return []

    flagged = []
    for index, interval in enumerate(rr):
        difference = abs(interval - median_rr) / median_rr
        if difference > tolerance:
            # RR interval belongs to the beat at the second R peak.
            flagged.append(index + 1)
    return flagged


def estimate_wave_intervals(ecg_signal, r_peaks, sample_rate):
    """Return rough educational estimates for PR, QRS, QT and QTc.

    These are signal-processing estimates, not clinical measurements.
    If a boundary cannot be found with reasonable confidence, None is used.
    """
    values = np.asarray(ecg_signal, dtype=float)
    fs = float(sample_rate)

    pr_values = []
    qrs_values = []
    qt_values = []
    qtc_values = []

    for r in np.asarray(r_peaks, dtype=int):
        if r < int(0.30 * fs) or r + int(0.55 * fs) >= len(values):
            continue

        # Approximate QRS onset/end around the R peak using local slope.
        qrs_window = values[r - int(0.12 * fs): r + int(0.12 * fs)]
        if len(qrs_window) < 10:
            continue

        derivative = np.abs(np.gradient(qrs_window))
        threshold = max(np.percentile(derivative, 35), np.max(derivative) * 0.08)
        center = int(0.12 * fs)

        left = center
        for i in range(center - 1, max(1, center - int(0.10 * fs)), -1):
            if derivative[i] < threshold:
                left = i
                break

        right = center
        for i in range(center + 1, min(len(derivative) - 2, center + int(0.10 * fs))):
            if derivative[i] < threshold:
                right = i
                break

        qrs_onset = r - center + left
        qrs_end = r - center + right
        qrs_ms = (qrs_end - qrs_onset) / fs * 1000.0

        if 40 <= qrs_ms <= 220:
            qrs_values.append(qrs_ms)
        else:
            continue

        # Search for a P-wave peak before QRS.
        p_start = max(0, r - int(0.30 * fs))
        p_end = max(p_start + 1, r - int(0.08 * fs))
        p_region = values[p_start:p_end]
        if len(p_region) > 5:
            p_peak = p_start + int(np.argmax(np.abs(p_region - np.median(p_region))))
            pr_ms = (qrs_onset - p_peak) / fs * 1000.0
            if 80 <= pr_ms <= 300:
                pr_values.append(pr_ms)

        # Search for the T-wave peak after QRS.
        t_start = min(len(values) - 1, qrs_end + int(0.08 * fs))
        t_end = min(len(values), r + int(0.50 * fs))
        t_region = values[t_start:t_end]
        if len(t_region) > 5:
            t_peak = t_start + int(np.argmax(np.abs(t_region - np.median(t_region))))
            qt_ms = (t_peak - qrs_onset) / fs * 1000.0
            if 250 <= qt_ms <= 650:
                qt_values.append(qt_ms)

                rr = _nearest_rr(r, r_peaks, fs)
                if rr:
                    qtc = qt_ms / np.sqrt(rr)
                    if 300 <= qtc <= 750:
                        qtc_values.append(qtc)

    return {
        "pr_ms": _median_or_none(pr_values),
        "qrs_ms": _median_or_none(qrs_values),
        "qt_ms": _median_or_none(qt_values),
        "qtc_ms": _median_or_none(qtc_values),
    }


def _nearest_rr(r_peak, r_peaks, sample_rate):
    index = np.where(r_peaks == r_peak)[0]
    if len(index) == 0:
        return None
    i = int(index[0])
    if i == 0:
        return None
    return (r_peak - r_peaks[i - 1]) / sample_rate


def _median_or_none(values):
    if not values:
        return None
    return float(np.median(values))
