def analyze_ecg(heart_rate, rr_intervals, irregular_beats, features):
    """
    Apply simple rule-based checks to an ECG signal.

    This is an academic demonstration only.
    It does not provide a medical diagnosis.
    """

    findings = []

    # Track whether any rule has flagged the result.
    flagged = False

    # ---------------------------------------------------------
    # 1. Check heart rate
    # ---------------------------------------------------------

    if heart_rate is None:
        findings.append(
            "Heart rate could not be calculated."
        )
        flagged = True

    elif heart_rate < 50:
        findings.append(
            "Low heart rate detected by the configured demo rules."
        )
        flagged = True

    elif heart_rate > 100:
        findings.append(
            "High heart rate detected by the configured demo rules."
        )
        flagged = True

    else:
        findings.append(
            "Heart rate is within the configured demo range."
        )

    # ---------------------------------------------------------
    # 2. Check irregular beat intervals
    # ---------------------------------------------------------

    if irregular_beats is not None and len(irregular_beats) > 0:
        findings.append(
            f"{len(irregular_beats)} beat interval(s) "
            "differ from the median RR interval."
        )
        flagged = True

    else:
        findings.append(
            "No large RR interval variation was flagged "
            "by the configured rules."
        )

    # ---------------------------------------------------------
    # 3. Check whether measurements were calculated
    # ---------------------------------------------------------

    measurement_names = {
        "pr_ms": "PR interval",
        "qrs_ms": "QRS duration",
        "qt_ms": "QT interval",
        "qtc_ms": "QTc",
    }

    for key, display_name in measurement_names.items():
        if features.get(key) is None:
            findings.append(
                f"{display_name} could not be estimated reliably."
            )

    # ---------------------------------------------------------
    # 4. Set final status
    # ---------------------------------------------------------

    if flagged:
        status = "FLAGGED"
        summary = (
            "The configured rules flagged one or more "
            "measurements or beat-interval checks."
        )
    else:
        status = "NORMAL"
        summary = (
            "No issues were flagged by the configured "
            "demo rules."
        )

    # ---------------------------------------------------------
    # 5. Return analysis results
    # ---------------------------------------------------------

    return {
        "status": status,
        "summary": summary,
        "findings": findings,
        "notes": (
            "This result is based on algorithmic signal-processing "
            "rules for an academic demonstration. NORMAL means "
            "that the configured rules did not flag the signal; "
            "it does not establish that the heart is medically normal. "
            "FLAGGED is not a medical diagnosis."
        ),
    }