# Explainable Failure Analysis in Time-Series Data Using SHAP

**Author:** Abdul Karim Nasir Siddiqui  
**Institution:** Friedrich-Alexander-Universität Erlangen-Nürnberg (FAU)  
**Institute:** Institute of Autonomous Systems and Mechatronics (ASM)  
**Supervisor:** Prof. Dr.-Ing. habil. Philipp Beckerle  
**Period:** May – October 2025

---

## Overview

This repository contains the code, experiments, and LaTeX thesis for a Master's thesis on **explainable failure analysis** in time-series sensor data from mobile robots.

The core question: *Which sensor feature, at which exact timestep, caused an ML model to predict a failure?*

Three failure scenarios are studied:
1. Object stuck underneath the robot
2. Wheel entanglement (cable/wire around wheel)
3. Extreme battery depletion

Three SHAP methods are compared:
- **TimeSHAP** — extends KernelSHAP to sequential/recurrent models
- **WinIT** — window-based temporal attribution (state of the art)
- **KernelSHAP** — classical SHAP baseline

Three datasets are used:
- **SQL database** — existing statistical features from ASM lab robot
- **ROS2 data** — raw sensor data collected in this thesis
- **NASA CMAPSS** — public turbofan engine benchmark

---

## Quickstart: Open in DevContainer

1. Install [Docker Desktop](https://www.docker.com/products/docker-desktop/) and [VSCode](https://code.visualstudio.com/)
2. Install the [Dev Containers extension](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers)
3. Clone this repo: `git clone <repo-url>`
4. Open the folder in VSCode — click **"Reopen in Container"** when prompted
5. Wait for the container to build (first time ~10 min)

---

## Repository Structure

```
thesis-repo/
├── .devcontainer/      # Docker + VSCode DevContainer config
├── .github/            # CI, issue templates
├── data/               # Raw and processed data (gitignored)
├── notebooks/          # Exploratory Jupyter notebooks
├── src/                # All production Python code
│   ├── data/           # Data loaders and preprocessor
│   ├── models/         # LSTM/GRU classifiers and trainer
│   ├── explainability/ # SHAP method wrappers and evaluator
│   └── visualization/  # Heatmaps and comparison plots
├── tests/              # Pytest test suite
├── results/            # Generated figures and metrics CSVs
├── thesis/             # LaTeX source
└── scripts/            # Pipeline runner and ROS2 data collection
```

---

## Running the Pipeline

```bash
# Full end-to-end run
python scripts/run_pipeline.py --dataset cmapss --model lstm --explainer timeshap

# Available options
--dataset   sql | ros2 | cmapss
--model     lstm | gru
--explainer timeshap | winit | kernel
```

---

## Compiling the Thesis PDF

Inside the DevContainer:

```bash
cd thesis
latexmk -xelatex main.tex
# Output: thesis/output/main.pdf
```

---

## Supervisor Collaboration

See [CONTRIBUTING.md](CONTRIBUTING.md) for how to give feedback, open issues, and review progress — no Git knowledge required.
