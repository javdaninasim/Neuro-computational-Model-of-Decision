<div align="center">

<h1 align="center">🧠 Neuro-Computational Model of Decision Making</h1>
<h3 align="center">Neural Decision-Making Through Drift-Diffusion & Biologically Plausible Spiking Networks</h3>


[**GitHub**](https://github.com/javdaninasim/Neuro-computational-Model-of-Decision) &nbsp; ⬩ &nbsp; [**Sharif University**](https://sharif.edu/)

</div>

---

### 📚 Project Overview

This repository implements a **comprehensive computational model of perceptual decision-making**, bridging classical psychological models (Drift-Diffusion Model) with biologically realistic spiking neural networks. The work models how the brain accumulates noisy sensory evidence to make binary choices—a process fundamental to perception, recognition, and cognition.

**Key Focus:** Integrating neural dynamics with behavioral predictions across multiple decision-making paradigms.

---

### 🎯 Core Models & Concepts

#### **1. Drift-Diffusion Model (DDM)**
Mathematical abstraction of evidence accumulation:
- **Decision variable** drifts stochastically toward two absorbing boundaries
- **Parameters:** Drift rate (signal strength), diffusion coefficient (noise), boundary separation, non-decision time
- **Predictions:** Reaction time distributions, error rates matching human psychophysics
- **Applications:** Fits behavioral data; validates theoretical assumptions about decision processes

#### **2. Attractor Network Model (Spiking Network)**
Biologically plausible recurrent neural circuit based on Wang (2002):
- **Architecture:** Two competing excitatory populations (Choice A vs. Choice B) with mutual inhibition
- **Dynamics:** Self-excitation creates winner-take-all competition; models transition from neutral to committed attractor state
- **Integration:** Stochastic differential equations solved via Euler-Maruyama method
- **Neuron Model:** Leaky integrate-and-fire neurons with AMPA, NMDA, and GABA synapses
- **Circuit Properties:** Bistability, hysteresis, noise-driven transitions

#### **3. Parameter Fitting & Estimation**
- **Optimization:** Maximum likelihood estimation of DDM parameters
- **Objective:** Fit drift rate, boundary separation, and non-decision time to empirical behavioral data
- **Validation:** Synthetic datasets with known parameters; recovery analysis

#### **4. Speed-Accuracy Trade-off (SAT)**
Systematic exploration of boundary separation effects:
- **Psychometric curves:** Accuracy vs. stimulus strength (coherence/evidence level)
- **Chronometric curves:** Reaction time vs. stimulus strength
- **Trade-off dynamics:** How adjusting boundaries changes the speed-accuracy compromise
- **Neural correlates:** Firing rate changes in competing populations

---

### 📂 Repository Structure & Files

#### **Root Level – Analysis & Models**
| File | Size | Purpose |
|:---|:---:|:---|
| `decision_model.py` | 16.7 KB | **Main spiking neural network implementation**. Wang 2002 integration circuit with AMPA, NMDA, GABA synapses. Loads pre-trained CNN outputs as evidence and runs 600 trials with neural dynamics simulation. |
| `v.py` | 2.4 KB | **SVM Classification pipeline**. Binary classification (animal vs. non-animal) on neural population activity. Tests multiple kernels (linear, RBF, polynomial). Generates confusion matrices and evaluation metrics. |
| `test_model Amin.py` | 7.1 KB | **Deep learning feature extraction**. Loads 6 pre-trained Keras models (multi-layer CNNs); applies level-wise thresholding to generate 30×30 feature maps from 256×256 images. |
| `Figure_1.png` | 18.7 KB | Visual representation of model component (decision dynamics or network structure). |
| `Figure_2.png` | 18.2 KB | Comparative analysis or results visualization. |
| `Figure_3.png` | 19.0 KB | Additional figure (likely speed-accuracy or neural trajectory). |

#### **Pre-trained Models (Keras .h5 files)**
| File | Size | Description |
|:---|:---:|:---|
| `model_0final.h5` | 9.7 KB | Layer 1: Input convolution (small network) |
| `model_1final.h5` | 7.7 KB | Layer 2: Pooling operation |
| `model_2final.h5` | 298 KB | Layer 3: Large convolutional stage (primary feature extraction) |
| `model_3final.h5` | 7.7 KB | Layer 4: Pooling operation |
| `model_4final.h5` | 303 KB | Layer 5: Convolutional stage (higher-level features) |
| `model_5final.h5` | 7.7 KB | Layer 6: Final pooling |
| `model_6final.h5` | 7.7 KB | Output classification layer |

#### **Data Files (NumPy .npy arrays)**
| File | Size | Description |
|:---|:---:|:---|
| `pred_amin_all.npy` | 8.6 MB | Neural predictions from spiking model (shape: 600 trials × timesteps × 30×30 feature maps) |
| `pred_amin_normalized.npy` | 8.6 MB | Normalized predictions for stability |
| `R_DE1_amin.npy` | 1.4 MB | Population firing rates from decision circuit population DE1 across all trials |
| `R_DE2_amin.npy` | 1.4 MB | Population firing rates from decision circuit population DE2 across all trials |
| `y_amin_all.npy` | 274 KB | Image filenames/labels for all 600 trials |
| `y_amin_sorted.npy` | 19.3 KB | Sorted unique labels for classification mapping |

#### **📁 Report/ Folder**
Comprehensive project documentation and experimental results:
- **`Report.pdf`** (555 KB) – Full technical report with methods, results, and analysis
- **`Plots/`** – Generated visualizations (firing rate trajectories, phase planes, heatmaps)
- **`human's data/`** – Behavioral responses from human subjects performing the same decision task
- **`model's data/`** – Corresponding neural model outputs for comparison

#### **📁 TaskDesign/ Folder – Behavioral Experiment Setup**
MATLAB implementation of the psychophysical task:
- **`Task.m`** – Main task script (15.5 KB); displays visual stimuli and records subject responses
- **`Task.asv`** – Auto-saved backup
- **`getMouseResponse.m`** – Input handling for mouse-based responses
- **`getResponseWithTiming.m`** – Reaction time measurement and logging
- **`getMouseHighlight.m`** – Visual feedback during task
- **`drawConfidenceBar.m`** – Confidence rating UI
- **`scrambleImage.m`** – Image preprocessing and augmentation
- **`results.csv / results.mat`** – Raw behavioral data from test runs
- **`results1.csv / results1.mat`** – Extended trial data (93 KB) with detailed timing
- **`results2.csv / results2.mat`** – Additional dataset (93 KB) for validation

---

### ⚡ Technology Stack

<div align="left">
  <img src="https://img.shields.io/badge/Python-1A1A1A?style=for-the-badge&logo=python&logoColor=3776AB" alt="Python" />
  <img src="https://img.shields.io/badge/NumPy-1A1A1A?style=for-the-badge&logo=numpy&logoColor=013243" alt="NumPy" />
  <img src="https://img.shields.io/badge/SciPy-1A1A1A?style=for-the-badge&logo=scipy&logoColor=8CAAE6" alt="SciPy" />
  <img src="https://img.shields.io/badge/Keras-1A1A1A?style=for-the-badge&logo=keras&logoColor=D00000" alt="Keras" />
  <img src="https://img.shields.io/badge/TensorFlow-1A1A1A?style=for-the-badge&logo=tensorflow&logoColor=FF6F00" alt="TensorFlow" />
  <img src="https://img.shields.io/badge/OpenCV-1A1A1A?style=for-the-badge&logo=opencv&logoColor=5C3EE8" alt="OpenCV" />
  <img src="https://img.shields.io/badge/Matplotlib-1A1A1A?style=for-the-badge&logo=python&logoColor=11557C" alt="Matplotlib" />
  <img src="https://img.shields.io/badge/scikit--learn-1A1A1A?style=for-the-badge&logo=scikit-learn&logoColor=F7931E" alt="scikit-learn" />
  <img src="https://img.shields.io/badge/MATLAB-1A1A1A?style=for-the-badge&logo=mathworks&logoColor=ED1B24" alt="MATLAB" />
</div>

<br>

> **Core Dependencies:** `numpy` • `scipy` • `tensorflow` • `keras` • `opencv-python` • `scikit-learn` • `matplotlib` • `brian2`

---

### 🚀 Quick Start

```bash
# 1. Clone the repository
git clone https://github.com/javdaninasim/Neuro-computational-Model-of-Decision.git
cd Neuro-computational-Model-of-Decision

# 2. Create Python environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 3. Install dependencies
pip install numpy scipy tensorflow keras opencv-python scikit-learn matplotlib

# 4. Run neural simulation
python decision_model.py

# 5. Run SVM classification
python v.py

# 6. Extract features from images
python test_model\ Amin.py
```

---

### 📖 How to Use This Repository

**Pipeline Overview:**

1. **Feature Extraction** (`test_model Amin.py`)
   - Loads images from dataset
   - Applies Difference-of-Gaussians (DoG) filtering
   - Processes through 6-layer CNN cascade
   - Outputs 30×30 feature maps (`pred_amin_all.npy`)

2. **Neural Simulation** (`decision_model.py`)
   - Loads CNN features as evidence signals
   - Runs spiking network for 600 image stimuli
   - Integrates stochastic differential equations
   - Records population firing rates (DE1, DE2)
   - Saves neural activity (`R_DE1_amin.npy`, `R_DE2_amin.npy`)

3. **Classification & Analysis** (`v.py`)
   - Loads neural population activity
   - Trains SVM with multiple kernels
   - Evaluates binary classification (animal vs. non-animal)
   - Generates confusion matrices and metrics

4. **Results & Comparison**
   - Compare model predictions with human behavioral data
   - Analyze speed-accuracy trade-offs
   - Plot firing rate trajectories and phase planes

---

### 📊 Key Components & Architecture

#### **Spiking Neural Network (Wang 2002)**
```
Decision Circuit:
├─ Population D1 (Choice A - Selective)
│  ├─ Excitatory neurons (E1): 240 neurons
│  └─ Self-excitation: w_p = 1.65 (strong)
├─ Population D2 (Choice B - Selective)
│  ├─ Excitatory neurons (E2): 240 neurons
│  └─ Self-excitation: w_p = 1.65 (strong)
├─ Population DN (Non-selective)
│  ├─ Excitatory neurons (E3): 1120 neurons
│  └─ Self-excitation: w_m = 1.0 (weak)
├─ Inhibitory Population I: 400 neurons
│  └─ Global inhibition from all populations
└─ Synaptic Channels:
   ├─ AMPA: Fast excitation (τ = 2 ms)
   ├─ NMDA: Slow excitation (τ_decay = 100 ms)
   └─ GABA: Inhibition (τ = 5 ms)
```

#### **Decision Dynamics**
- **Bistability:** Two stable firing states (high/low rate)
- **Hysteresis:** Asymmetric transition thresholds
- **Attractor landscape:** Winner-take-all competition modeled by mutual inhibition
- **Stochasticity:** Poisson external input creates variability

---

### 💡 Key Findings & Insights

| Aspect | Finding | Implication |
|:---|:---|:---|
| **Neural Basis** | Decision populations show clear winner-take-all dynamics during stimulation | Matches neurophysiology of LIP, PFC, basal ganglia |
| **Speed-Accuracy** | Increasing boundary separation (more cautious) increases accuracy at cost of RT | Reconciles neural and behavioral data |
| **Feature Tuning** | CNN-extracted features feed into decision circuit with multiplicative modulation | Realistic sensory-motor coupling |
| **Population Coding** | Firing rate difference between DE1 and DE2 predicts choice | Linear classifier sufficient; supports decision variable hypothesis |

---

### 📝 Mathematical Foundation

**Drift-Diffusion Model:**
$$dX_t = \mu \, dt + \sigma \, dW_t$$

- $\mu$ = drift rate (evidence strength)
- $\sigma$ = diffusion coefficient (noise)
- $W_t$ = Wiener process
- Boundaries at $\pm a$; absorbing on first hit

**Spiking Network (Euler-Maruyama):**
$$C_m \frac{dV}{dt} = -g_{\text{leak}}(V - V_L) - I_E - I_I + I_{\text{ext}}$$

- Integrate-and-fire with multiple conductance channels
- AMPA/NMDA/GABA channels with separate dynamics
- Network operation every 5 ms bin

---

### 🎓 Learning & Application Domains

✅ **Computational Neuroscience** – Neural circuit models, decision-making mechanisms  
✅ **Cognitive Modeling** – Bridging neural and behavioral data  
✅ **Deep Learning** – CNN feature extraction as sensory input  
✅ **Biologically-Inspired AI** – Spiking neural networks for robotics/robotics  
✅ **Psychophysics** – Speed-accuracy trade-offs, reaction time distributions  
✅ **Brain-Computer Interfaces** – Real-time decision decoding from population activity  

---

### 📜 References & Theory

- **Wang, X.J.** (2002). *Probabilistic decision making by slow reverberation in cortical circuits.* **Neuron, 36**, 955–968. ⭐ **Core model paper**
- **Ratcliff, R. & McKoon, G.** (2008). *The diffusion decision model: Theory and data for two-choice decision tasks.* **Psychological Review, 115**, 873–925.
- **Gold, J.I. & Shadlen, M.N.** (2007). *The neural basis of decision making.* **Annual Review of Neuroscience, 30**, 535–574.
- **Huk, A.C. & Shadlen, M.N.** (2005). *Neural activity in macaque parietal cortex reflects temporal integration of visual motion signals during perceptual decision making.* **Journal of Neuroscience, 25**, 10420–10436.

---

### 📞 Project Information

| Detail | Information |
|:---|:---|
| **Institution** | Sharif University of Technology, Dept. of Computer Engineering |
| **Research Area** | Computational Neuroscience / Neuro-AI |
| **Topic** | Neural Bases of Decision-Making & Evidence Accumulation |
| **Primary Author** | Nasim Javdani |
| **Models Implemented** | Drift-Diffusion Model, Wang 2002 Spiking Circuit, CNN Feature Extraction |
| **Key Datasets** | 600 image trials, human behavioral responses, neural population recordings |

---

### 🌟 Highlights

🧠 **Biologically Realistic:** Based on validated neuroscience (Wang 2002)  
📊 **Multi-Scale Integration:** Links pixels → CNN features → neural dynamics → behavior  
🔬 **Reproducible:** Complete pipeline from raw images to neural simulations  
🎯 **Decision-Focused:** Models actual binary choice, not just classification  
⚡ **Spiking Networks:** Neuromorphic computing with spike-based dynamics  

---

### 📜 Attribution & License

This project contains computational models and experimental code from research in computational neuroscience at **Sharif University of Technology**, Department of Computer Engineering.

**Author:** Nasim Javdani  
**GitHub:** [@javdaninasim](https://github.com/javdaninasim)  
**LinkedIn:** [Nasim Javdani](https://linkedin.com/in/nasim-javdani-810a9932a)  

---

<div align="center">
  <img src="https://capsule-render.vercel.app/api?type=waving&color=2E86C1&height=100&section=footer" width="100%"/>
</div>
```

Copy this entire text! It's ready to paste directly into your README.md file.
