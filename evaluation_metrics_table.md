## 1. Evaluation Without Noise or Variations

| **Eval method** | **General Definition**| **Definition our  project** | **CSV Metrics to Use** | **Formula** | **General Formula** |
|-----------------------|------------------------------------------------------------------|----------------------------------------------------------------------------------------------|---------------------------------------------|------------------------------------------------------------------------------|---------------------------------------------|
| **Steady-State Error** |  Deviation from reference after settlin | Difference between temperature inside the target area and the target temperature`| `temperatureSensor.T`, `TARGET_TEMPERATURE`| `SSE = mean(abs(temperatureSensor.T[-M:] - TARGET_TEMPERATURE[-M:]))`, where M isthe number of samples in the steady-state window| $\text{SSE} = \frac{1}{M} \sum_{i=N-M+1}^{N} abs(y_i - r_i)$|
| **Rise Time** | Time to go from a% to b% of response range [a and b are parameters to choose]| Time taken for `temperatureSensor.T` to rise toward `TARGET_TEMPERATURE`| `temperatureSensor.T`, `TARGET_TEMPERATURE`, `time`| `RiseTime = t_b% - t_a%`| |
| **Settling Time**      | Time to stay within ±ε% of setpoint | Time until `temperatureSensor.T` remains within ±ε% of `TARGET_TEMPERATURE`| `temperatureSensor.T`, `TARGET_TEMPERATURE`, `time`| `SettlingTime = last exit from ±ε% band`| |
| **Overshoot (%)**      | System's response to a sudden input change exceeds the intended output level, as a percentage | Max peak of `temperatureSensor.T` above `TARGET_TEMPERATURE`| `temperatureSensor.T`, `TARGET_TEMPERATURE`| `Overshoot = (max(temperatureSensor.T) - TARGET_TEMPERATURE) / TARGET_TEMPERATURE * 100`| |
| **Mean Square Error**  | average squared difference between the estimated values and the true value over time| Overall deviation from target temperature| `temperatureSensor.T`, `TARGET_TEMPERATURE` | `MSE = \sum((temperatureSensor.T - TARGET_TEMPERATURE)^2)`| $\text{MSE} = \frac{1}{N} \sum_{i=1}^{N} (y_i - r_i)^2 $|
| **Energy Used (Joules)**| Energy consumed by the system | Energy consumed by the controller | `heatSourcePower`, `time`| `Energy=`| |

---l

## 2. Evaluation With Sensor Noise

| **Eval method** | **General Definition**| **Definition our  project** | **CSV Metrics to Use** | **Formula** | **General Formula** |
|----------------------------|------------------------------------------------------------------|----------------------------------------------------------------------------------------------|---------------------------------------------|------------------------------------------------------------------------------|---------------------------------------------|
| **Steady-State Error**     | As above, using noisy signal | Use `temperatureSensor.T` instead of `temperatureSensor.T`| `temperatureSensor.T`, `TARGET_TEMPERATURE`| `SSE` = `$mean(mod(temperatureSensor.T - TARGET_TEMPERATURE))$`|
| **Rise Time**              | As above, with sensor noise| Rise behavior seen in `temperatureSensor.T`| `temperatureSensor.T`, `TARGET_TEMPERATURE`, `time`| `RiseTime = t_b% - t_a%`|
| **Settling Time**          | Time to enter and stay within ±ε% of setpoint| Noisy stabilization within setpoint | `temperatureSensor.T`, `TARGET_TEMPERATURE`, `time`| `SettlingTime = last exit of temperatureSensor.T from ±ε% TARGET_TEMPERATURE's band`|
| **Overshoot (%)**          | Max overshoot with noisy measurement| Peak `temperatureSensor.T` overshoot | `temperatureSensor.T`, `TARGET_TEMPERATURE`| `Overshoot = (max(temperatureSensor.T) - TARGET_TEMPERATURE) / TARGET_TEMPERATURE * 100`|
| **Mean Square Error**      | Average squared deviation from setpoint| Using noisy measurements| `temperatureSensor.T`, `TARGET_TEMPERATURE`| `MSE = mean((temperatureSensor.T - TARGET_TEMPERATURE)^2)`|
| **Energy Used (Joules)**   | Same as above | Control effort remains based on `heatSourcePower`| `heatSourcePower`, `time`| `Energy = `|
| **Variance After Settling**| Variability after system stabilizes| Fluctuation in `temperatureSensor.T` after settling| `temperatureSensor.T`, `time` | `Variance = var(temperatureSensor.T[t > t_settle])`|
| **Number of Oscillations** | Count of zero-crossings or peaks | Fluctuations of `temperatureSensor.T` around setpoint | `temperatureSensor.T`, `TARGET_TEMPERATURE`| `Oscillations = count crossings of TARGET_TEMPERATURE ± ε`|
| **Avg Recovery Time**      | Time to stabilize after disturbance or deviation | From large deviation back to ±ε% band | `temperatureSensor.T`, `TARGET_TEMPERATURE`, `time`| `RecoveryTime = t_recovered - t_deviation` |

---

## 3. Evaluation With Disturbances (Window Events)

| **Eval method** | **General Definition**| **Definition our  project** | **CSV Metrics to Use** | **Formula** | **General Formula** |
|----------------------------|------------------------------------------------------------------|----------------------------------------------------------------------------------------------|---------------------------------------------|------------------------------------------------------------------------------|---------------------------------------------|
| **Steady-State Error**     | As in case 1 | Use `temperatureSensor.T`, even under disturbance | `temperatureSensor.T`, `TARGET_TEMPERATURE`| `SSE = mean(mod(temperatureSensor.T - TARGET_TEMPERATURE))`|
| **Rise Time**              | As in case 1| Rise after temperature drop (e.g., window opened) | `temperatureSensor.T`, `TARGET_TEMPERATURE`, `time`| `RiseTime` |
| **Settling Time**          | As in case 1 | Stabilization after external disturbance | `temperatureSensor.T`, `TARGET_TEMPERATURE`, `time`| `SettlingTime = last exit from ±ε% band`|
| **Overshoot (%)**          | As in case 1 | Room may overreact when recovering from disturbance | `temperatureSensor.T`, `TARGET_TEMPERATURE` | `Overshoot = (max(temperatureSensor.T) - TARGET_TEMPERATURE) / TARGET_TEMPERATURE * 100`|
| **Mean Square Error**      | As in case 1 | Tracks deviation even with external events| `temperatureSensor.T`, `TARGET_TEMPERATURE`| `MSE = mean((temperatureSensor.T - TARGET_TEMPERATURE)^2)`|
| **Energy Used (Joules)**   | As in case 1 | Often increases under disturbances | `heatSourcePower`, `time`| `Energy `|
| **Variance After Settling**| As in case 2 | Residual fluctuations after window closes | `temperatureSensor.T`, `time` | `Variance = var(temperatureSensor.T[t > t_settle])`|
| **Number of Oscillations** | As in case 2 | Peaks/swinging around setpoint due to overcorrection | `temperatureSensor.T`, `TARGET_TEMPERATURE`| `Oscillations = count crossings of TARGET_TEMPERATURE ± ε`|
| **Avg Recovery Time**      | Time to stabilize after disturbance (e.g., window change)| Time from `windowState` change to temperature re-stabilization| `temperatureSensor.T`, `TARGET_TEMPERATURE`, `windowState`  | `RecoveryTime = t_stable - t_disturbance_event`|
