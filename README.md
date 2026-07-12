# Decision-Support Incentives Plotting Codebase

This repository contains the Signal Detection Theory (SDT) calculations, numerical simulation models, and plotting scripts for the paper: **"Effects of Reliance-Dependent Incentives on Algorithm-Supported Decision Making"**.

The code generates high-quality, publication-ready, IEEE-compatible grayscale figures using distinct line styles, markers, and hatches.

## Repository Structure

```
├── .gitignore                      # Git configuration to ignore output figures and caches
├── requirements.txt                # Project dependencies
├── README.md                       # Setup and run instructions
├── plot_sdt_contours.py            # Contour plots (Performance Benefit, Acceptance, Responsibility)
├── plot_sdt_thresholds.py          # SDT distributions & probability update thresholds
├── plot_behavioral_traps.py        # Phase space and odds boundary plots
├── plot_experiment_results.py      # Experimental metrics (Scores, d', subjective ratings)
└── src/
    ├── __init__.py
    ├── config.py                   # IEEE formatting presets and stylesheets
    ├── sdt_model.py                # Mathematical definitions (SDT simulation, V-ratio calculation)
    └── experimental_data.py        # Experimental dataset structures (means & CIs)
```

## Setup and Installation

1. Make sure Python 3.8+ is installed on your system.
2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Generating the Figures

You can run each plotting script individually:

- **Contour Grid Simulation & Plots**:
  ```bash
  python plot_sdt_contours.py
  ```
  Generates `Contour_IEEE_BW.png`.

- **SDT Distribution & Threshold Shifts**:
  ```bash
  python plot_sdt_thresholds.py
  ```
  Generates `sdt_thresholds_ieee.png`.

- **Behavioral Traps & universal phase space**:
  ```bash
  python plot_behavioral_traps.py
  ```
  Generates `academic_behavioral_traps_greyscale.png`.

- **Experimental Results**:
  ```bash
  python plot_experiment_results.py
  ```
  Generates:
  - `experiment_scores.png`
  - `experiment_d_prime.png`
  - `subjective_usefulness.png`
  - `subjective_self_success.png`
  - `subjective_automation_success.png`

## Custom CSV Data

If you have a CSV file containing your raw experiment logs, you can load and query it via the scaffolding in [experimental_data.py](file:///C:/Users/ordra/Documents/antigravity/beautiful-planck/src/experimental_data.py#L125-L132).
