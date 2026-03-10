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
    visible = [row for row in rows if 1.65 <= row[0] <= 3.30]
    visible_peak = max(visible, key=lambda item: item[2]) if visible else None
    visible_average = sum(item[2] for item in visible) / len(visible) if visible else 0.0
    if onset is not None and onset >= 3.0 and visible_average <= 0.2:
        optical_class = "transparent-like"
    elif visible_average <= 0.8:
        optical_class = "moderate-loss-like"
    else:
        optical_class = "lossy-visible-like"
    return {
        "path": str(path),
        "peak_energy_eV": peak[0],
        "peak_epsilon2": peak[2],
        "peak_epsilon1": peak[1],
        "onset_energy_eV": onset,
        "visible_peak_energy_eV": visible_peak[0] if visible_peak is not None else None,
        "visible_peak_epsilon2": visible_peak[2] if visible_peak is not None else None,
        "visible_average_epsilon2": visible_average,
        "optical_class": optical_class,
        "transparent_visible_hint": onset is not None and onset >= 3.0,
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
