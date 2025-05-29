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
    


 
