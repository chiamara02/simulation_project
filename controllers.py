class BaseController:
    def update(self, fmu_outputs: dict[str, float], time: float, step_size: float) -> dict[str, float]:
        pass


class PIDController(BaseController):
    def __init__(self, measurement_var, control_var, Kp, Ki, Kd, setpoint, max_output):
        self.measurement_var = measurement_var
        self.control_var = control_var
        self.Kp = Kp
        self.Ki = Ki
        self.Kd = Kd
        self.setpoint = setpoint
        self.integral = 0
        self.prev_error = 0
        self.max_output = max_output
        if max_output <= 0:
            raise ValueError("max_output must be a positive value")

    def update(self, fmu_outputs, time, step_size):
        measurement = fmu_outputs[self.measurement_var]
        error = self.setpoint - measurement
        self.integral += error * step_size
        derivative = (error - self.prev_error) / step_size
        output = self.Kp * error + self.Ki * self.integral + self.Kd * derivative
        if output > self.max_output:  
            output = self.max_output
        self.prev_error = error

        return {self.control_var: output}
