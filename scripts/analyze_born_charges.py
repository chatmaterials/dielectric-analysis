#!/usr/bin/env python3

from __future__ import annotations

import argparse
import json
from pathlib import Path


def parse_blocks(text: str) -> list[tuple[str, list[list[float]]]]:
    blocks = []
    lines = [line.rstrip() for line in text.splitlines()]
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        if not line:
            i += 1
            continue
        label = line
        matrix = []
        for j in range(3):
            parts = lines[i + 1 + j].split()
            matrix.append([float(x) for x in parts[:3]])
        blocks.append((label, matrix))
        i += 4
    return blocks


def analyze(path: Path) -> dict[str, object]:
    blocks = parse_blocks(path.read_text())
    atoms = []
    max_iso = None
    for label, matrix in blocks:
        iso = (matrix[0][0] + matrix[1][1] + matrix[2][2]) / 3.0
        atoms.append({"label": label, "isotropic_charge": iso})
        max_iso = iso if max_iso is None or abs(iso) > abs(max_iso) else max_iso
    return {
        "path": str(path),
        "atoms": atoms,
        "largest_isotropic_charge": max_iso,
        "observations": ["Born effective charge tensors were summarized into isotropic averages."],
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Analyze Born effective charge tensors.")
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
