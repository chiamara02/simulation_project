## 1. Evaluation Without Noise or Variations

| **Eval method** | **General Definition**| **Definition our  project** | **CSV Metrics to Use** | **Formula** | **General Formula** |
|-----------------------|------------------------------------------------------------------|----------------------------------------------------------------------------------------------|---------------------------------------------|------------------------------------------------------------------------------|---------------------------------------------|
| **Steady-State Error** |  Deviation from reference after settlin | Difference between temperature inside the target area and the target temperature`| `Room Air.T`, `heater.T_ref`| `SSE = mean(abs(roomAir.T[-M:] - heater.T_ref[-M:]))`, where M isthe number of samples in the steady-state window| $\text{SSE} = \frac{1}{M} \sum_{i=N-M+1}^{N} abs(y_i - r_i)$|
| **Rise Time** | Time to go from a% to b% of response range [a and b are parameters to choose]| Time taken for `roomAir.T` to rise toward `heater.T_ref`| `roomAir.T`, `heater.T_ref`, `time`| `RiseTime = t_b% - t_a%`| |
| **Settling Time**      | Time to stay within ±ε% of setpoint | Time until `roomAir.T` remains within ±ε% of `heater.T_ref`| `roomAir.T`, `heater.T_ref`, `time`| `SettlingTime = last exit from ±ε% band`| |
| **Overshoot (%)**      | System's response to a sudden input change exceeds the intended output level, as a percentage | Max peak of `roomAir.T` above `heater.T_ref`| `roomAir.T`, `heater.T_ref`| `Overshoot = (max(roomAir.T) - heater.T_ref) / heater.T_ref * 100`| |
| **Mean Square Error**  | average squared difference between the estimated values and the true value over time| Overall deviation from target temperature| `roomAir.T`, `heater.T_ref` | `MSE = \sum((roomAir.T - heater.T_ref)^2)`| $\text{MSE} = \frac{1}{N} \sum_{i=1}^{N} (y_i - r_i)^2 $|
| **Energy Used (Joules)**| Energy consumed by the system | Energy consumed by the controller | `heatSourcePower`, `time`| `Energy=`| |

---

## 2. Evaluation With Sensor Noise

| **Eval method** | **General Definition**| **Definition our  project** | **CSV Metrics to Use** | **Formula** | **General Formula** |
|----------------------------|------------------------------------------------------------------|----------------------------------------------------------------------------------------------|---------------------------------------------|------------------------------------------------------------------------------|---------------------------------------------|
| **Steady-State Error**     | As above, using noisy signal | Use `measuredTemp` instead of `roomAir.T`| `measuredTemp`, `heater.T_ref`| `SSE` = `$mean(mod(measuredTemp - heater.T_ref))$`|
| **Rise Time**              | As above, with sensor noise| Rise behavior seen in `measuredTemp`| `measuredTemp`, `heater.T_ref`, `time`| `RiseTime = t_b% - t_a%`|
| **Settling Time**          | Time to enter and stay within ±ε% of setpoint| Noisy stabilization within setpoint | `measuredTemp`, `heater.T_ref`, `time`| `SettlingTime = last exit of measuredTemp from ±ε% heater.T_ref's band`|
| **Overshoot (%)**          | Max overshoot with noisy measurement| Peak `measuredTemp` overshoot | `measuredTemp`, `heater.T_ref`| `Overshoot = (max(measuredTemp) - heater.T_ref) / heater.T_ref * 100`|
| **Mean Square Error**      | Average squared deviation from setpoint| Using noisy measurements| `measuredTemp`, `heater.T_ref`| `MSE = mean((measuredTemp - heater.T_ref)^2)`|
| **Energy Used (Joules)**   | Same as above | Control effort remains based on `heatSourcePower`| `heatSourcePower`, `time`| `Energy = `|
| **Variance After Settling**| Variability after system stabilizes| Fluctuation in `measuredTemp` after settling| `measuredTemp`, `time` | `Variance = var(measuredTemp[t > t_settle])`|
| **Number of Oscillations** | Count of zero-crossings or peaks | Fluctuations of `measuredTemp` around setpoint | `measuredTemp`, `heater.T_ref`| `Oscillations = count crossings of heater.T_ref ± ε`|
| **Avg Recovery Time**      | Time to stabilize after disturbance or deviation | From large deviation back to ±ε% band | `measuredTemp`, `heater.T_ref`, `time`| `RecoveryTime = t_recovered - t_deviation` |

---

## 3. Evaluation With Disturbances (Window Events)

| **Eval method** | **General Definition**| **Definition our  project** | **CSV Metrics to Use** | **Formula** | **General Formula** |
|----------------------------|------------------------------------------------------------------|----------------------------------------------------------------------------------------------|---------------------------------------------|------------------------------------------------------------------------------|---------------------------------------------|
| **Steady-State Error**     | As in case 1 | Use `roomAir.T`, even under disturbance | `roomAir.T`, `heater.T_ref`| `SSE = mean(mod(roomAir.T - heater.T_ref))`|
| **Rise Time**              | As in case 1| Rise after temperature drop (e.g., window opened) | `roomAir.T`, `heater.T_ref`, `time`| `RiseTime` |
| **Settling Time**          | As in case 1 | Stabilization after external disturbance | `roomAir.T`, `heater.T_ref`, `time`| `SettlingTime = last exit from ±ε% band`|
| **Overshoot (%)**          | As in case 1 | Room may overreact when recovering from disturbance | `roomAir.T`, `heater.T_ref` | `Overshoot = (max(roomAir.T) - heater.T_ref) / heater.T_ref * 100`|
| **Mean Square Error**      | As in case 1 | Tracks deviation even with external events| `roomAir.T`, `heater.T_ref`| `MSE = mean((roomAir.T - heater.T_ref)^2)`|
| **Energy Used (Joules)**   | As in case 1 | Often increases under disturbances | `heatSourcePower`, `time`| `Energy `|
| **Variance After Settling**| As in case 2 | Residual fluctuations after window closes | `roomAir.T`, `time` | `Variance = var(roomAir.T[t > t_settle])`|
| **Number of Oscillations** | As in case 2 | Peaks/swinging around setpoint due to overcorrection | `roomAir.T`, `heater.T_ref`| `Oscillations = count crossings of heater.T_ref ± ε`|
| **Avg Recovery Time**      | Time to stabilize after disturbance (e.g., window change)| Time from `windowState` change to temperature re-stabilization| `roomAir.T`, `heater.T_ref`, `windowState`  | `RecoveryTime = t_stable - t_disturbance_event`|
