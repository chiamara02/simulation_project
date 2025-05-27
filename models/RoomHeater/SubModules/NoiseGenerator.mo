within RoomHeater.SubModules;
block NoiseGenerator "Normal noise generator with input ports for mu and sigma"
  import distribution = Modelica.Math.Distributions.Normal.quantile;
  extends Modelica.Blocks.Interfaces.PartialNoise;
  // Input ports for mean and standard deviation
  //Modelica.Blocks.Interfaces.RealInput mu "Mean of normal distribution";
  //Modelica.Blocks.Interfaces.RealInput sigma "Standard deviation of normal distribution";
  Modelica.Blocks.Interfaces.RealInput mu annotation(
    Placement(transformation(origin = {-111, 19}, extent = {{-11, -11}, {11, 11}}), iconTransformation(origin = {-120, 40}, extent = {{-20, -20}, {20, 20}})));
  Modelica.Blocks.Interfaces.RealInput sigma annotation(
    Placement(transformation(origin = {-111, -19}, extent = {{-11, -11}, {11, 11}}), iconTransformation(origin = {-120, -40}, extent = {{-20, -20}, {20, 20}})));
initial equation
  r = distribution(r_raw, mu, sigma);

equation
  // Draw random number at sample times
  when generateNoise and sample(startTime, samplePeriod) then
    r = distribution(r_raw, mu, sigma);
  end when;

  annotation(
    Icon(coordinateSystem(preserveAspectRatio = false, extent = {{-100, -100}, {100, 100}}), graphics = {Text(visible = enableNoise, extent = {{-66, 92}, {94, 66}}, textColor = {175, 175, 175}, textString = "mu=input"), Text(visible = enableNoise, extent = {{-70, -68}, {94, -96}}, textColor = {175, 175, 175}, textString = "sigma=input")}),
    Documentation(info = "<html>
<p>
This block generates reproducible random noise at its output according to a normal distribution,
with expectation value and standard deviation provided as input signals (mu and sigma).
See <a href=\"modelica://Modelica.Blocks.Noise\">Blocks.Noise</a> for more information.
</p>
</html>"),
    uses(Modelica(version = "4.0.0")));
end NoiseGenerator;