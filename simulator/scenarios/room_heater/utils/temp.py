import numpy as np
import matplotlib.pyplot as plt
import datetime as dt
from meteostat import Hourly, Point
import pandas as pd


def simulate_temperature(day, month, start_time, end_time):

    """
    Simulate temperature data for a given day and time range.
    """
    
    vancouver = Point(49.2497, -123.1193, 70)
    start = dt.datetime(2023, month, day, start_time)
    end = dt.datetime(2023, month, day, end_time)
    
    data = Hourly(vancouver, start, end)
    data = data.fetch()
    #print(data.columns)
    data = data[['temp']]
    
 
    #print(f"Fetched data for {day}/{month} from {start_time} to {end_time}")
    #print(data)
    
    
    return data


def interpolate_temperatures(df, col="temp", freq=10, noise_scale=0.1): 
    
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

       # Skip segment if no intermediate time points
        if n < 2:
            continue

        # Initialize segment values
        segment = [v0]
        last_point = v0
        direction = 1 if v1 >= last_point else -1

        for _ in range(n - 2):  # Exclude first and last points

            attempts = 0
            while attempts < 100:  # Limit attempts to avoid infinite loop
                attempts += 1
                candidate = segment[-1] + np.random.normal(0, noise_scale)
                if direction == 1 and last_point <= candidate <= v1:
                    break
                elif direction == -1 and v1 <= candidate <= last_point:
                    break
            segment.append(candidate)
            last_point = candidate

        segment.append(v1)  # Final value must match v1

        result.extend(segment)
        times.extend(time_range)

    # Add last point from df
    result.append(df.iloc[-1][col])
    times.append(df.index[-1])

    return pd.DataFrame({col: result}, index=times)


# Example simulation
#temps = simulate_temperature(23, 2, 17, 22)
#final_temps = interpolate_temperatures(temps, noise_scale=0.2)
#print(final_temps)
# #Plotting the results
#plt.figure(figsize=(12, 6))
#plt.plot(final_temps.index, final_temps['temp'], label='Simulated Temperature', color='blue', marker='o', markersize=4)
#plt.title('Simulated Temperature Over Time')
#plt.xlabel('Time')
#plt.ylabel('Temperature (°C)')
#plt.xticks(rotation=45)
#plt.grid()
#plt.legend()
#plt.show()