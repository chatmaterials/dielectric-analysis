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
    born = run_json("scripts/analyze_born_charges.py", "fixtures/born/born_charges.dat", "--json")
    ensure(abs(born["largest_isotropic_charge"] - 2.1) < 1e-6, "dielectric-analysis should summarize Born charges")
    optical = run_json("scripts/analyze_optical_response.py", "fixtures/optical/optical_spectrum.dat", "--json")
    ensure(abs(optical["peak_energy_eV"] - 2.5) < 1e-6, "dielectric-analysis should find the strongest optical peak")
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
    finally:
        shutil.rmtree(temp_dir)
    print("dielectric-analysis regression passed")


if __name__ == "__main__":
    main()
