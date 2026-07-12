# Effects of Reliance-Dependent Incentives on Algorithm-Supported Decision Making

This repository contains the code, data, and plotting scripts for the paper **"Effects of Reliance-Dependent Incentives on Algorithm-Supported Decision Making."** 

It includes the implementation of the discrete Expected Value (EV) framework, Signal Detection Theory (SDT) logic, and the scripts used to generate the grayscale figures presented in the paper.

---

## 📌 Overview

The code evaluates how different reliance-dependent incentive structures influence human decision-making when supported by an algorithm. 

* **Theoretical Framework**: Calculates optimal reliance thresholds based on an Expected Value (EV) method and Signal Detection Theory (SDT).
* **Experimental Results**: Includes behavioral data from an experiment with 544 participants. 
* **Reproducibility**: The repository provides everything needed to recreate the exact ANOVA graphs and contour plots (in academic grayscale) featured in the publication.

---

## 📂 Repository Structure

* **`main.py`**: The centralized execution script. Run this to generate all figures.
* **`utils.py`**: Contains core algorithmic logic and SDT calculations.
* **`ev_method.py`**: Isolates the Expected Value logic (Stage 1 Alert System and Stage 2 Posterior Probabilities).
* **`plotting.py`**: Houses the predefined data arrays and visualization configurations. Generates IEEE-style, high-resolution grayscale plots.
* **`data/`**: Contains the raw experimental data (`.csv` format) from the 544 participants. *Note: Plotting data is pre-configured in the Python scripts for immediate execution; the CSV is provided for raw data transparency and independent statistical analysis.*
* **`figures/`**: The output directory where `main.py` will save the generated `.png` plots.

---

## ⚙️ Installation & Requirements

This code requires **Python 3.7+**. 
