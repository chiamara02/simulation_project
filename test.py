from FMUWrapper import FMUWrapper
from controllers import *

fmu_path = 'fmu_models/RoomHeater.fmu'

exposed_params = []

# Initialize the wrapper
fmu_sim = FMUWrapper(path=fmu_path, stop_time=1000, step_size=1, parameters=exposed_params)

# Set up and initialize the FMU
fmu_sim.initialize_fmu()

# Print input variables
fmu_sim.print_input_variables()

# Define the fault conditions or and the input variables
input_vars = [
     
        {
        'variable': 'outsideTemp',
        'values': [
          
        ],
        'default': 10.0
    },
      {
        'variable': 'sensorNoiseMu',
        'values': [
          
        ],
        'default': 0.0
    },
      {
        'variable': 'sensorNoiseSigma',
        'values': [
          
        ],
        'default': 0.0
    },
      {
        'variable': 'windowState',
        'values': [
          
        ],
        'default': 2
    },
     
    
]


# Controller
pid = PIDController(measurement_var="temperatureSensor.T", control_var="heatSourcePower",
                    Kp=500, Ki=0.2, Kd=2, setpoint=23.0, max_output=2000.0)

onOff = OnOffController(measurement_var="temperatureSensor.T", control_var="heatSourcePower",
                       setpoint=23.0, threshold=0.1
                    , on_value=1500.0, off_value=0.0)

# Define the variables to plot
plot_vars = ['temperatureSensor.T' ,'heatSourcePower']

# Run hybrid simulation
times, data = fmu_sim.simulate_with_controller(
    input_vars=input_vars,
    controller=onOff,
    plot_vars=plot_vars
)

# Plot the results
fmu_sim.plot_results(times, data)
