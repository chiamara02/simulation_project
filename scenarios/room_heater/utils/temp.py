import numpy as np
import matplotlib.pyplot as plt
import datetime as dt
from meteostat import Hourly, Point
import pandas as pd


def simulate_temperature(day, month, start_time, end_time, seed=None):

    """
    Simulate temperature data for a given day and time range.
    """

    if seed is not None:
        np.random.seed(seed)
    
    vancouver = Point(49.2497, -123.1193, 70)
    start = dt.datetime(2023, month, day, start_time)
    end = dt.datetime(2023, month, day, end_time)
    
    data = Hourly(vancouver, start, end)
    data = data.fetch()
    print(data.columns)
    data = data[['temp']]
    
 
    print(f"Fetched data for {day}/{month} from {start_time} to {end_time}")
    print(data)
    
    
    return data


def interpolate_temperatures(df, col="temp", freq=10, noise_scale=0.1): # TODO repeat sampling to obtain exactly n values in range
    
    """ 
    Enrich temperature data generating values at a specified frequency 
    by adding random noise to a linear interpolation between points.
    """
    
    result = []
    times = []

    for i in range(len(df) - 1):
        t0, t1 = df.index[i], df.index[i+1]
        v0, v1 = df.iloc[i][col], df.iloc[i+1][col]
        
        time_range = pd.date_range(t0, t1, freq=f"{freq}min")
        n = len(time_range)

        base = np.linspace(v0, v1, n)
        noise = np.random.normal(0, noise_scale, n).cumsum()
        noise -= np.linspace(0, noise[-1], n)  # anchor start and end
        segment = base + noise

        result.extend(segment[:-1])
        times.extend(time_range[:-1])

    # Add final point
    result.append(df.iloc[-1][col])
    times.append(df.index[-1])

    return pd.DataFrame({col: result}, index=times)

# Example simulation
#temps = simulate_temperature(23, 8, 6, 12)

#final_temps = random_walk_interpolate(temps, noise_scale=0.2)
#print(final_temps)

# Plotting the results
#plt.figure(figsize=(12, 6))
#plt.plot(final_temps.index, final_temps['temp'], label='Simulated Temperature', color='blue')
#plt.title('Simulated Temperature Over Time')
#plt.xlabel('Time')
#plt.ylabel('Temperature (°C)')
#plt.xticks(rotation=45)
#plt.grid()
#plt.legend()
#plt.show()