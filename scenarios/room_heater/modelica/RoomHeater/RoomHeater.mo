within RoomHeater;
model RoomHeater
  Modelica.Thermal.HeatTransfer.Components.HeatCapacitor roomAir(C = 1e6, T(start = 291.15))  annotation(
    Placement(transformation(origin = {38, 20}, extent = {{-10, -10}, {10, 10}})));
  Modelica.Thermal.HeatTransfer.Components.ThermalConductor wall(G = 6)  annotation(
    Placement(transformation(origin = {-12, 10}, extent = {{-10, -10}, {10, 10}})));
  Modelica.Thermal.HeatTransfer.Sources.PrescribedHeatFlow heater annotation(
    Placement(transformation(origin = {2, -30}, extent = {{-10, -10}, {10, 10}})));
  Modelica.Thermal.HeatTransfer.Celsius.TemperatureSensor temperatureSensor annotation(
    Placement(transformation(origin = {68, 58}, extent = {{-10, -10}, {10, 10}})));
  Modelica.Thermal.HeatTransfer.Celsius.PrescribedTemperature outsideTemperature annotation(
    Placement(transformation(origin = {-56, 10}, extent = {{-10, -10}, {10, 10}})));
  Modelica.Blocks.Interfaces.RealInput outsideTemp annotation(
    Placement(transformation(origin = {-112, 10}, extent = {{-12, -12}, {12, 12}}), iconTransformation(origin = {-120, 48}, extent = {{-20, -20}, {20, 20}})));
  Modelica.Blocks.Interfaces.RealInput heatSourcePower annotation(
    Placement(transformation(origin = {-112, -30}, extent = {{-12, -12}, {12, 12}}), iconTransformation(origin = {-120, -52}, extent = {{-20, -20}, {20, 20}})));
  Modelica.Blocks.Interfaces.RealOutput measuredTemp annotation(
    Placement(transformation(origin = {110, 0}, extent = {{-10, -10}, {10, 10}}), iconTransformation(origin = {121, 1}, extent = {{-21, -21}, {21, 21}})));
  SubModules.Window window annotation(
    Placement(transformation(origin = {-12, 54}, extent = {{-10, -10}, {10, 10}})));
  SubModules.NoiseGenerator normalNoise(samplePeriod = 1)  annotation(
    Placement(transformation(origin = {-18, -76}, extent = {{-10, -10}, {10, 10}})));
  Modelica.Blocks.Interfaces.RealInput sensorNoiseMu annotation(
    Placement(transformation(origin = {-59, -111}, extent = {{-11, -11}, {11, 11}}, rotation = 90), iconTransformation(origin = {0, -120}, extent = {{-20, -20}, {20, 20}}, rotation = 90)));
  Modelica.Blocks.Interfaces.RealInput sensorNoiseSigma annotation(
    Placement(transformation(origin = {-41, -111}, extent = {{-11, -11}, {11, 11}}, rotation = 90), iconTransformation(origin = {60, -120}, extent = {{-20, -20}, {20, 20}}, rotation = 90)));
  Modelica.Blocks.Interfaces.IntegerInput windowState annotation(
    Placement(transformation(origin = {-12, 112}, extent = {{-12, -12}, {12, 12}}, rotation = -90), iconTransformation(origin = {0, 118}, extent = {{-20, -20}, {20, 20}}, rotation = -90)));
  Modelica.Blocks.Math.MultiSum multiSum(nu = 2)  annotation(
    Placement(transformation(origin = {77, 0}, extent = {{-7, -7}, {7, 7}}, rotation = -0)));
equation
  connect(heater.port, roomAir.port) annotation(
    Line(points = {{12, -30}, {38, -30}, {38, 10}}, color = {191, 0, 0}));
  connect(wall.port_b, roomAir.port) annotation(
    Line(points = {{-2, 10}, {38, 10}}, color = {191, 0, 0}));
  connect(roomAir.port, temperatureSensor.port) annotation(
    Line(points = {{38, 10}, {58, 10}, {58, 58}}, color = {191, 0, 0}));
  connect(outsideTemperature.port, wall.port_a) annotation(
    Line(points = {{-46, 10}, {-22, 10}}, color = {191, 0, 0}));
  connect(heatSourcePower, heater.Q_flow) annotation(
    Line(points = {{-112, -30}, {-8, -30}}, color = {0, 0, 127}));
  connect(outsideTemp, outsideTemperature.T) annotation(
    Line(points = {{-112, 10}, {-68, 10}}, color = {0, 0, 127}));
  connect(window.port_b, roomAir.port) annotation(
    Line(points = {{-2, 54}, {12, 54}, {12, 10}, {38, 10}}, color = {191, 0, 0}));
  connect(outsideTemperature.port, window.port_a) annotation(
    Line(points = {{-46, 10}, {-32, 10}, {-32, 54}, {-22, 54}}, color = {191, 0, 0}));
  connect(sensorNoiseMu, normalNoise.mu) annotation(
    Line(points = {{-59, -111}, {-59, -72}, {-30, -72}}, color = {0, 0, 127}));
  connect(sensorNoiseSigma, normalNoise.sigma) annotation(
    Line(points = {{-41, -111}, {-41, -80}, {-30, -80}}, color = {0, 0, 127}));
  connect(windowState, window.window_state) annotation(
    Line(points = {{-12, 112}, {-12, 68}}, color = {255, 127, 0}));
  connect(multiSum.y, measuredTemp) annotation(
    Line(points = {{86, 0}, {110, 0}}, color = {0, 0, 127}));
  connect(temperatureSensor.T, multiSum.u[1]) annotation(
    Line(points = {{78, 58}, {86, 58}, {86, 20}, {64, 20}, {64, 0}, {70, 0}}, color = {0, 0, 127}));
  connect(normalNoise.y, multiSum.u[2]) annotation(
    Line(points = {{-6, -76}, {60, -76}, {60, 0}, {70, 0}}, color = {0, 0, 127}));
  annotation(
    uses(Modelica(version = "4.0.0")));
end RoomHeater;