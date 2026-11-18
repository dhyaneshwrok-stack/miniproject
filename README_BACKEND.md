# PulseMind ECG Backend

This build adds the first working ECG analysis backend to the existing PySide6 UI.

## Pipeline

CSV/TXT ECG file
-> validation
-> filtering
-> R-peak detection
-> RR intervals
-> heart rate
-> approximate PR/QRS/QT/QTc measurements
-> rule-based flags
-> SQLite history
-> PDF report

## Technology

- Python
- PySide6
- Pandas
- NumPy
- SciPy
- Matplotlib
- SQLite
- ReportLab

## Run

Create/activate a virtual environment and install:

```bash
python -m pip install -r requirements.txt
```

Then:

```bash
python main.py
```

Open **ECG Analysis**, click **Load ECG File**, and select:

`samples/demo_ecg.csv`

The demo file is synthetic test data for checking the software pipeline. It is not a clinical ECG record.

## Important scope

PulseMind is an academic signal-analysis project. The ECG measurements and rule-based findings are software estimates for educational/demonstration use and are not a medical diagnosis or a substitute for clinical interpretation.
