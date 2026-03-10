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
    return {
        "path": str(path),
        "diagonal": diagonal,
        "isotropic_average": iso,
        "diagonal_anisotropy": anisotropy,
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
