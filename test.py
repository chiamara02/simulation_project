from FMUWrapper import FMUWrapper
from controllers import PIDController

fmu_path = 'fmu_models/RoomHeater.fmu'

exposed_params = []

# Initialize the wrapper
fmu_sim = FMUWrapper(path=fmu_path, stop_time=10000, step_size=0.01, parameters=exposed_params)

# Set up and initialize the FMU
fmu_sim.initialize_fmu()

# Print input variables
fmu_sim.print_input_variables()

# Define the fault conditions or and the input variables
input_vars = [
     
    {
        'variable': 'outsideTemp',
        'values': [
            {'value': 10.0, 'start_time': 0, 'end_time': 1401},
            {'value': 9.0, 'start_time': 1401, 'end_time': 10000},
           
        ],
        'default': 2
    },
    
]


# Controller
pid = PIDController(measurement_var="temperatureSensor.T", control_var="heatSourcePower",
                    Kp=500, Ki=0.2, Kd=2, setpoint=23.0, max_output=2000.0)



# Define the variables to plot
plot_vars = ['temperatureSensor.T']

# Run hybrid simulation
times, data = fmu_sim.simulate_with_controller(
    input_vars=input_vars,
    controllers=[pid],
    plot_vars=plot_vars
)

# Plot the results
fmu_sim.plot_results(times, data)
