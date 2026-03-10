#!/usr/bin/env python3

from __future__ import annotations

import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def run(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run([sys.executable, *args], cwd=ROOT, text=True, capture_output=True, check=True)


def run_json(*args: str):
    return json.loads(run(*args).stdout)


def ensure(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def main() -> None:
    tensor = run_json("scripts/analyze_dielectric_tensor.py", "fixtures/dielectric/dielectric_tensor.dat", "--json")
    ensure(abs(tensor["isotropic_average"] - 5.1666666667) < 1e-6, "dielectric-analysis should summarize the dielectric tensor")
    ensure(tensor["dielectric_class"] == "low-k", "dielectric-analysis should classify the reference tensor")
    ensure(tensor["energy_storage_proxy"] > 1.9, "dielectric-analysis should compute an energy-storage proxy")
    born = run_json("scripts/analyze_born_charges.py", "fixtures/born/born_charges.dat", "--json")
    ensure(abs(born["largest_isotropic_charge"] - 2.1) < 1e-6, "dielectric-analysis should summarize Born charges")
    ensure(born["anomalous_count"] == 1, "dielectric-analysis should identify anomalous Born charges")
    ensure(born["polarity_score"] > 4.0, "dielectric-analysis should compute a polarity score")
    optical = run_json("scripts/analyze_optical_response.py", "fixtures/optical/optical_spectrum.dat", "--json")
    ensure(abs(optical["peak_energy_eV"] - 2.5) < 1e-6, "dielectric-analysis should find the strongest optical peak")
    ensure(not optical["transparent_visible_hint"], "dielectric-analysis should identify the reference fixture as visible-active")
    ensure(optical["optical_class"] == "lossy-visible-like", "dielectric-analysis should classify the visible optical loss regime")
    ranked = run_json(
        "scripts/compare_dielectric_candidates.py",
        "fixtures",
        "fixtures/candidates/opaque-lowk",
        "fixtures/candidates/highk-lossy",
        "--target-epsilon",
        "5.0",
        "--max-anisotropy",
        "2.0",
        "--minimum-onset",
        "0.0",
        "--json",
    )
    ensure(ranked["best_case"] == "fixtures", "dielectric-analysis should rank the stronger dielectric fixture ahead of the opaque low-k candidate")
    temp_dir = Path(tempfile.mkdtemp(prefix="dielectric-analysis-report-"))
    try:
        report_path = Path(
            run(
                "scripts/export_dielectric_report.py",
                "--dielectric-path",
                "fixtures/dielectric/dielectric_tensor.dat",
                "--born-path",
                "fixtures/born/born_charges.dat",
                "--optical-path",
                "fixtures/optical/optical_spectrum.dat",
                "--output",
                str(temp_dir / "DIELECTRIC_REPORT.md"),
            ).stdout.strip()
        )
        report_text = report_path.read_text()
        ensure("# Dielectric Analysis Report" in report_text, "dielectric report should have a heading")
        ensure("## Dielectric Tensor" in report_text and "## Born Effective Charges" in report_text and "## Optical Response" in report_text, "dielectric report should include all sections")
        ensure("## Screening Note" in report_text, "dielectric report should include a screening note")
    finally:
        shutil.rmtree(temp_dir)
    print("dielectric-analysis regression passed")


if __name__ == "__main__":
    main()
