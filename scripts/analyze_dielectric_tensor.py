#!/usr/bin/env python3

from __future__ import annotations

import argparse
import json
from pathlib import Path


def analyze(path: Path) -> dict[str, object]:
    rows = []
    for line in path.read_text().splitlines():
        parts = line.split()
        if len(parts) < 3:
            continue
        rows.append([float(x) for x in parts[:3]])
    if len(rows) != 3:
        raise SystemExit("Dielectric tensor file must contain 3 rows with at least 3 columns")
    diagonal = [rows[i][i] for i in range(3)]
    iso = sum(diagonal) / 3.0
    anisotropy = max(diagonal) - min(diagonal)
    min_diag = min(diagonal)
    max_diag = max(diagonal)
    anisotropy_ratio = max_diag / min_diag if abs(min_diag) > 1e-14 else None
    off_diagonal_norm = (
        sum(rows[i][j] ** 2 for i in range(3) for j in range(3) if i != j)
    ) ** 0.5
    refractive_index = iso**0.5 if iso > 0.0 else None
    energy_storage_proxy = iso / (1.0 + anisotropy + off_diagonal_norm)
    if iso >= 15.0:
        dielectric_class = "high-k"
    elif iso >= 8.0:
        dielectric_class = "moderate-k"
    else:
        dielectric_class = "low-k"
    return {
        "path": str(path),
        "diagonal": diagonal,
        "isotropic_average": iso,
        "diagonal_anisotropy": anisotropy,
        "anisotropy_ratio": anisotropy_ratio,
        "off_diagonal_norm": off_diagonal_norm,
        "refractive_index_estimate": refractive_index,
        "energy_storage_proxy": energy_storage_proxy,
        "dielectric_class": dielectric_class,
        "observations": ["Dielectric tensor summary extracted from the 3x3 tensor."],
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Analyze a dielectric tensor.")
    parser.add_argument("path")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    payload = analyze(Path(args.path).expanduser().resolve())
    if args.json:
        print(json.dumps(payload, indent=2))
        return
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
