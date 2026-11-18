from .ecg_analyzer import analyze_ecg
from .ecg_features import (
    calculate_heart_rate,
    calculate_rr_intervals,
    estimate_wave_intervals,
    find_irregular_beats,
)
from .ecg_loader import load_ecg_file
from .ecg_processor import clean_ecg
from .ecg_validator import validate_ecg_data, get_signal_information
from .r_peak_detector import detect_r_peaks


def analyze_file(file_path, sample_rate=None):
    """Run the complete ECG processing pipeline."""
    data = load_ecg_file(file_path, sample_rate=sample_rate)
    valid, message = validate_ecg_data(data)
    if not valid:
        raise ValueError(message)

    information = get_signal_information(data)
    filtered = clean_ecg(data["signal"], data["sample_rate"])
    r_peaks = detect_r_peaks(filtered, data["sample_rate"])

    if len(r_peaks) < 2:
        raise ValueError("Could not detect enough R-peaks for analysis.")

    rr_intervals = calculate_rr_intervals(r_peaks, data["sample_rate"])
    heart_rate = calculate_heart_rate(rr_intervals)
    irregular_beats = find_irregular_beats(r_peaks, data["sample_rate"])
    features = estimate_wave_intervals(filtered, r_peaks, data["sample_rate"])
    analysis = analyze_ecg(
        heart_rate,
        rr_intervals,
        irregular_beats,
        features,
    )

    result = {
        **information,
        **features,
        **analysis,
        "file_name": data["file_name"],
        "file_path": data["file_path"],
        "time": data["time"],
        "raw_signal": data["signal"],
        "filtered_signal": filtered,
        "r_peaks": r_peaks,
        "rr_intervals": rr_intervals,
        "average_rr": float(rr_intervals.mean()) if len(rr_intervals) else None,
        "heart_rate": heart_rate,
        "beat_count": len(r_peaks),
        "irregular_beats": irregular_beats,
    }

    return result
