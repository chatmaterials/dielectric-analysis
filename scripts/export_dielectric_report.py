#!/usr/bin/env python3

from __future__ import annotations

import argparse
from pathlib import Path

from analyze_born_charges import analyze as analyze_born
from analyze_dielectric_tensor import analyze as analyze_tensor
from analyze_optical_response import analyze as analyze_optical


def render_markdown(tensor: dict[str, object] | None, born: dict[str, object] | None, optical: dict[str, object] | None) -> str:
    lines = ["# Dielectric Analysis Report", ""]
    if tensor is not None:
        lines.extend(
            [
                "## Dielectric Tensor",
                f"- Isotropic average: `{tensor['isotropic_average']:.4f}`",
                f"- Diagonal anisotropy: `{tensor['diagonal_anisotropy']:.4f}`",
                "",
            ]
        )
    if born is not None:
        lines.extend(
            [
                "## Born Effective Charges",
                f"- Largest isotropic charge: `{born['largest_isotropic_charge']:.4f}`",
                "",
            ]
        )
    if optical is not None:
        lines.extend(
            [
                "## Optical Response",
                f"- Onset energy (eV): `{optical['onset_energy_eV']:.4f}`",
                f"- Peak energy (eV): `{optical['peak_energy_eV']:.4f}`",
                f"- Peak epsilon2: `{optical['peak_epsilon2']:.4f}`",
                "",
            ]
        )
    return "\n".join(lines).rstrip() + "\n"


def main() -> None:
    parser = argparse.ArgumentParser(description="Export a markdown dielectric-analysis report.")
    parser.add_argument("--dielectric-path")
    parser.add_argument("--born-path")
    parser.add_argument("--optical-path")
    parser.add_argument("--output")
    args = parser.parse_args()
    tensor = analyze_tensor(Path(args.dielectric_path).expanduser().resolve()) if args.dielectric_path else None
    born = analyze_born(Path(args.born_path).expanduser().resolve()) if args.born_path else None
    optical = analyze_optical(Path(args.optical_path).expanduser().resolve()) if args.optical_path else None
    if tensor is None and born is None and optical is None:
        raise SystemExit("Provide at least one analysis input")
    output = Path(args.output).expanduser().resolve() if args.output else Path.cwd() / "DIELECTRIC_REPORT.md"
    output.write_text(render_markdown(tensor, born, optical))
    print(output)


if __name__ == "__main__":
    main()
