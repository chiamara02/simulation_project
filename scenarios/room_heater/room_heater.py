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
    month = np.random.randint(1, 12)
    start_time = np.random.randint(0, 20)
    end_time = (start_time + 4) % 24  # ensures end_time is within the same day
    freq = 10  # frequency in minutes
    temperatures = simulate_temperature(day, month, start_time, end_time, seed=seed)
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
        "default": 10.0
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
        "default": np.random.uniform(0.0, 0.0)
    })

    # windowState: randomly open (0), partially open (1) or closed (2) for periods
    values = []
    t = 0
    while t < duration:
        next_t = t + step_size * int(np.random.exponential(1800)) # on average twice per hour
        values.append({
            "value": np.random.choice(3),  # 0: open, 1: closed, 2: locked
            "start_time": t,
            "end_time": min(next_t, duration)
        })
        t = next_t
    input_vars.append({
        "variable": "windowState",
        "values": values,
        "default": 2
    })

    return input_vars


def setup_controller(controller_type):
    """
    Setup the controller based on the type.
    """
    if controller_type == "pid":
        from controllers.pid_controller import PIDController
        return PIDController(control_input="temperatureSensor.T", control_output="heatSourcePower",
                             Kp=500, Ki=0.2, Kd=0, setpoint=16.0, max_output=2000.0)
    elif controller_type == "onoff":
        from controllers.onoff_controller import OnOffController
        return OnOffController(control_input="temperatureSensor.T", control_output="heatSourcePower",
                               setpoint=16.0, threshold=0.1,
                               on_value=1500.0, off_value=0.0)
    elif controller_type == "fuzzy":
        from controllers.fuzzy_controller import FuzzyLogicController
        return FuzzyLogicController(config=fuzzy_config, target_var= "temperatureSensor.T", inputs = ["error","outsideTemp","roomAir.der_T"], setpoint=16.0)
    else:
        raise ValueError(f"Unsupported controller type: {controller_type}")
    

def get_fmu_path():
    """
    Returns the path to the FMU model.
    """
    return "scenarios/room_heater/fmu/RoomHeater.fmu"