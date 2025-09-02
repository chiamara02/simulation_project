# Simulation Project

![Python](https://img.shields.io/badge/Python-3.8%2B-blue?logo=python)
![License](https://img.shields.io/badge/license-Academic-lightgrey)

> **A modular simulation and evaluation framework for fuzzy, PID, and on-off heating controllers.**

---

## Table of Contents

- [Overview](#overview)
- [Folder Structure](#folder-structure)
- [Features](#features)
- [Getting Started](#getting-started)
- [Usage](#usage)
- [Customization](#customization)
- [Contributing](#contributing)
- [References](#references)
- [License](#license)

---

## Overview

This repository contains the main code, configuration, and analysis tools for a heating control simulation. The project is designed to evaluate and compare different control strategies for room heating, including fuzzy, PID, and on-off controllers, using simulation data and various evaluation metrics.

## Folder Structure

```
project/
├── bibtext.bib                  # Bibliography references
├── evaluation_metrics_table.md   # Table summarizing evaluation metrics
├── evaluation.md                # Evaluation methodology and results
├── README.md                    # (This file)
├── requirements.txt             # Python dependencies
├── configs/                     # Configuration files for simulations and controllers
├── evaluation/                  # Jupyter notebooks and scripts for data analysis and plotting
│   ├── correlations_plot.ipynb
│   ├── external_temperature_analisys.ipynb
│   ├── external_temperature_distribution.ipynb
│   ├── metrics_calculator_with_variance_reduction.ipynb
│   ├── metrics_calculator.ipynb
│   ├── metrics_plot.ipynb
│   ├── output_signal_plot.ipynb
│   └── plots/                   # Generated plots and figures
│       ├── correlations/
│       ├── metrics_comparison/
│       ├── output_distributions/
│       └── variance_reduction/
│   └── simulation_results/      # Simulation data (raw, clean, statistics)
│       ├── clean_data/
│       ├── raw_data/
│       └── statistics/
│   └── src/                     # Source code for metrics and data processing
│       ├── compute_distributions.py
│       ├── data_loader.py
│       ├── metrics.py
├── simulator/                   # Simulation engine and controllers
│   ├── simulate.py
│   ├── controllers/             # Controller implementations (fuzzy, PID, on-off)
│   ├── scenarios/               # Simulation scenarios
│   └── simulation_engine/       # FMU wrapper and simulation generator
├── sources/                     # Reference papers and documentation
│   └── 1-s2.0-S0378778815304680-main.pdf
```

## Features

- Modular controller architecture (fuzzy, PID, on-off)
- FMU-based simulation engine
- Jupyter notebooks for in-depth analysis and visualization
- Easily extensible with new controllers, metrics, or scenarios
- Well-documented configuration and evaluation methodology

## Getting Started

### Prerequisites

- Python 3.8+
- Recommended: [scikit-fuzzy](https://pythonhosted.org/scikit-fuzzy/) for fuzzy logic extensions

### Installation

Clone the repository:

```bash
git clone <repository-url>
cd <repository-folder>/project
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## Usage

1. **Configure the system:**
	- Edit files in `configs/` and `simulator/controllers/` to adjust variables, membership functions, or rules.
2. **Run simulations:**
	- Execute:
	  ```bash
	  python simulator/simulate.py
	  ```
3. **Analyze results:**
	- Open and run the notebooks in `evaluation/` to analyze and visualize the results.

## Customization

- Add or modify controllers in `simulator/controllers/`
- Change simulation scenarios in `simulator/scenarios/`
- Update or add evaluation metrics in `evaluation/src/`

## Contributing

Contributions are welcome! Please open issues or submit pull requests for improvements, bug fixes, or new features.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a pull request

## References

- See `sources/` for related research papers.
- Bibliography in `bibtext.bib`.

## License

This project is for academic and research purposes. See LICENSE if present.