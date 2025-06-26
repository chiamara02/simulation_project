import numpy as np
class BaseController:
    def update(self, control_inputs: dict[str, float], time: float, step_size: float) -> dict[str, float]:
        pass


class PIDController(BaseController):
    def __init__(self, control_input, control_output, Kp, Ki, Kd, setpoint, max_output):
        self.control_input = control_input
        self.control_output = control_output
        self.Kp = Kp
        self.Ki = Ki
        self.Kd = Kd
        self.setpoint = setpoint
        self.integral = 0
        self.prev_error = 0
        self.max_output = max_output
        if max_output <= 0:
            raise ValueError("max_output must be a positive value")

    def update(self, model_variables, step_size):
        measurement = model_variables[self.control_input]
        error = self.setpoint - measurement
        self.integral += error * step_size
        derivative = (error - self.prev_error) / step_size
        output = self.Kp * error + self.Ki * self.integral + self.Kd * derivative
        if output > self.max_output:  
            output = self.max_output
        self.prev_error = error

        return {self.control_output: output}

class OnOffController(BaseController):
    def __init__(self, control_input, control_output, setpoint, threshold, on_value=1.0, off_value=0.0):
        self.control_input = control_input
        self.control_output = control_output
        self.setpoint = setpoint
        self.threshold = threshold
        self.on_value = on_value
        self.off_value = off_value

    def update(self, model_variables, step_size):
        if self.control_input not in model_variables:
            raise ValueError(f"Control input variable '{self.control_input}' not found in model variables.")
        measurement =model_variables[self.control_input]
        if measurement < self.setpoint - self.threshold:
            output = self.on_value  # Turn on
        elif measurement > self.setpoint + self.threshold:
            output = self.off_value  # Turn off
        else:
            output = self.off_value  # No change

        return {self.control_output: output} if output is not None else {}
    

class FuzzyLogicController(BaseController):
    def __init__(self, config: dict, input: float,  setpoint: float):
        self.config = config
        self.setpoint = setpoint
        self.input = input
        self.control_input = list(config["inputs"].keys())[0]  # assuming one input variable: "error"
        self.control_output = list(config["output"].keys())[0]
        self.input_mfs = config["inputs"][self.control_input]["membership_functions"]
        self.output_mfs = config["output"][self.control_output]["membership_functions"]
        self.output_range = config["output"][self.control_output]["range"]
        self.rules = config["rules"]

    def membership_degree(self, x, points):
        """Triangular or trapezoidal membership."""
        points = sorted(points)
        if len(points) == 3:  # Triangular
            a, b, c = points
            if a <= x <= b:
                return (x - a) / (b - a)
            elif b < x <= c:
                return (c - x) / (c - b)
            else:
                return 0.0
        elif len(points) == 4:  # Trapezoidal
            a, b, c, d = points
            if a <= x < b:
                return (x - a) / (b - a)
            elif b <= x <= c:
                return 1.0
            elif c < x <= d:
                return (d - x) / (d - c)
            else:
                return 0.0
        else:
            raise ValueError("Invalid membership function definition.")

    def fuzzify(self, x, mfs):
        return {label: self.membership_degree(x, points) for label, points in mfs.items()}

    def defuzzify(self, output_degrees):
        resolution = 100
        output_values = np.linspace(*self.output_range, resolution)
        aggregated = np.zeros_like(output_values)

        for label, degree in output_degrees.items():
            mf_points = self.output_mfs[label]
            mf_values = np.array([self.membership_degree(v, mf_points) for v in output_values])
            aggregated = np.maximum(aggregated, np.minimum(degree, mf_values))

        return np.sum(output_values * aggregated) / np.sum(aggregated) if np.sum(aggregated) != 0 else 0

    def update(self, model_variables, step_size):
        feedback = model_variables[self.input]
        error = self.setpoint - feedback
        fuzzified_input = self.fuzzify(error, self.input_mfs)

        # Apply rules
        output_activation = {}
        for rule in self.rules:
            input_label = rule["if"][self.control_input]
            output_label = rule["then"][self.control_output]
            degree = fuzzified_input.get(input_label, 0)
            output_activation[output_label] = max(output_activation.get(output_label, 0), degree)

        output_value = self.defuzzify(output_activation)
        return {self.control_output: float(output_value)}
 
