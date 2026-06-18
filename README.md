# Neuro-Computational Model of Decision Making

> A biologically plausible computational model of **neural decision-making**, implemented in Python and Jupyter Notebooks.  
> **Author:** Nasim Javdani · [GitHub](https://github.com/javdaninasim) · [LinkedIn](https://linkedin.com/in/nasim-javdani-810a9932a)

---

## Overview

This project models the neural dynamics underlying **perceptual decision-making** — the process by which the brain accumulates noisy sensory evidence and commits to a choice. The work bridges mathematical models and biologically plausible neural circuit implementations, drawing on frameworks from computational neuroscience.

---

## Repository Structure

```
Neuro-computational-Model-of-Decision/
├── 1_DriftDiffusionModel.ipynb        # Mathematical DDM: evidence accumulation
├── 2_AttractorNetwork.ipynb           # Recurrent neural circuit model (Wang 2002)
├── 3_ParameterFitting.ipynb           # Fitting model parameters to behavioral data
├── 4_SpeedAccuracyTradeoff.ipynb      # SAT analysis: boundary vs. accuracy
└── utils/
    ├── simulate.py                    # Core simulation functions
    └── plot.py                        # Visualization helpers
```

---

## Models

### 1. Drift-Diffusion Model (DDM)
A mathematical description of evidence accumulation:
- A noisy decision variable drifts toward one of two absorbing boundaries
- Parameters: drift rate (signal strength), diffusion coefficient (noise), boundary separation, non-decision time
- Generates reaction time distributions and error rates that match human psychophysics

### 2. Attractor Network Model
A biologically plausible recurrent neural network (Wang, 2002):
- Two excitatory populations representing the two choices compete via mutual inhibition
- Self-excitation (recurrence) creates winner-take-all dynamics
- Models the transition from an undecided state to a committed attractor
- Governed by stochastic differential equations (Euler-Maruyama integration)

### 3. Parameter Fitting
- Fitting DDM parameters (drift rate, boundary, NDT) to behavioral data using maximum likelihood estimation
- Validation against synthetic datasets

### 4. Speed-Accuracy Trade-off (SAT)
- Systematic analysis of how boundary separation controls the trade-off between fast responses and accuracy
- Psychometric and chronometric functions

---

## Background

Decision-making involves neural circuits in the lateral intraparietal cortex (LIP), prefrontal cortex (PFC), and basal ganglia. This project translates known neurophysiological findings into solvable mathematical models. The attractor network reproduces key experimental signatures including ramping activity, choice-dependent firing rates, and reaction time variability.

---

## Technologies

| Tool | Purpose |
|---|---|
| Python 3 | Core programming language |
| Jupyter Notebook | Interactive simulation and reporting |
| NumPy / SciPy | Numerical integration and optimization |
| Matplotlib | Visualization (RT distributions, phase planes, heatmaps) |

---

## How to Run

1. Clone the repository:
   ```bash
   git clone https://github.com/javdaninasim/Neuro-computational-Model-of-Decision.git
   cd Neuro-computational-Model-of-Decision
   ```
2. Install dependencies:
   ```bash
   pip install numpy scipy matplotlib jupyter
   ```
3. Run notebooks in order for a progressive build-up from DDM to the full circuit model.

---

## References

- Ratcliff, R. & McKoon, G. (2008). *The diffusion decision model.* Psychological Review.
- Wang, X.J. (2002). *Probabilistic decision making by slow reverberation in cortical circuits.* Neuron.
- Gold, J.I. & Shadlen, M.N. (2007). *The neural basis of decision making.* Annual Review of Neuroscience.

---

## Course Info

- **Topic:** Computational Neuroscience / Neuro-AI
- **Institution:** Sharif University of Technology, Department of Computer Engineering
