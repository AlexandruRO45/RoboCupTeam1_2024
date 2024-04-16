#Only Fuzzy draft
import fuzzylite as fl

# Create the fuzzy logic engine
engine = fl.Engine(
    name="ObstacleAvoidance",
    input_variables=[
        fl.InputVariable(
            name="input1",
            minimum=-3.9159,
            maximum=3.94159,
            lock_range=False,
            terms=[
                fl.Trapezoid("FarCCW", -5.389, -4.08, -2.81248, -1.84259),
                fl.Trapezoid("CCW", -2.62975, -2.115, -1.09761, -0.4782), 
                fl.Trapezoid("Center", -0.647803, -0.1509, 0.125296, 0.659436),
                fl.Trapezoid("CW", 0.461731, 1.05301, 2.09883, 2.68355),
                fl.Trapezoid("FarCW", 1.85422, 2.81006, 4.105, 5.415)]
        )
    ],
    output_variables=[
        fl.OutputVariable(
            name="Drive",
            minimum=-6,
            maximum=6,
            lock_range=False,
            lock_previous=False,
            default_value=fl.nan,
            aggregation=fl.Maximum(),
            defuzzifier=fl.Centroid(resolution=100),
            terms=[
                fl.Trapezoid("Right40", -8.25, -6.25, -4.48658, -3.45617),
                fl.Trapezoid("Right20", -4.31485, -3.60644, -1.78175, -0.75),
                fl.Trapezoid("Forward", -1.78175, -0.794275, 0.858676, 1.80322),
                fl.Trapezoid("Left20", 0.75, 1.93202, 3.54204, 4.42218),
                fl.Trapezoid("Left40", 3.56351, 4.52952, 6.25, 8.25)],
        )
    ],
    rule_blocks=[
        fl.RuleBlock(
            name="mamdani",
            conjunction=None,
            disjunction=None,
            implication=fl.AlgebraicProduct(),
            activation=fl.General(),
            rules=[
                fl.Rule.create("if input1 is FarCCW then Drive is Right40"),
                fl.Rule.create("if input1 is CCW then Drive is Right20"),
                fl.Rule.create("if input1 is Center then Drive is Forward"),
                fl.Rule.create("if input1 is CW then Drive is Left20"),
                fl.Rule.create("if input1 is FarCW then Drive is Left40"),
            ],
        )
    ],
)


# Get the defuzzified output
#obstacle_value = 0.7

# Evaluate the rules
#get the fuzzy process
engine.input_variable("input1").value = 0.7
engine.process()
print("y =", engine.output_variable("Drive").value)
DriveOut= engine.output_variable("Drive").value
print (DriveOut)

if 1.8< DriveOut < 4.1:
    self.startMotion(self.turnLeft20)
    print("Robot B Turning left 20")

elif 4.1< DriveOut:
    self.startMotion(self.turnLeft40)
    print("Robot B Turning left 40")

elif -1.8< DriveOut < -4.1:
    self.startMotion(self.turnRight20)
    print("Robot B Turning right 20")

elif -4.1< DriveOut:
    self.startMotion(self.turnRight40)
    print("Robot B Turning right 40")
else:
    self.startMotion(self.forwards)
    print("Robot B moving forward")



# > y = 0.5
