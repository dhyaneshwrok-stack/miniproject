from pathlib import Path

import numpy as np
import pandas as pd


def load_ecg_file(file_path, sample_rate=None):
    """Load an ECG CSV/TXT file and return a simple data dictionary."""
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"File not found: {path}")

    if path.suffix.lower() == ".csv":
        data = pd.read_csv(path)
    elif path.suffix.lower() == ".txt":
        data = pd.read_csv(path, sep=None, engine="python")
    else:
        raise ValueError("Only CSV and TXT files are supported.")

    data = data.dropna(axis=1, how="all")
    if data.empty:
        raise ValueError("The ECG file is empty.")

    signal_column = _find_signal_column(data)
    signal = pd.to_numeric(data[signal_column], errors="coerce")
    signal = signal.dropna().to_numpy(dtype=float)

    if len(signal) < 100:
        raise ValueError("The ECG file does not contain enough signal data.")

    time_column = _find_time_column(data)
    time = None

    if time_column:
        time = pd.to_numeric(data[time_column], errors="coerce").to_numpy(dtype=float)
        valid = np.isfinite(time)
        time = time[valid]
        signal = signal[: len(time)]

    if sample_rate is None and time is not None:
        sample_rate = _calculate_sample_rate(time)

    if sample_rate is None or sample_rate <= 0:
        raise ValueError(
            "Sampling rate is required. Add a time column or enter the sample rate."
        )

    sample_rate = float(sample_rate)
    time = np.arange(len(signal), dtype=float) / sample_rate

    return {
        "file_path": str(path),
        "file_name": path.name,
        "time": time,
        "signal": signal,
        "sample_rate": sample_rate,
        "signal_column": signal_column,
    }


def _find_signal_column(data):
    names = ["ECG", "ecg", "Signal", "signal", "Voltage", "voltage", "Value", "value"]
    for name in names:
        if name in data.columns:
            return name

    numeric_columns = []
    for column in data.columns:
        values = pd.to_numeric(data[column], errors="coerce")
        if values.notna().sum() >= 100:
            numeric_columns.append(column)

    if not numeric_columns:
        raise ValueError("Could not find a numeric ECG signal column.")

    # If there is a time column, prefer the other numeric column.
    for column in numeric_columns:
        if column.lower() not in {"time", "timestamp"}:
            return column

    return numeric_columns[0]


def _find_time_column(data):
    for name in ["Time", "time", "Timestamp", "timestamp"]:
        if name in data.columns:
            return name
    return None


def _calculate_sample_rate(time):
    if len(time) < 2:
        return None

    differences = np.diff(time)
    differences = differences[differences > 0]
    if len(differences) == 0:
        return None

    return float(1.0 / np.median(differences))
