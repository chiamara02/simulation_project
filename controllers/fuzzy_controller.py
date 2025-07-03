from controllers.base_controller import BaseController
import numpy as np

class FuzzyLogicController(BaseController):
    def __init__(self, config: dict, target_var, inputs: list, setpoint: float):
        self.config = config
        self.target_var = target_var  # The variable to control (e.g. "temperatureSensor.T")
        self.setpoint = setpoint
        self.inputs = inputs  # list of variable names (e.g. ["error", "outdoorTemperature", "temperatureDerivative"])
        self.output_name = list(config["output"].keys())[0]

        # Extract input membership functions
       
        self.input_mfs = {
            var_name: config["inputs"][var_name]["membership_functions"]
            for var_name in self.inputs
            if var_name != target_var and var_name in config["inputs"]
        }
        if "error" in config["inputs"]:
            self.input_mfs["error"] = config["inputs"]["error"]["membership_functions"]
            

        # Output membership functions and range
        self.output_mfs = config["output"][self.output_name]["membership_functions"]
        self.output_range = config["output"][self.output_name]["range"]
        self.rules = config["rules"]

    def membership_degree(self, x, points):
        """Triangular or trapezoidal membership."""
        points = sorted(points)
        if len(points) == 3:
            a, b, c = points
            if a == b or b == c:
                return 0.0 
            if a <= x <= b:
                return (x - a) / (b - a)
            elif b < x <= c:
                return (c - x) / (c - b)
            else:
                return 0.0
        elif len(points) == 4:
            a, b, c, d = points
            if b == a or c == d:
                return 0.0
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

    def fuzzify(self, value, mfs):
        return {
            label: self.membership_degree(value, points)
            for label, points in mfs.items()
        }

    def defuzzify(self, output_degrees):
        resolution = 100
        output_values = np.linspace(*self.output_range, resolution)
        aggregated = np.zeros_like(output_values)

        for label, degree in output_degrees.items():
            mf_points = self.output_mfs[label]
            mf_values = np.array([self.membership_degree(v, mf_points) for v in output_values])
           # print(f"  MF '{label}': max degree {degree}, MF values: {mf_values}")

            aggregated = np.maximum(aggregated, np.minimum(degree, mf_values))
            #print(f"Aggregated for label '{label}': {aggregated}")
        total = np.sum(aggregated)
        return np.sum(output_values * aggregated) / total if total != 0 else 0

    def update(self, model_variables, step_size):
        # Build current input values, computing error from setpoint
        input_values = {}
        for var in self.inputs:
            if var == "error":
                input_values["error"] = self.setpoint - model_variables[self.target_var]
                #print(f"Calculated error: {input_values['error']} (setpoint: {self.setpoint}, target: {model_variables[self.target_var]})")
            else:
                input_values[var] = model_variables[var]

        # Fuzzify all input values
        fuzzified_inputs = {
            var: self.fuzzify(value, self.input_mfs[var])
            for var, value in input_values.items()
        }

        #print("Fuzzified inputs:")
        #for var, degrees in fuzzified_inputs.items():
        #    print(f"  {var}: {degrees}")


        # Apply rules
        output_activation = {}
        for rule in self.rules:
            rule_if = rule["if"]
            rule_then = rule["then"]
            rule_strengths = []

            for var in rule_if:
                label = rule_if[var]
                rule_strengths.append(fuzzified_inputs[var].get(label, 0))

            # Take the minimum strength across all conditions (AND logic)
            rule_strength = min(rule_strengths)
            #print(f"Rule triggered: {rule_if} → {rule_then}, strength: {rule_strength}")
            output_label = list(rule_then.values())[0]
            output_activation[output_label] = max(output_activation.get(output_label, 0), rule_strength)
        
        #print("Output activation:", output_activation)


        output_value = self.defuzzify(output_activation)
        return {self.output_name: float(output_value)}
