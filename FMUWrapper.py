from typing import Set, List, Dict
import fmpy
import pandas as pd
from fmpy.fmi2 import FMU2Slave
import matplotlib.pyplot as plt


class FMUWrapper:
    """
    A wrapper class for working with FMUs using the FMpy library.

    This class simplifies the interaction with FMUs, including initialization, setting and getting variable values, 
    running simulations, and plotting results.

    Attributes:
        path (str): The file path to the FMU.
        stop_time (float): The simulation end time. Default is 1000.
        step_size (float): The simulation step size. Default is 0.02.
        model_description: The model description of the FMU, obtained from the FMU file.
        variables (dict): A dictionary containing model variable metadata like type, causality, and value reference.
    """

    def __init__(self, path: str, stop_time: float = 1000, step_size: float = 0.02, parameters: List[Dict] = []):
        """
        Initialize the FMUWrapper object and read the FMU model description.

        Args:
            path (str): The path to the FMU file.
            stop_time (float): The simulation stop time. Default is 1000.
            step_size (float): The step size for simulation. Default is 0.02.
        """

        self.model_description = fmpy.read_model_description(path)
        self.start_time = self.model_description.defaultExperiment.startTime
        self.stop_time = stop_time
        self.step_size = step_size
        self.path = path
        self.variables = {
            var.name: {'type': var.type, 'causality': var.causality,
                       'valueReference': var.valueReference, 'variability': var.variability}
            for var in self.model_description.modelVariables
        }
        self.parameters = parameters




    def initialize_fmu(self):
        """
        Initialize the FMU by extracting, instantiating, and entering initialization mode.
        
        This prepares the FMU for simulation by performing necessary setup steps.
        """

        self.fmu = FMU2Slave(guid=self.model_description.guid,
                             unzipDirectory=fmpy.extract(self.path),
                             modelIdentifier=self.model_description.coSimulation.modelIdentifier,
                             instanceName='instance1')

        self.fmu.instantiate()
        self.fmu.setupExperiment(startTime=self.start_time)
        self.fmu.enterInitializationMode()
        self.__set_parameters(self.parameters)
        self.fmu.exitInitializationMode()
        



    def __set_variable(self, var_name: str, var_value, var_causality: str):
        """
        Set the value of a variable in the FMU.

        Args:
            var_name (str): The name of the variable to set.
            var_value: The value to assign to the variable. Type depends on the variable's declared type.

        Raises:
            NameError: If the variable is not found or cannot be modified or if the type of causality(e.g. 'input', 'const) 
            does not support modifications.
            ValueError: If the variable type does not match the provided value type.
        """
        if var_causality != 'input' and var_causality != 'parameter':
            raise NameError(
                f"Type '{var_causality}' not modifiable")
        variable = self.variables.get(var_name)

        if variable is None:
            raise NameError(
                f"Variable '{var_name}' not found in the model description")

        if variable['causality'] != var_causality:
            raise NameError(
                f"Variable '{var_name}' cannot be modified because it is not an input variable nor a parameter")

        var_type = variable['type']
        var_ref = variable['valueReference']

        # Check that variable type and input value type are compatible
        if var_type == 'Boolean' and isinstance(var_value, bool):
            self.fmu.setBoolean([var_ref], [var_value])
        elif var_type == 'Real' and isinstance(var_value, float):
            self.fmu.setReal([var_ref], [var_value])
        elif var_type == 'Integer' and isinstance(var_value, int):
            self.fmu.setInteger([var_ref], [var_value])
        else:
            raise ValueError(f"Unsupported variable type for variable '{var_name}'. \
                             The correct data type for this variable is '{var_type}'")
        


    def __get_variable(self, var_name: str):
        """
        Get the value of a variable from the FMU. 

        Args:
            var_name (str): The name of the variable to retrieve.

        Returns:
            The value of the variable, type depends on the variable's declared type.

        Raises:
            NameError: If the variable is not found in the model description.
            ValueError: If the variable's type is unsupported.
        """

        variable = self.variables.get(var_name)

        if variable is None:
            raise NameError(
                f"Variable '{var_name}' not found in the model description")

        var_type = variable['type']
        var_ref = variable['valueReference']

        # Retrieve variable value based on its type
        if var_type == 'Real':
            return self.fmu.getReal([var_ref])[0]
        elif var_type == 'Boolean':
            return self.fmu.getBoolean([var_ref])[0]
        elif var_type == 'Integer':
            return self.fmu.getInteger([var_ref])[0]
        else:
            raise ValueError(f"Unsupported variable type for variable '{var_name}'. \
                             The data type for this variable is '{var_type}'")

    def __set_parameters(self, parameters: List[Dict]):

        """
        This method iterates over a list of parameters and sets each parameter's value in the FMU model.
        Each parameter is defined as a dictionary containing the 'name' and 'value' keys. The method
        internally calls `__set_variable` for each parameter to update the FMU's state.

        Args:
            parameters (List[Dict]): 
                A list of dictionaries where each dictionary represents a parameter to set. 
                Each dictionary should have the following keys:
                    - 'name' (str): The name of the parameter to set.
                    - 'value' (Any): The value to assign to the parameter.

        """

        for parameter in parameters:
            par_name = parameter['name']
            par_value = parameter['value']
            self.__set_variable(par_name, par_value, 'parameter') 
                


    def simulate(self, input_vars: List[Dict] = None, plot_vars: List[str] = None): 
        """
        Run the FMU simulation, setting input variables and recording data for plotting.

        Args:
            input_vars (List[Dict]): A list of input variables with their values and time intervals.
                                     Default is an empty list.
            plot_vars (List[str]): A list of variable names to track for plotting. Default is an empty list.

        Returns:
            times (List[float]): A list of time points for the simulation.
            plot_data (Dict[str, List[float]]): A dictionary containing the tracked variable values 
                                                over time for each variable specified in plot_vars.
        """

        if plot_vars is None:
            plot_vars = []

        if input_vars is None:
            input_vars = []

        time = self.start_time
        times = []
        plot_data = {var: [] for var in plot_vars}

        initialized_variables = set()
        for input_var in input_vars:
            var = Input(input_var)
            # Check if the variable was already defined
            if var in initialized_variables:
                raise NameError(
                    f"Variable '{var.var_name}' already has a value")
            else:
                initialized_variables.add(var)

        # Simulation loop
        while time <= self.stop_time:
            # Set values for the input variables
            if initialized_variables:
                for input_var in initialized_variables:
                    var_value = input_var.get_value(time)
                    self.__set_variable(input_var.var_name, var_value, 'input')

            # Store current time and variable values
            times.append(time)
            for var in plot_vars:
                plot_data[var].append(self.__get_variable(var))

            # Perform simulation step
            self.fmu.doStep(currentCommunicationPoint=time,
                            communicationStepSize=self.step_size)
            time += self.step_size

            
        initialized_variables.clear()
        # Terminate simulation
        self.fmu.terminate()
        self.fmu.freeInstance()

        return times, plot_data
    

    def simulate_with_controller(self, input_vars=None, controller=None, plot_vars=None):
        if input_vars is None:
            input_vars = []

        if plot_vars is None:
            plot_vars = []

        time = self.start_time
        times = []
        plot_data = {var: [] for var in plot_vars}

        # Prepare static inputs
        initialized_inputs = set()
        input_objects = []
        for input_var in input_vars:
            var = Input(input_var)
            input_objects.append(var)
            if var in initialized_inputs:
                raise NameError(f"Duplicate input: {var.var_name}")
            initialized_inputs.add(var)

        while time <= self.stop_time:
            # Apply static inputs
            for input_var in input_objects:
                value = input_var.get_value(time)
                self.__set_variable(input_var.var_name, value, 'input')

            # Gather FMU outputs needed for controller
            fmu_outputs = {var: self.__get_variable(var) for var in plot_vars}

            # Run controllers and set controller-driven inputs
            if controller is not None:
                control_updates = controller.update(fmu_outputs, self.step_size)
                for var_name, value in control_updates.items():
                    self.__set_variable(var_name, value, 'input')

            # Record data
            times.append(time)
            for var in plot_vars:
                plot_data[var].append(self.__get_variable(var))

            # Step the FMU
            self.fmu.doStep(currentCommunicationPoint=time, communicationStepSize=self.step_size)
            time += self.step_size

        self.fmu.terminate()
        self.fmu.freeInstance()

        return times, plot_data

    


    def plot_results(self, times: List[float], plot_data: Dict[str, List[float]]):
        """
        Plot the results of the simulation.

        Args:
            times (List[float]): A list of time points from the simulation.
            plot_data (Dict[str, List[float]]): A dictionary of variable values over time to plot.
        """
        df = pd.DataFrame(plot_data, index=times)
        df.to_csv('simulations/simulation_results.csv', index_label='Time')
        plt.figure()
        for var, values in plot_data.items():
            plt.plot(times, values, label=var)
        plt.xlabel('Time (s)')
        plt.ylabel('Values')
        plt.legend()
        plt.show()



    def print_input_variables(self):
        """
        Print the input variables of the FMU model.

        This method extracts and prints all variables from the FMU model
        description that have the 'input' causality. For each input variable, 
        it displays the name and type

        The output format is:
        - Name: the name of the variable.
        - Type: the data type of the variable (e.g., Real, Integer, etc.).
        
        """

        print("\nInput Variables in the FMU:")
        for variable in self.model_description.modelVariables:
            if(variable.causality == 'input'):
                print(f"Name: {variable.name}, Type: {variable.type}")  
        print("\n")




