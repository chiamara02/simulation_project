import os
import json
import importlib
from FMUWrapper import FMUWrapper

CONFIG_DIR = "configs"

class SimulationGenerator:

    def __init__(self, scenario_name, duration, step_size, controller_type, simulation_id):

        self.scenario_name = scenario_name
        self.duration = duration
        self.step_size = step_size
        self.simulation_id = simulation_id
        self.controller_type = controller_type
        self.scenario_module = self.__import_scenario()
        self.fmu_path = self.__get_fmu_path()
        self.simulation_events_path = self.__generate_events()
        self.simulation_events = self.__load_events(self.simulation_events_path)
        self.controller = self.__get_controller()
        self.fmu_simulator = FMUWrapper(path=self.fmu_path, stop_time=self.duration, step_size=self.step_size)
        
    def __import_scenario(self):
        """
        Dynamically import the scenario script.
        """
        try:
            scenario_module = importlib.import_module(f"scenarios.{self.scenario_name}")
        except ImportError as e:
            raise ImportError(f"Scenario '{self.scenario_name}' could not be imported: {e}")
        return scenario_module

    def __generate_events(self):
        """
        Generate input event configuration.
        Saves it as JSON and returns the path.
        """

        if not hasattr(self.scenario_module, "generate_inputs"):
            raise AttributeError(f"Scenario '{self.scenario_name}' must define a 'generate_inputs' function")


        input_vars = self.scenario_module.generate_inputs(self.duration, self.step_size, self.simulation_id)

        # Save to JSON
        os.makedirs(CONFIG_DIR, exist_ok=True)
        json_path = os.path.join(CONFIG_DIR, f"{self.scenario_name}_sim_{self.simulation_id+1}.json")
        with open(json_path, "w") as f:
            json.dump(input_vars, f, indent=2)
        print(f"Generated input events saved to {json_path}")
        return json_path

    def __load_events(self, json_path):
        """
        Loads a JSON file into the input_vars format for the FMUWrapper.
        """
        with open(json_path, "r") as f:
            return json.load(f)

    def __get_controller(self):
        """
        Initialize the controller based on the type specified.
        """
        if not hasattr(self.scenario_module, "setup_controller"):
            raise AttributeError(f"Scenario '{self.scenario_name}' must define a 'setup_controller' function")        
       
        return self.scenario_module.setup_controller(self.controller_type)
    
    def __get_fmu_path(self):
        """
        Get the path to the FMU file based on the scenario name.
        """
        return self.scenario_module.get_fmu_path() 
    
    
    def run_simulation(self):
        """
        Run the FMU simulation with the generated input events and controller.
        """
                
        self.fmu_simulator.initialize_fmu()

        times, plot_data, simulation_data = self.fmu_simulator.simulate_with_controller(
            input_vars=self.simulation_events,
            controller=self.controller,
            plot_vars=[]
        )

        return times, simulation_data


    def save_results_to_csv(self, times, simulation_data, output_path):
        """
        Save the simulation results to a CSV file.
        """
        self.fmu_simulator.save_results_to_csv(times, simulation_data, os.path.join(output_path, "simulation_results.csv"))
        os.rename(self.simulation_events_path, os.path.join(output_path, "input_config.json"))