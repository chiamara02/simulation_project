import numpy as np
from scenarios.room_heater.utils.temp import *
from scenarios.room_heater.utils.fuzzy_config import fuzzy_config



def generate_inputs(duration, step_size, seed=0):
    """
    Generate input variables for the room heater scenario.
    """
    
    np.random.seed(seed)    # ensures reproducibility
    input_vars = []

    # outsideTemp 
    day = np.random.randint(1, 28)
    month = np.random.choice([1,2,3,4,10,11,12])  # only winter months
    start_time = np.random.randint(0, 20)
    end_time = (start_time + 4) % 24  # ensures end_time is within the same day
    freq = 10  # frequency in minutes
    temperatures = simulate_temperature(day, month, start_time, end_time)
    final_temperatures = interpolate_temperatures(temperatures, freq = freq)
    
    values = []
    rows = list(final_temperatures.itertuples())  # convert to list so we can look ahead
    for i, row in enumerate(rows):
        start_time = start_time + freq * 60 if i > 0 else 0  # start_time is cumulative
        end_time = start_time + freq * 60  
        values.append({
            "value": row.temp,
            "start_time": start_time,
            "end_time": end_time
        })

    input_vars = [{
        "variable": "outsideTemp",
        "values": values,
        "default": 20.0
    }]
    
    # sensorNoiseMu and Sigma: random constant noise
    input_vars.append({
        "variable": "sensorNoiseMu",
        "values": [],
        "default": np.random.uniform(-0.0, 0.0)
    })
    input_vars.append({
        "variable": "sensorNoiseSigma",
        "values": [],
        "default": 0.2
        
    })


    # windowState: randomly open (0), partially open (1) or closed (2) for periods
    values = []
    t = 0
    current_state = 2   # start closed

    while t < duration:
        # Sample next transition time
        next_t = t + step_size * int(np.random.exponential(7200))
        next_state = 2 #simulate_window_markov(current_state)

        values.append({
            "value": current_state,
            "start_time": t,
            "end_time": min(next_t, duration)
        })

        # Move forward
        t = next_t
        current_state = next_state

    input_vars.append({
        "variable": "windowState",
        "values": values,
        "default": 2
    })

    return input_vars

def simulate_window_markov(current_state):

    states = [0, 1, 2]  # 0=open, 1=vasistas, 2=closed
    
    transition_rules = {
        2: [0, 1],  # from closed → can go to open or vasistas
        0: [2],     # from open → must go to closed
        1: [2]      # from vasistas → must go to closed
    }
    possible_next = transition_rules[current_state]
    next_state = int(np.random.choice(possible_next))
    return next_state

def setup_controller(controller_type):
    """
    Setup the controller based on the type.
    """
    if controller_type == "pid":
        from controllers.pid_controller import PIDController
        return PIDController(control_input="measuredTemp", control_output="heatSourcePower",
                             Kp=500, Ki=0.02, Kd=0, setpoint=20.0, max_output=2000.0)
    elif controller_type == "onoff":
        from controllers.onoff_controller import OnOffController
        return OnOffController(control_input="measuredTemp", control_output="heatSourcePower",
                               setpoint=20.0, threshold=0.1,
                               on_value=1500.0, off_value=0.0)
    elif controller_type == "fuzzy":
        from controllers.fuzzy_controller import FuzzyLogicController
        return FuzzyLogicController(config=fuzzy_config, target_var= "measuredTemp", inputs = ["error","outsideTemp","roomAir.der_T"], setpoint=20.0)
    else:
        raise ValueError(f"Unsupported controller type: {controller_type}")
    

def get_fmu_path():
    """
    Returns the path to the FMU model.
    """
    return "simulator/scenarios/room_heater/fmu/RoomHeater.fmu"