---
name: "dielectric-analysis"
description: "Use when the task is to analyze dielectric and optical-response quantities from DFT results, including dielectric tensors, Born effective charges, optical spectra, and compact markdown reports from finished calculations."
---

# Dielectric Analysis

Use this skill for dielectric and optical-response post-processing rather than generic workflow setup.

## When to use

- summarize a static or high-frequency dielectric tensor
- inspect Born effective charges
- summarize a simple optical spectrum
- write a compact dielectric-analysis report from existing calculations

## Use the bundled helpers

- `scripts/analyze_dielectric_tensor.py`
  Summarize a dielectric tensor and simple anisotropy measures.
- `scripts/analyze_born_charges.py`
  Summarize Born effective charge tensors and isotropic averages.
- `scripts/analyze_optical_response.py`
  Summarize a simple optical spectrum and identify the strongest absorption peak.
- `scripts/export_dielectric_report.py`
  Export a markdown dielectric-analysis report.

## Guardrails

- Distinguish raw tensor extraction from deeper lattice-dynamical interpretation.
- Treat simple optical summaries as descriptors, not full spectroscopy analysis.
- State clearly when the analysis is a compact summary rather than a full dielectric workflow.