class Input:
    """
    Class to represent an input variable with time-dependent values and perform operations 
    like checking for overlapping time ranges in the value definition and retrieving values based on the current time step.
    
    Attributes:
        var (dict): The input dictionary containing the variable's details.
        var_name (str): The name of the variable.
        values (list): A list of dictionaries each containing 'value', 'start_time', and 'end_time'
        default: The default value to be returned if no time range matches a given time.
    """
     
    def __init__(self, input_var: Dict):
        """
        Initializes the Input object with the provided variable details and checks for 
        overlapping time ranges.

        Args:
            input_var (dict): A dictionary containing the variable name, a list of time ranges, 
                              and a default value.
        """

        self.var = input_var
        self.var_name = self.var['variable']
        self.values = self.var['values']
        self.default = self.var['default']
        self.check_overlap()


    def check_overlap(self):
        """
        Checks for overlapping time ranges in the variable's values. Raises a ValueError if 
        any two consecutive time ranges overlap (i.e., if the 'end_time' of one range is 
        greater than the 'start_time' of the next range).
        
        Raises:
            ValueError: If invalid or overlapping time ranges are found.
        """
        # Check if time ranges are valid
        for value in self.values:
            if value['end_time'] < value['start_time']:
                raise ValueError(f"Invalid time range: 'end_time' is less than 'start_time' \
                         for variable '{self.var_name}' in range {value}")
            
        time_ranges = sorted(self.values, key=lambda x: x['start_time'])

        #Check for overlaps
        for i in range(len(time_ranges) - 1):
            current_range = time_ranges[i]
            next_range = time_ranges[i + 1]
            
            # Check if the current range overlaps with the next range
            if current_range['end_time'] > next_range['start_time']:
                raise ValueError(f"Overlap found in variable '{self.var_name}' \
                                 between {current_range} and {next_range}")


    def get_value(self, time: float):
        """
        Retrieves the value of the variable corresponding to the given time.
        If the time falls within a specific time range, the associated value is returned.
        If no time range matches, the default value is returned.

        Args:
            time (float): The time for which the variable's value is to be retrieved.

        Returns:
            The value associated with the time range that includes the given time.
            If no time range matches, returns the default value.
        """

        # Check if time falls within any of the time ranges
        for value in self.values:
            if value['start_time'] <= time < value['end_time']:
                return value['value']
        # Return default if no range matches the time
        return self.default



