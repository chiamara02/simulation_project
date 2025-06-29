from controllers.base_controller import BaseController

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
        print(f"PIDController: measurement={measurement}, setpoint={self.setpoint}, step_size={step_size}")
        error = self.setpoint - measurement
        self.integral += error * step_size
        derivative = (error - self.prev_error) / step_size
        output = self.Kp * error + self.Ki * self.integral + self.Kd * derivative
        if output > self.max_output:  
            output = self.max_output
        self.prev_error = error

        return {self.control_output: output}