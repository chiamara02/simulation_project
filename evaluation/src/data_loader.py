import os
import pandas as pd

def load_data(controller, sim_type, res_path=None):
    if res_path is None:
        # Get the current directory
        current_dir = os.getcwd()
        
        if os.path.basename(current_dir) == 'evaluation':
            res_path = os.path.join(current_dir, "simulation_results")
        else:
            res_path = os.path.join(current_dir, "simulation_results")

        if not os.path.exists(res_path):
            parent_dir = os.path.dirname(current_dir)
            res_path = os.path.join(parent_dir, "evaluation", "simulation_results")
            
    folder = os.path.join(res_path, sim_type, controller)
    if not os.path.exists(folder):
        raise FileNotFoundError(f"Folder {folder} does not exist.")
    dataframe = []
    for sim_dir in sorted(os.listdir(folder)):
        sim_path = os.path.join(folder, sim_dir, "simulation_results.csv")
        if os.path.exists(sim_path):
            dataframe.append(pd.read_csv(sim_path))
    return dataframe