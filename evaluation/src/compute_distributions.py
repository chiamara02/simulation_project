from pathlib import Path
import sys
import numpy as np
import pandas as pd
import argparse

# Navigate to the project root
project_root = Path(__file__).resolve().parents[3] / "project"
sys.path.append(str(project_root))

from simulator.scenarios.room_heater.utils.temp import simulate_temperature, interpolate_temperatures
#from simulator.scenarios.room_heater.room_heater import simulate_window_markov



def main():

    all_temperatures = pd.DataFrame()

    for i in [1, 2, 3, 4, 10, 11, 12]: # months
        for j in range(1,29):
            for k in range (0,21):

                temperature = simulate_temperature(j, i, k, k)
                all_temperatures = pd.concat([all_temperatures, temperature])
                print(f"Simulated temperature for month {i}, day {j}, hour {k}")
    
    print(f"Num of temp entries: {len(all_temperatures)}")
    all_temperatures.to_csv(project_root / "evaluation" / "simulation_results" / "clean_data"/"all_temperatures.csv", index=False)

if __name__ == "__main__":
    main()