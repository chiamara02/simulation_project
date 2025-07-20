# ✅ TODO: Evaluation Plan

## 1. Visual Inspection & Hypothesis Formulation

### 1.1 Plot Controller Output Over Time (3 scenarios × 3 controllers)
- [ ] For each **scenario** (nominal, noise, disturbances):
  - [ ] For each **controller** (pid, onoff, fuzzy):
    - [ ] Plot **output signal** over time
    
    result: have a 3*3 image with scenarios as rows and controllers as columns

### 1.2 Plot Output Signal Distributions (Histogram Overlays)
- [ ] For each **controller**:
  - [ ] Plot **histogram** of output signal for all 3 scenarios on same plot
  - [ ] Use scenario as 'hue' to differentiate the color for each scenario histogram in the same plot

  result: have a 3*1 image with a controller for each plot

### 1.3 Explore Relationships via Pairplots
- [x] Combine key variables:
  - output signal, actual temperature, outside temperature, noise (only noise scenario)
- [x] Generate **pairplot** for each scenario
  - use windowstate as hue to color the different points
  result: have 9 pairplots, one for each pair scenario/controller

---

## 2. Metrics & Variance Reduction

### 2.1 Estimate Distributions of Influencing Variables
- [x ] Plot or fit probability distributions for:
  - [x] Outside temperature 
  - [ ] Window state (markov chain) (no time)
  - [ ] Sensor noise (Gaussian) (no time)
  result: have a distribution for each variable, qq plot for temp distribution and original temp data, quantiles plot

### 2.2 Stratified Metrics Recalculation
- [x] Define bins or quantiles for stratification:
  - [x] Outside temperature (e.g., cold, moderate, hot)
  - [ ] Window state (open, closed, semi-open) (we probably do not have time for this)
- [x] Recalculate metrics (metrics in metrics.py) for each stratum
- [x] Compare variance before and after stratification
  result: have tables showing variance reduction and ci plot showing the reduction of ci for the mean

### 2.3 Discuss
- [ ] Summarize insights from:
  - [ ] Time series plots
  - [ ] Histogram overlays
  - [ ] Stratified metric tables
  result: text highlighting consistencies or contradictions between visual and quantitative findings

---

## 3. Correlation Analysis
- [ ] plot heatmaps showing potential correlations between variables

### 3.1 Correlation: Outside Temp vs. Energy Consumption
- [ ] For each scenario and controller:
  - [ ] Compute **Pearson correlation coefficient**
  - [ ] Plot scatter with regression line (optional)

### 3.2 Conditional Correlation: Window State
- [ ] For each temperature stratum:
  - [ ] Plot energy use (output of controller) vs. window state
  - [ ] Compute correlation (Pearson)


