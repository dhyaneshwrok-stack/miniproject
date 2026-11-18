from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle


def generate_pdf_report(output_path, patient_name, patient_id, result):
    """Create a simple PDF summary from an ECG analysis result."""
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    styles = getSampleStyleSheet()
    document = SimpleDocTemplate(
        str(output_path),
        pagesize=A4,
        rightMargin=18 * mm,
        leftMargin=18 * mm,
        topMargin=18 * mm,
        bottomMargin=18 * mm,
    )

    story = [
        Paragraph("PulseMind ECG Analysis Report", styles["Title"]),
        Spacer(1, 8),
        Paragraph("Educational signal analysis report — not a medical diagnosis.", styles["Normal"]),
        Spacer(1, 12),
    ]

    patient_table = Table([
        ["Patient", patient_name or "Not provided"],
        ["Patient ID", patient_id or "Not provided"],
        ["Dataset", result.get("file_name", "")],
    ], colWidths=[35 * mm, 130 * mm])
    patient_table.setStyle(TableStyle([
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("BACKGROUND", (0, 0), (0, -1), colors.whitesmoke),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ]))
    story.append(patient_table)
    story.append(Spacer(1, 14))

    measurements = [
        ["Measurement", "Value"],
        ["Sampling rate", f"{result.get('sample_rate', 0):.2f} Hz"],
        ["Duration", f"{result.get('duration', 0):.2f} s"],
        ["Detected beats", str(result.get("beat_count", 0))],
        ["Heart rate", _format(result.get("heart_rate"), "BPM")],
        ["Average RR", _format(result.get("average_rr"), "s")],
        ["PR interval", _format(result.get("pr_ms"), "ms")],
        ["QRS duration", _format(result.get("qrs_ms"), "ms")],
        ["QT interval", _format(result.get("qt_ms"), "ms")],
        ["QTc", _format(result.get("qtc_ms"), "ms")],
        ["Status", result.get("status", "UNKNOWN")],
    ]
    table = Table(measurements, colWidths=[60 * mm, 105 * mm])
    table.setStyle(TableStyle([
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#E53935")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
    ]))
    story.append(table)
    story.append(Spacer(1, 14))

    story.append(Paragraph("Analysis Findings", styles["Heading2"]))
    for finding in result.get("findings", []):
        story.append(Paragraph(f"• {finding}", styles["BodyText"]))

    story.append(Spacer(1, 10))
    story.append(Paragraph(result.get("notes", ""), styles["BodyText"]))

    document.build(story)


def _format(value, unit):
    if value is None:
        return "Not estimated"
    return f"{float(value):.2f} {unit}"
