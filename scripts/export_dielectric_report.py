#!/usr/bin/env python3

from __future__ import annotations

import argparse
from pathlib import Path

from analyze_born_charges import analyze as analyze_born
from analyze_dielectric_tensor import analyze as analyze_tensor
from analyze_optical_response import analyze as analyze_optical


def screening_note(tensor: dict[str, object] | None, optical: dict[str, object] | None) -> str:
    if tensor is None:
        return "Screening is incomplete without a dielectric tensor."
    if tensor["dielectric_class"] == "high-k":
        base = "The isotropic dielectric response already falls in a high-k regime."
    elif tensor["dielectric_class"] == "moderate-k":
        base = "The isotropic dielectric response is moderate and may still be useful if anisotropy remains controlled."
    else:
        base = "The isotropic dielectric response is low-k in this compact summary."
    if optical is None:
        return base
    if optical["transparent_visible_hint"]:
        return f"{base} The sampled optical onset is above the visible range, which is favorable for transparency-oriented screening."
    return f"{base} The sampled optical onset enters the visible range, so transparency may be limited."


def render_markdown(tensor: dict[str, object] | None, born: dict[str, object] | None, optical: dict[str, object] | None) -> str:
    lines = ["# Dielectric Analysis Report", ""]
    if tensor is not None:
        lines.extend(
            [
                "## Dielectric Tensor",
                f"- Isotropic average: `{tensor['isotropic_average']:.4f}`",
                f"- Diagonal anisotropy: `{tensor['diagonal_anisotropy']:.4f}`",
                f"- Anisotropy ratio: `{tensor['anisotropy_ratio']:.4f}`",
                f"- Refractive index estimate: `{tensor['refractive_index_estimate']:.4f}`",
                f"- Dielectric class: `{tensor['dielectric_class']}`",
                "",
            ]
        )
    if born is not None:
        lines.extend(
            [
                "## Born Effective Charges",
                f"- Largest isotropic charge: `{born['largest_isotropic_charge']:.4f}`",
                f"- Charge spread: `{born['charge_spread']:.4f}`",
                f"- Anomalous labels: `{', '.join(born['anomalous_labels']) if born['anomalous_labels'] else 'none'}`",
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
                f"- Visible peak energy (eV): `{optical['visible_peak_energy_eV']:.4f}`" if optical["visible_peak_energy_eV"] is not None else "- Visible peak energy (eV): `n/a`",
                f"- Transparent visible hint: `{optical['transparent_visible_hint']}`",
                "",
            ]
        )
    lines.extend(["## Screening Note", f"- {screening_note(tensor, optical)}", ""])
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
