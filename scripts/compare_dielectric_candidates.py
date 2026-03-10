#!/usr/bin/env python3

from __future__ import annotations

import argparse
import json
from pathlib import Path

from analyze_born_charges import analyze as analyze_born
from analyze_dielectric_tensor import analyze as analyze_tensor
from analyze_optical_response import analyze as analyze_optical


def locate_required(root: Path, relative_paths: list[str]) -> Path:
    for relative in relative_paths:
        candidate = root / relative
        if candidate.exists():
            return candidate
    raise SystemExit(f"Could not locate any of {relative_paths} in {root}")


def analyze_case(root: Path, target_epsilon: float, max_anisotropy: float, minimum_onset: float, mode: str) -> dict[str, object]:
    tensor = analyze_tensor(locate_required(root, ["dielectric_tensor.dat", "dielectric/dielectric_tensor.dat"]))
    born = analyze_born(locate_required(root, ["born_charges.dat", "born/born_charges.dat"]))
    optical = analyze_optical(locate_required(root, ["optical_spectrum.dat", "optical/optical_spectrum.dat"]))

    epsilon_penalty = max(0.0, target_epsilon - float(tensor["isotropic_average"]))
    anisotropy_penalty = max(0.0, float(tensor["diagonal_anisotropy"]) - max_anisotropy)
    onset_value = float(optical["onset_energy_eV"]) if optical["onset_energy_eV"] is not None else 0.0
    onset_penalty = max(0.0, minimum_onset - onset_value)
    visible_penalty = max(0.0, float(optical["visible_average_epsilon2"]) - 0.3)
    loss_tangent_penalty = max(0.0, float(optical["loss_tangent_at_peak"]) - 0.5)
    if mode == "transparent":
        score = 0.5 * epsilon_penalty + anisotropy_penalty + 2.0 * onset_penalty + 2.0 * visible_penalty + loss_tangent_penalty
    elif mode == "high-k":
        score = 1.5 * epsilon_penalty + 0.5 * anisotropy_penalty + 0.5 * onset_penalty + 0.5 * visible_penalty + 0.25 * loss_tangent_penalty
    else:
        score = epsilon_penalty + anisotropy_penalty + onset_penalty + visible_penalty + 0.5 * loss_tangent_penalty
    return {
        "case": root.name,
        "path": str(root),
        "isotropic_average": tensor["isotropic_average"],
        "diagonal_anisotropy": tensor["diagonal_anisotropy"],
        "energy_storage_proxy": tensor["energy_storage_proxy"],
        "dielectric_class": tensor["dielectric_class"],
        "largest_isotropic_charge": born["largest_isotropic_charge"],
        "polarity_score": born["polarity_score"],
        "anomalous_count": born["anomalous_count"],
        "onset_energy_eV": optical["onset_energy_eV"],
        "visible_average_epsilon2": optical["visible_average_epsilon2"],
        "transparency_quality_score": optical["transparency_quality_score"],
        "loss_tangent_at_peak": optical["loss_tangent_at_peak"],
        "optical_class": optical["optical_class"],
        "transparent_visible_hint": optical["transparent_visible_hint"],
        "epsilon_penalty": epsilon_penalty,
        "anisotropy_penalty": anisotropy_penalty,
        "onset_penalty": onset_penalty,
        "visible_penalty": visible_penalty,
        "loss_tangent_penalty": loss_tangent_penalty,
        "screening_score": score,
    }


def analyze_cases(roots: list[Path], target_epsilon: float, max_anisotropy: float, minimum_onset: float, mode: str) -> dict[str, object]:
    cases = [analyze_case(root, target_epsilon, max_anisotropy, minimum_onset, mode) for root in roots]
    ranked = sorted(cases, key=lambda item: item["screening_score"])
    return {
        "target_epsilon": target_epsilon,
        "max_anisotropy": max_anisotropy,
        "minimum_onset_eV": minimum_onset,
        "mode": mode,
        "ranking_basis": "screening_score = weighted(epsilon_penalty, anisotropy_penalty, onset_penalty, visible_penalty, loss_tangent_penalty)",
        "cases": ranked,
        "best_case": ranked[0]["case"] if ranked else None,
        "observations": [
            "This is a compact dielectric-screening heuristic intended for candidate ranking, not a full polarizability workflow."
        ],
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Rank dielectric candidates with a compact high-k and anisotropy heuristic.")
    parser.add_argument("paths", nargs="+")
    parser.add_argument("--target-epsilon", type=float, default=5.0)
    parser.add_argument("--max-anisotropy", type=float, default=2.0)
    parser.add_argument("--minimum-onset", type=float, default=0.0)
    parser.add_argument("--mode", choices=["balanced", "transparent", "high-k"], default="balanced")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    payload = analyze_cases(
        [Path(path).expanduser().resolve() for path in args.paths],
        args.target_epsilon,
        args.max_anisotropy,
        args.minimum_onset,
        args.mode,
    )
    if args.json:
        print(json.dumps(payload, indent=2))
        return
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
