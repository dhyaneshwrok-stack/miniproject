import numpy as np


def validate_ecg_data(ecg_data):
    """Validate the basic ECG data before processing."""
    if not isinstance(ecg_data, dict):
        return False, "Invalid ECG data."

    signal = ecg_data.get("signal")
    sample_rate = ecg_data.get("sample_rate")

    if signal is None or len(signal) < 100:
        return False, "ECG signal is too short."

    signal = np.asarray(signal, dtype=float)
    if not np.isfinite(signal).all():
        return False, "ECG signal contains invalid values."

    if sample_rate is None or sample_rate <= 0:
        return False, "Sampling rate is missing or invalid."

    return True, "ECG data is valid."


def get_signal_information(ecg_data):
    signal = np.asarray(ecg_data["signal"], dtype=float)
    sample_rate = float(ecg_data["sample_rate"])

    return {
        "number_of_samples": len(signal),
        "sample_rate": sample_rate,
        "duration": len(signal) / sample_rate,
        "minimum": float(np.min(signal)),
        "maximum": float(np.max(signal)),
        "average": float(np.mean(signal)),
    }
