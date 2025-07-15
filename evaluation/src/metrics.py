import numpy as np
import pandas as pd
import scipy.stats as stats

def settling_time(data: pd.DataFrame, output_var: str, target_var: float, disturbance_src: str) -> float:
    
    if output_var not in data.columns :
        raise ValueError("Output or target variable not found in DataFrame.")

    for row in data.itertuples():
        if abs(target_var - getattr(row, output_var)) < 0.025 * target_var:
            settling_time_value = getattr(row, 'time')
            break
    else:
        settling_time_value = np.nan  # If no settling time is found

    return settling_time_value

def steady_state_error(data: pd.DataFrame, output_var: str, target_var: float, disturbance_src: str) -> float:
    
    if output_var not in data.columns :
        raise ValueError("Output or target variable not found in DataFrame.")

    settling_t = settling_time(data,output_var, target_var, disturbance_src)
    steady_data = data[data['time'] >= settling_t]
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
    
    for row in data.itertuples():
        if getattr(row, output_var) >= 0.99 * target_var:
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
    
    energy = np.sum(data[output_var]) / (3600 * 1000)  # Convert to kWh

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
    if np.isnan(settling_time_value):
        return np.nan
    
    steady_data = data[data['time'] >= settling_time_value]
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
    
    disturbance_times = data['time'][(data[disturbance_src] != data[disturbance_src].shift(1)) & data[disturbance_src] != 2]
    recovery_times = []
    
    if disturbance_times.empty: return float('nan')

    for i in range(len(disturbance_times)):
        start_time = disturbance_times[i]
        if (i < len(disturbance_times)- 1):
            end_time = disturbance_times[i+1]
            data_slice = data[(data['time'] >= start_time) & (data['time'] < end_time)]
        else:
            data_slice = data[data['time'] >= start_time]
    

        time_at_recovery = data_slice['time'][abs(target_var - data_slice[output_var]) <= 
                                           steady_state_error(data, output_var, target_var, disturbance_src)]
        if time_at_recovery.empty: return float('nan')
        time_at_recovery = time_at_recovery.iloc[0]
        recovery_duration = time_at_recovery - data_slice['time'].iloc[0]
        recovery_times.append(recovery_duration)


    return np.mean(recovery_times)


def compute_confidence_interval(data, confidence=0.95):
    data = np.array(data)
    # Remove NaN values
    data = data[~np.isnan(data)]  
    if len(data) == 0:
        return np.nan, np.nan, np.nan
    
    n = len(data)
    mean = np.mean(data)
    std = np.std(data, ddof=1)
    z = stats.norm.ppf(1 - (1 - confidence) / 2)
    ci_lower = mean - z * (std / np.sqrt(n))
    ci_upper = mean + z * (std / np.sqrt(n))
    return mean, ci_lower, ci_upper

def compute_variance_confidence_interval(data, confidence=0.95):
    """Using chi-squared distribution"""
    data = np.array(data)
    data = data[~np.isnan(data)] 
    if len(data) <= 1:
        return np.nan, np.nan, np.nan
    
    n = len(data)
    var = np.var(data, ddof=1)
    df = n - 1
    
    # Chi-squared critical values
    chi2_lower = stats.chi2.ppf((1 - confidence) / 2, df)
    chi2_upper = stats.chi2.ppf(1 - (1 - confidence) / 2, df)
    
    var_ci_lower = (df * var) / chi2_upper
    var_ci_upper = (df * var) / chi2_lower
    
    return var, var_ci_lower, var_ci_upper