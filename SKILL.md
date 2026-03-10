---
name: "dielectric-analysis"
description: "Use when the task is to analyze dielectric and optical-response quantities from DFT results, including dielectric tensors, Born effective charges, optical spectra, dielectric-screening heuristics, candidate ranking, and compact markdown reports from finished calculations."
---

# Dielectric Analysis

Use this skill for dielectric and optical-response post-processing rather than generic workflow setup.

## When to use

- summarize a static or high-frequency dielectric tensor
- inspect Born effective charges
- summarize a simple optical spectrum
- rank multiple dielectric candidates with a compact high-k and anisotropy heuristic
- write a compact dielectric-analysis report from existing calculations

## Use the bundled helpers

- `scripts/analyze_dielectric_tensor.py`
  Summarize a dielectric tensor, anisotropy measures, and a compact dielectric class.
- `scripts/analyze_born_charges.py`
  Summarize Born effective charge tensors, isotropic averages, and anomalous-charge labels.
- `scripts/analyze_optical_response.py`
  Summarize a simple optical spectrum, identify visible-range peaks, and estimate a transparency hint.
- `scripts/compare_dielectric_candidates.py`
  Rank multiple dielectric candidates with a compact high-k and anisotropy heuristic.
- `scripts/export_dielectric_report.py`
  Export a markdown dielectric-analysis report.

## Guardrails

- Distinguish raw tensor extraction from deeper lattice-dynamical interpretation.
- Treat simple optical summaries as descriptors, not full spectroscopy analysis.
- State clearly when the analysis is a compact summary rather than a full dielectric workflow.
