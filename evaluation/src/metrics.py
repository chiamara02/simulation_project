import numpy as np
import pandas as pd
import scipy.stats as stats

def settling_time(data: pd.DataFrame, output_var: str, target_val: float, disturbance_src: str) -> float:
    tolerance_band = 0.025 * abs(target_val)
    signal = data[output_var].values
    time = data['time'].values

    for i in range(len(signal)):
        within_band = np.abs(signal[i:] - target_val) < tolerance_band
        if np.all(within_band):
            return time[i]  # Settling time found, return it

    return time[-1]  # No settling time found, return last time as penalty



def steady_state_error(data: pd.DataFrame, output_var: str, target_var: float, disturbance_src: str) -> float:
    
    if output_var not in data.columns :
        raise ValueError("Output or target variable not found in DataFrame.")

    settling_t = settling_time(data,output_var, target_var, disturbance_src)
    steady_data = data[data['time'] >= settling_t]
    if steady_data.empty or len(steady_data) < 2:
        return np.nan  # No data after settling time
    steady_state_error_value = np.mean(steady_data[output_var] - target_var)
   
    return steady_state_error_value


def overshoot(data: pd.DataFrame, output_var: str, target_var: float, disturbance_src: str) -> float:
    
    if output_var not in data.columns :
        raise ValueError("Output or target variable not found in DataFrame.")

    overshoot_value = np.max(data[output_var]) - target_var
    return overshoot_value




def rise_time(data: pd.DataFrame, output_var: str, target_var: float, disturbance_src: str) -> float:

    if output_var not in data.columns :
        raise ValueError("Output or target variable not found in DataFrame.")
    
    rise_time = data['time'].iloc[-1]  # Default to last time if no rise time found
    for row in data.itertuples():
        if getattr(row, output_var) >= 0.985 * target_var:
            rise_time = getattr(row, 'time')
            break
    
    
    return rise_time


def mean_square_error(data: pd.DataFrame, output_var: str, target_var: float, disturbance_src: str) -> float:

    if output_var not in data.columns :
        raise ValueError("Output or target variable not found in DataFrame.")
    
    mse = ((target_var - data[output_var]) ** 2).sum() / len(data)
    return mse 


def energy_consumed(data: pd.DataFrame, output_var: str, target_var: float, disturbance_src: str) -> float:

    if output_var not in data.columns:
        raise ValueError("Output variable not found in DataFrame.")
    
    energy = np.sum(data["heatSourcePower"]) / (3600 * 1000)  # Convert to kWh

    return energy


def comfort_time(data: pd.DataFrame, output_var: str, target_var: float, disturbance_src: str) -> float:

    if output_var not in data.columns :
        raise ValueError("Output or target variable not found in DataFrame.")
    
    comfort_time = 0
    for row in data.itertuples():
        if abs(getattr(row, output_var) - target_var) < 0.025 * target_var:
            comfort_time += 1
    
    return comfort_time

def variance_after_settling(data: pd.DataFrame, output_var: str, target_var: float, disturbance_src: str) -> float:

    if output_var not in data.columns :
        raise ValueError("Output or target variable not found in DataFrame.")
    
    settling_time_value = settling_time(data, output_var, target_var, disturbance_src)
    steady_data = data[data['time'] >= settling_time_value]
    if steady_data.empty or len(steady_data) < 2:
        return np.nan  # No data after settling time
    variance_value = np.var(steady_data[output_var])

    return variance_value



def number_of_oscillations(data: pd.DataFrame, output_var: str, target_var: float, disturbance_src: str) -> int:

    if output_var not in data.columns :
        raise ValueError("Output or target variable not found in DataFrame.")
    
    oscillations = 0
    for i in range(1, len(data)):
        if (data[output_var].iloc[i] >= target_var and 
            data[output_var].iloc[i-1] < target_var) or \
           (data[output_var].iloc[i] <= target_var and 
            data[output_var].iloc[i-1] > target_var):
            oscillations += 1
    
    return oscillations


def recovery_time(data: pd.DataFrame, output_var: str, target_var: float, disturbance_src: str) -> float:

    if output_var not in data.columns :
        raise ValueError("Output or target variable not found in DataFrame.")
    
    disturbance_times = data['time'][ (data[disturbance_src] != data[disturbance_src].shift(1)) &
    (data[disturbance_src].shift(1) == 2)]
    
    #print(f"Disturbance times: {disturbance_times}") 
    recovery_times = []
    
    if disturbance_times.empty: return np.nan

    for i in range(len(disturbance_times)):
        start_time = disturbance_times.iloc[i]
        if (i < len(disturbance_times)- 1):
            end_time = disturbance_times.iloc[i+1]
            data_slice = data[(data['time'] >= start_time) & (data['time'] < end_time)]
        else:
            data_slice = data[data['time'] >= start_time]
    

        time_at_recovery = data_slice['time'][abs(target_var - data_slice[output_var]) <= 
                                                0.015 * abs(target_var)]
        if time_at_recovery.empty:  
            recovery_times.append(data_slice['time'].iloc[-1] - data_slice['time'].iloc[0])
            continue
        time_at_recovery = time_at_recovery.iloc[0]
        recovery_duration = time_at_recovery - data_slice['time'].iloc[0]
        recovery_times.append(recovery_duration)


    return np.mean(recovery_times)

