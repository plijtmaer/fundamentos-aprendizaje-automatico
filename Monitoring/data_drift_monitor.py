import pandas as pd
from pathlib import Path
from evidently import Report
from evidently.presets import DataDriftPreset

BASE = Path(__file__).resolve().parent

def run_data_drift(reference_path: Path, current_path: Path, html_out: Path, order="current_first"):
    ref = pd.read_csv(reference_path)
    cur = pd.read_csv(current_path)

    report = Report(metrics=[DataDriftPreset()], include_tests=True)

    # Evidently 0.7.x (según tu snippet oficial): run(current, reference)
    result = report.run(cur, ref) if order == "current_first" else report.run(ref, cur)

    html_out.parent.mkdir(parents=True, exist_ok=True)
    result.save_html(str(html_out))
    print(f"[OK] Reporte guardado en: {html_out}")

if __name__ == "__main__":
    reference_csv = BASE / "reference.csv"
    current_csv   = BASE / "current.csv"
    out_html      = BASE / "data_drift_report.html"

    if not reference_csv.exists() or not current_csv.exists():
        raise FileNotFoundError(f"No encontré CSVs. Esperaba:\n- {reference_csv}\n- {current_csv}")

    run_data_drift(reference_csv, current_csv, out_html, order="current_first")
