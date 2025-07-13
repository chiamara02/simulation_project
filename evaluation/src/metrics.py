import numpy as np
import pandas as pd

def steady_state_error(data: pd.DataFrame, output_var: str, target_var: str) -> float:
    
    if output_var not in data.columns or target_var not in data.columns:
        raise ValueError("Output or target variable not found in DataFrame.")

    settling_time = settling_time(output_var, target_var)
    steady_state_error_value = np.mean(data[output_var].iloc[settling_time:] - data[target_var].iloc[settling_time:])
    return steady_state_error_value


def overshoot(data: pd.DataFrame, output_var: str, target_var: str) -> float:
    
    if output_var not in data.columns or target_var not in data.columns:
        raise ValueError("Output or target variable not found in DataFrame.")

    overshoot_value = np.max(data[output_var]) - np.max(data[target_var])
    return overshoot_value


def settling_time(data: pd.DataFrame, output_var: str, target_var: str) -> float:
    
    if output_var not in data.columns or target_var not in data.columns:
        raise ValueError("Output or target variable not found in DataFrame.")

    for row in data.itertuples():
        if abs(row[target_var] - row[output_var]) < 0.025 * np.max(data[target_var]):
            settling_time_value = row['time']
            break
    else:
        settling_time_value = np.nan  # If no settling time is found

    return settling_time_value


def rise_time(data: pd.DataFrame, output_var: str, target_var: str) -> float:

    if output_var not in data.columns or target_var not in data.columns:
        raise ValueError("Output or target variable not found in DataFrame.")
    
    for row in data.itertuples():
        if row[output_var] >= 0.9 * np.max(data[target_var]):
            rise_time = row['time'] - data['time'][0]
            break
    
    return rise_time


def mean_square_error(data: pd.DataFrame, output_var: str, target_var: str) -> float:

    if output_var not in data.columns or target_var not in data.columns:
        raise ValueError("Output or target variable not found in DataFrame.")
    
    mse = ((data[target_var] - data[output_var]) ** 2).sum() / len(data)
    return mse 


def energy_consumed(data: pd.DataFrame, output_var: str) -> float:

    if output_var not in data.columns:
        raise ValueError("Output variable not found in DataFrame.")
    
    energy = np.sum(data[output_var]) / (3600 * 1000)  # Convert to kWh

    return energy


def comfort_time(data: pd.DataFrame, output_var: str, target_var: str) -> float:

    if output_var not in data.columns or target_var not in data.columns:
        raise ValueError("Output or target variable not found in DataFrame.")
    
    comfort_time = 0
    for row in data.itertuples():
        if abs(row[output_var] - row[target_var]) < 0.025 * np.max(data[target_var]):
            comfort_time += 1
    
    return comfort_time

def variance_after_settling(data: pd.DataFrame, output_var: str, target_var: str) -> float:

    if output_var not in data.columns or target_var not in data.columns:
        raise ValueError("Output or target variable not found in DataFrame.")
    
    settling_time_value = settling_time(data, output_var, target_var)
    if np.isnan(settling_time_value):
        return np.nan
    
    variance_value = np.var(data[output_var].iloc[settling_time_value:])

    return variance_value



def number_of_oscillations(data: pd.DataFrame, output_var: str, target_var: str) -> int:

    if output_var not in data.columns or target_var not in data.columns:
        raise ValueError("Output or target variable not found in DataFrame.")
    
    oscillations = 0
    for i in range(1, len(data)):
        if (data[output_var].iloc[i] >= data[target_var].iloc[i] and 
            data[output_var].iloc[i-1] < data[target_var].iloc[i-1]) or \
           (data[output_var].iloc[i] <= data[target_var].iloc[i] and 
            data[output_var].iloc[i-1] > data[target_var].iloc[i-1]):
            oscillations += 1
    
    return oscillations


def recovery_time(data: pd.DataFrame, output_var: str, target_var: str, disturbance_src: str) -> float:

    if output_var not in data.columns or target_var not in data.columns:
        raise ValueError("Output or target variable not found in DataFrame.")
    
    disturbance_times = data['time'][data[disturbance_src] != data[disturbance_src].shift(1)]
    recovery_times = []
    
    if not disturbance_times: return float('nan')

    for i in range(len(disturbance_times)):
        start_time = disturbance_times[i]
        if (i < len(disturbance_times)- 1):
            end_time = disturbance_times[i+1]
            data_slice = data[(data['time'] >= start_time) & (data['time'] < end_time)]
        else:
            data_slice = data[data['time'] >= start_time]
    

        time_at_recovery = data_slice['time'][abs(data_slice[target_var] - data_slice[output_var]) <= 
                                           steady_state_error(data, output_var, target_var)]
        if not time_at_recovery: return float('nan')
        time_at_recovery = time_at_recovery.iloc[0]
        recovery_duration = time_at_recovery - data_slice['time'].iloc[0]
        recovery_times.append(recovery_duration)


    return np.mean(recovery_times)
