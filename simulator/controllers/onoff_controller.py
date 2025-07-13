from controllers.base_controller import BaseController


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