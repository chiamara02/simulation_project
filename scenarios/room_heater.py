import random
from scenarios.temp import *

def generate_inputs(duration, step_size, seed=0):
    random.seed(seed)  # ensures reproducibility

    input_vars = []

    # outsideTemp fluctuates
    day = random.randint(1, 28)
    month = random.randint(1, 12)
    start_time = random.randint(0, 24)
    end_time = (start_time + 4) % 24  # ensures end_time is within the same day
    temperatures = simulate_temperature(day, month, start_time, end_time, seed=seed)
    final_temperatures = random_walk_interpolate(temperatures)
    
    values = []
    rows = list(final_temperatures.itertuples())  # convert to list so we can look ahead

    for i, row in enumerate(rows):
        start_time = row.Index
        end_time = rows[i + 1].Index if i + 1 < len(rows) else row.Index  # end_time is next row's index
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
        "default": random.uniform(-0.5, 0.5)
    })
    input_vars.append({
        "variable": "sensorNoiseSigma",
        "values": [],
        "default": random.uniform(0.0, 0.3)
    })

    # windowState: randomly open (1) or closed (2) for periods
    values = []
    t = 0
    while t < duration:
        next_t = t + step_size * random.randint(50, 150)
        values.append({
            "value": random.choice([0, 1, 2]),  # 0: open, 1: closed, 2: locked
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
        from controllers import PIDController
        return PIDController(control_input="temperatureSensor.T", control_output="heatSourcePower",
                             Kp=500, Ki=0.2, Kd=2, setpoint=23.0, max_output=2000.0)
    elif controller_type == "onoff":
        from controllers import OnOffController
        return OnOffController(control_input="temperatureSensor.T", control_output="heatSourcePower",
                               setpoint=23.0, threshold=0.1,
                               on_value=1500.0, off_value=0.0)
    else:
        raise ValueError(f"Unsupported controller type: {controller_type}")
    

def get_fmu_path():
    """
    Returns the path to the FMU model.
    """
    return "fmu_models/RoomHeater.fmu"