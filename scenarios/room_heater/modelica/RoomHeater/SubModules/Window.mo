within RoomHeater.SubModules;
model Window "Lumped thermal element transporting heat without storing it"
  extends Modelica.Thermal.HeatTransfer.Interfaces.Element1D;
  Modelica.Units.SI.ThermalConductance G "Constant thermal conductance of material";
  Modelica.Blocks.Interfaces.IntegerInput window_state annotation(
    Placement(transformation(origin = {-1, 115}, extent = {{-15, -15}, {15, 15}}, rotation = -90), iconTransformation(origin = {0, 134}, extent = {{-20, -20}, {20, 20}}, rotation = -90)));
equation
  if window_state == 0 then
    G = 100.0;
  elseif window_state == 1 then
    G = 10.0;
  else
    G = 2.5;
  end if;
  Q_flow = G*dT;
  annotation(
    Icon(coordinateSystem(preserveAspectRatio = true, extent = {{-100, -100}, {100, 100}}), graphics = {Rectangle(fillColor = {192, 192, 192}, pattern = LinePattern.None, fillPattern = FillPattern.Backward, extent = {{-90, 70}, {90, -70}}), Line(points = {{-90, 70}, {-90, -70}}, thickness = 0.5), Line(points = {{90, 70}, {90, -70}}, thickness = 0.5), Text(textColor = {0, 0, 255}, extent = {{-150, 120}, {150, 80}}, textString = "%name")}),
    Documentation(info = "<html>
<p>
This is a model for transport of heat without storing it; see also:
<a href=\"modelica://Modelica.Thermal.HeatTransfer.Components.ThermalResistor\">ThermalResistor</a>.
It may be used for complicated geometries where
the thermal conductance G (= inverse of thermal resistance)
is determined by measurements and is assumed to be constant
over the range of operations. If the component consists mainly of
one type of material and a regular geometry, it may be calculated,
e.g., with one of the following equations:
</p>
<ul>
<li><p>
    Conductance for a <strong>box</strong> geometry under the assumption
    that heat flows along the box length:</p>
    <blockquote><pre>
G = k*A/L
k: Thermal conductivity (material constant)
A: Area of box
L: Length of box
    </pre></blockquote>
    </li>
<li><p>
    Conductance for a <strong>cylindrical</strong> geometry under the assumption
    that heat flows from the inside to the outside radius
    of the cylinder:</p>
    <blockquote><pre>
G = 2*pi*k*L/log(r_out/r_in)
pi   : Modelica.Constants.pi
k    : Thermal conductivity (material constant)
L    : Length of cylinder
log  : Modelica.Math.log;
r_out: Outer radius of cylinder
r_in : Inner radius of cylinder
    </pre></blockquote>
    </li>
</ul>
<blockquote><pre>
Typical values for k at 20 degC in W/(m.K):
  aluminium   220
  concrete      1
  copper      384
  iron         74
  silver      407
  steel        45 .. 15 (V2A)
  wood         0.1 ... 0.2
</pre></blockquote>
</html>"),
    uses(Modelica(version = "4.0.0")));
end Window;