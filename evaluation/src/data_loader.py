import os
import pandas as pd

def load_data(controller, sim_type, res_path=None):
    if res_path is None:
        # Get the current directory
        current_dir = os.getcwd()
        
        if os.path.basename(current_dir) == 'evaluation':
            res_path = os.path.join(current_dir, "simulation_results/raw_data")
        else:
            res_path = os.path.join(current_dir, "simulation_results/raw_data")

        if not os.path.exists(res_path):
            parent_dir = os.path.dirname(current_dir)
            res_path = os.path.join(parent_dir, "evaluation", "simulation_results/raw_data")
            
    folder = os.path.join(res_path, sim_type, controller)
    if not os.path.exists(folder):
        raise FileNotFoundError(f"Folder {folder} does not exist.")
    dataframe = []
    for sim_dir in sorted(os.listdir(folder)):
        sim_path = os.path.join(folder, sim_dir, "simulation_results.csv")
        if os.path.exists(sim_path):
            frame = pd.read_csv(sim_path)
            frame = frame.rename(columns=lambda x: x.replace('.', '_'))
            dataframe.append(frame)
            

    return dataframe

def clean_and_merge_data(dataframes, scenario_name, columns_to_keep):
    if not dataframes:
        return pd.DataFrame()
    
    cleaned_frames = []
    for i, frame in enumerate(dataframes):
        if columns_to_keep:
            cleaned_frame = frame[columns_to_keep]
        else:
            cleaned_frame = frame.dropna(axis=1, how='all')
        
        # Add simulation_run column
        cleaned_frame['simulation_run'] = i
        cleaned_frames.append(cleaned_frame)

    merged_df = pd.concat(cleaned_frames, ignore_index=True)

    
    merged_df.drop_duplicates(inplace=True)
    merged_df.reset_index(drop=True, inplace=True)
    os.makedirs("simulation_results/clean_data", exist_ok=True)
    merged_df.to_csv(f"simulation_results/clean_data/{scenario_name}.csv", index=False)
    
    return merged_df