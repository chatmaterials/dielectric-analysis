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
        rows.append((float(parts[0]), float(parts[1]), float(parts[2])))
    if not rows:
        raise SystemExit("Optical spectrum file contains no data")
    peak = max(rows, key=lambda item: item[2])
    onset_candidates = [energy for energy, _, eps2 in rows if eps2 > 1e-6]
    onset = min(onset_candidates) if onset_candidates else None
    return {
        "path": str(path),
        "peak_energy_eV": peak[0],
        "peak_epsilon2": peak[2],
        "peak_epsilon1": peak[1],
        "onset_energy_eV": onset,
        "observations": ["Optical-response summary extracted from the sampled spectrum."],
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Analyze a simple optical-response spectrum.")
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
