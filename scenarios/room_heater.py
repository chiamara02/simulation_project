import random

def generate_inputs(duration, step_size, seed=0):
    random.seed(seed)  # ensures reproducibility

    input_vars = []

    # outsideTemp fluctuates
    values = []
    t = 0
    while t < duration:
        next_t = t + step_size * random.randint(10, 50)
        values.append({
            "value": random.uniform(5, 25),
            "start_time": t,
            "end_time": min(next_t, duration)
        })
        t = next_t
    input_vars.append({
        "variable": "outsideTemp",
        "values": values,
        "default": 10.0
    })

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
            "value": random.choice([1, 2]),
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