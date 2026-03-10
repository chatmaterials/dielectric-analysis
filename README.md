# dielectric-analysis

[![CI](https://img.shields.io/github/actions/workflow/status/chatmaterials/dielectric-analysis/ci.yml?branch=main&label=CI)](https://github.com/chatmaterials/dielectric-analysis/actions/workflows/ci.yml) [![Release](https://img.shields.io/github/v/release/chatmaterials/dielectric-analysis?display_name=tag)](https://github.com/chatmaterials/dielectric-analysis/releases)

Standalone skill for dielectric and optical-response analysis from DFT results.

## Install

```bash
npx skills add chatmaterials/dielectric-analysis -g -y
```

## Local Validation

```bash
python3 -m py_compile scripts/*.py
npx skills add . --list
python3 scripts/analyze_dielectric_tensor.py fixtures/dielectric/dielectric_tensor.dat --json
python3 scripts/analyze_born_charges.py fixtures/born/born_charges.dat --json
python3 scripts/analyze_optical_response.py fixtures/optical/optical_spectrum.dat --json
python3 scripts/export_dielectric_report.py --dielectric-path fixtures/dielectric/dielectric_tensor.dat --born-path fixtures/born/born_charges.dat --optical-path fixtures/optical/optical_spectrum.dat
python3 scripts/run_regression.py
```
