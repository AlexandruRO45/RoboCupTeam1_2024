#Final Fuzzzy Draft
# Draft: Robot 1 MRC

# Copyright 1996-2023 Cyberbotics Ltd.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Example of Python controller for Nao robot.
   This demonstrates how to access sensors and actuators"""

from controller import Robot, Keyboard, Motion, Receiver
from controller import Robot, Motor, GPS, InertialUnit
import fuzzylite as fl
import math

# COMS



timestep=64

class Nao (Robot):
    PHALANX_MAX = 8

    # load motion files
    def loadMotionFiles(self):
        self.handWave = Motion('../../motions/HandWave.motion')
        self.forwards = Motion('../../motions/Forwards50.motion')
        self.backwards = Motion('../../motions/Backwards.motion')
        self.sideStepLeft = Motion('../../motions/SideStepLeft.motion')
        self.sideStepRight = Motion('../../motions/SideStepRight.motion')
        self.turnLeft20 = Motion('../../motions/TurnLeft20.motion')
        self.turnRight20 = Motion('../../motions/TurnRight20.motion')
        self.turnLeft20 = Motion('../../motions/TurnLeft40.motion')
        self.turnRight20 = Motion('../../motions/TurnRight40.motion')
        self.taiChi = Motion('../../motions/TaiChi.motion')
        self.wipeForhead = Motion('../../motions/WipeForehead.motion')
        self.StandUpFromFront= Motion('../../motions/StandUpFromFront.motion')
        self.Shoot= Motion('../../motions/Shoot.motion')

    def startMotion(self, motion):
        # interrupt current motion
        if self.currentlyPlaying:
            self.currentlyPlaying.stop()

        # start new motion
        motion.play()
        self.currentlyPlaying = motion

    # the accelerometer axes are oriented as on the real robot
    # however the sign of the returned values may be opposite
    def printAcceleration(self):
        acc = self.accelerometer.getValues()
        print('----------accelerometer----------')
        print('acceleration: [ x y z ] = [%f %f %f]' % (acc[0], acc[1], acc[2]))

    # the gyro axes are oriented as on the real robot
    # however the sign of the returned values may be opposite
    def printGyro(self):
        vel = self.gyro.getValues()
        print('----------gyro----------')
        # z value is meaningless due to the orientation of the Gyro
        print('angular velocity: [ x y ] = [%f %f]' % (vel[0], vel[1]))

    def printGps(self):
        p = self.gps.getValues()
        print('----------gps----------')
        print('position: [ x y z ] = [%f %f %f]' % (p[0], p[1], p[2]))

    # the InertialUnit roll/pitch angles are equal to naoqi's AngleX/AngleY
    def printInertialUnit(self):
        rpy = self.inertialUnit.getRollPitchYaw()
        print('----------inertial unit----------')
        print('roll/pitch/yaw: [%f %f %f]' % (rpy[0], rpy[1], rpy[2]))

    def printFootSensors(self):
        fsv = []  # force sensor values

        fsv.append(self.fsr[0].getValues())
        fsv.append(self.fsr[1].getValues())

        left = []
        right = []

        newtonsLeft = 0
        newtonsRight = 0

        # The coefficients were calibrated against the real
        # robot so as to obtain realistic sensor values.
        left.append(fsv[0][2] / 3.4 + 1.5 * fsv[0][0] + 1.15 * fsv[0][1])  # Left Foot Front Left
        left.append(fsv[0][2] / 3.4 + 1.5 * fsv[0][0] - 1.15 * fsv[0][1])  # Left Foot Front Right
        left.append(fsv[0][2] / 3.4 - 1.5 * fsv[0][0] - 1.15 * fsv[0][1])  # Left Foot Rear Right
        left.append(fsv[0][2] / 3.4 - 1.5 * fsv[0][0] + 1.15 * fsv[0][1])  # Left Foot Rear Left

        right.append(fsv[1][2] / 3.4 + 1.5 * fsv[1][0] + 1.15 * fsv[1][1])  # Right Foot Front Left
        right.append(fsv[1][2] / 3.4 + 1.5 * fsv[1][0] - 1.15 * fsv[1][1])  # Right Foot Front Right
        right.append(fsv[1][2] / 3.4 - 1.5 * fsv[1][0] - 1.15 * fsv[1][1])  # Right Foot Rear Right
        right.append(fsv[1][2] / 3.4 - 1.5 * fsv[1][0] + 1.15 * fsv[1][1])  # Right Foot Rear Left

        for i in range(0, len(left)):
            left[i] = max(min(left[i], 25), 0)
            right[i] = max(min(right[i], 25), 0)
            newtonsLeft += left[i]
            newtonsRight += right[i]

        print('----------foot sensors----------')
        print('+ left ---- right +')
        print('+-------+ +-------+')
        print('|' + str(round(left[0], 1)) +
              '  ' + str(round(left[1], 1)) +
              '| |' + str(round(right[0], 1)) +
              '  ' + str(round(right[1], 1)) +
              '|  front')
        print('| ----- | | ----- |')
        print('|' + str(round(left[3], 1)) +
              '  ' + str(round(left[2], 1)) +
              '| |' + str(round(right[3], 1)) +
              '  ' + str(round(right[2], 1)) +
              '|  back')
        print('+-------+ +-------+')
        print('total: %f Newtons, %f kilograms'
              % ((newtonsLeft + newtonsRight), ((newtonsLeft + newtonsRight) / 9.81)))

    def printFootBumpers(self):
        ll = self.lfootlbumper.getValue()
        lr = self.lfootrbumper.getValue()
        rl = self.rfootlbumper.getValue()
        rr = self.rfootrbumper.getValue()
        print('----------foot bumpers----------')
        print('+ left ------ right +')
        print('+--------+ +--------+')
        print('|' + str(ll) + '  ' + str(lr) + '| |' + str(rl) + '  ' + str(rr) + '|')
        print('|        | |        |')
        print('|        | |        |')
        print('+--------+ +--------+')

    def printUltrasoundSensors(self):
        dist = []
        for i in range(0, len(self.us)):
            dist.append(self.us[i].getValue())

        print('-----ultrasound sensors-----')
        print('left: %f m, right %f m' % (dist[0], dist[1]))

    def printCameraImage(self, camera):
        scaled = 2  # defines by which factor the image is subsampled
        width = camera.getWidth()
        height = camera.getHeight()

        # read rgb pixel values from the camera
        image = camera.getImage()

        print('----------camera image (gray levels)---------')
        print('original resolution: %d x %d, scaled to %d x %f'
              % (width, height, width / scaled, height / scaled))

        for y in range(0, height // scaled):
            line = ''
            for x in range(0, width // scaled):
                gray = camera.imageGetGray(image, width, x * scaled, y * scaled) * 9 / 255  # rescale between 0 and 9
                line = line + str(int(gray))
            print(line)

    def setAllLedsColor(self, rgb):
        # these leds take RGB values
        for i in range(0, len(self.leds)):
            self.leds[i].set(rgb)

        # ear leds are single color (blue)
        # and take values between 0 - 255
        self.leds[5].set(rgb & 0xFF)
        self.leds[6].set(rgb & 0xFF)

    def setHandsAngle(self, angle):
        for i in range(0, self.PHALANX_MAX):
            clampedAngle = angle
            if clampedAngle > self.maxPhalanxMotorPosition[i]:
                clampedAngle = self.maxPhalanxMotorPosition[i]
            elif clampedAngle < self.minPhalanxMotorPosition[i]:
                clampedAngle = self.minPhalanxMotorPosition[i]

            if len(self.rphalanx) > i and self.rphalanx[i] is not None:
                self.rphalanx[i].setPosition(clampedAngle)
            if len(self.lphalanx) > i and self.lphalanx[i] is not None:
                self.lphalanx[i].setPosition(clampedAngle)

    def printHelp(self):
        print('----------nao_demo_python----------')
        print('Use the keyboard to control the robots (one at a time)')
        print('(The 3D window need to be focused)')
        print('[Up][Down]: move one step forward/backwards')
        print('[<-][->]: side step left/right')
        print('[Shift] + [<-][->]: turn left/right')
        print('[U]: print ultrasound sensors')
        print('[A]: print accelerometers')
        print('[G]: print gyros')
        print('[S]: print gps')
        print('[I]: print inertial unit (roll/pitch/yaw)')
        print('[F]: print foot sensors')
        print('[B]: print foot bumpers')
        print('[Home][End]: print scaled top/bottom camera image')
        print('[PageUp][PageDown]: open/close hands')
        print('[7][8][9]: change all leds RGB color')
        print('[0]: turn all leds off')
        print('[T]: perform Tai chi movements')
        print('[W]: wipe its forehead')
        print('[H]: print this help message')

    def findAndEnableDevices(self):
        # get the time step of the current world.
        self.timeStep = int(self.getBasicTimeStep())

        # camera
        self.cameraTop = self.getDevice("CameraTop")
        self.cameraBottom = self.getDevice("CameraBottom")
        self.cameraTop.enable(4 * self.timeStep)
        self.cameraBottom.enable(4 * self.timeStep)

        # accelerometer
        self.accelerometer = self.getDevice('accelerometer')
        self.accelerometer.enable(4 * self.timeStep)

        # gyro
        self.gyro = self.getDevice('gyro')
        self.gyro.enable(4 * self.timeStep)

        # gps
        self.gps = self.getDevice('gps')
        self.gps.enable(4 * self.timeStep)

        # inertial unit
        self.inertialUnit = self.getDevice('inertial unit')
        self.inertialUnit.enable(self.timeStep)

        # ultrasound sensors
        self.us = []
        usNames = ['Sonar/Left', 'Sonar/Right']
        for i in range(0, len(usNames)):
            self.us.append(self.getDevice(usNames[i]))
            self.us[i].enable(self.timeStep)

        # foot sensors
        self.fsr = []
        fsrNames = ['LFsr', 'RFsr']
        for i in range(0, len(fsrNames)):
            self.fsr.append(self.getDevice(fsrNames[i]))
            self.fsr[i].enable(self.timeStep)

        # foot bumpers
        self.lfootlbumper = self.getDevice('LFoot/Bumper/Left')
        self.lfootrbumper = self.getDevice('LFoot/Bumper/Right')
        self.rfootlbumper = self.getDevice('RFoot/Bumper/Left')
        self.rfootrbumper = self.getDevice('RFoot/Bumper/Right')
        self.lfootlbumper.enable(self.timeStep)
        self.lfootrbumper.enable(self.timeStep)
        self.rfootlbumper.enable(self.timeStep)
        self.rfootrbumper.enable(self.timeStep)

        # there are 7 controlable LED groups in Webots
        self.leds = []
        self.leds.append(self.getDevice('ChestBoard/Led'))
        self.leds.append(self.getDevice('RFoot/Led'))
        self.leds.append(self.getDevice('LFoot/Led'))
        self.leds.append(self.getDevice('Face/Led/Right'))
        self.leds.append(self.getDevice('Face/Led/Left'))
        self.leds.append(self.getDevice('Ears/Led/Right'))
        self.leds.append(self.getDevice('Ears/Led/Left'))

        # get phalanx motor tags
        # the real Nao has only 2 motors for RHand/LHand
        # but in Webots we must implement RHand/LHand with 2x8 motors
        self.lphalanx = []
        self.rphalanx = []
        self.maxPhalanxMotorPosition = []
        self.minPhalanxMotorPosition = []
        for i in range(0, self.PHALANX_MAX):
            self.lphalanx.append(self.getDevice("LPhalanx%d" % (i + 1)))
            self.rphalanx.append(self.getDevice("RPhalanx%d" % (i + 1)))

            # assume right and left hands have the same motor position bounds
            self.maxPhalanxMotorPosition.append(self.rphalanx[i].getMaxPosition())
            self.minPhalanxMotorPosition.append(self.rphalanx[i].getMinPosition())

        # shoulder pitch motors
        self.RShoulderPitch = self.getDevice("RShoulderPitch")
        self.LShoulderPitch = self.getDevice("LShoulderPitch")

        # keyboard
        self.keyboard = self.getKeyboard()
        self.keyboard.enable(10 * self.timeStep)

    def __init__(self):
        Robot.__init__(self)
        self.currentlyPlaying = False

        # initialize stuff
        self.findAndEnableDevices()
        self.loadMotionFiles()
        self.printHelp()

    def run(self):
        self.handWave.setLoop(True)
        self.handWave.play()
        self.currentlyPlaying = self.handWave

        # until a key is pressed
        key = -1
        while robot.step(self.timeStep) != -1:
            key = self.keyboard.getKey()
            if key > 0:
                break

        self.handWave.setLoop(False)

        while True:
            key = self.keyboard.getKey()

            if key == Keyboard.LEFT:
                self.startMotion(self.sideStepLeft)
            elif key == Keyboard.RIGHT:
                self.startMotion(self.sideStepRight)
            elif key == Keyboard.UP:
                self.startMotion(self.forwards)
            elif key == Keyboard.DOWN:
                self.startMotion(self.backwards)
            elif key == Keyboard.LEFT | Keyboard.SHIFT:
                self.startMotion(self.turnLeft60)
            elif key == Keyboard.RIGHT | Keyboard.SHIFT:
                self.startMotion(self.turnRight60)
            elif key == ord('A'):
                self.printAcceleration()
            elif key == ord('G'):
                self.printGyro()
            elif key == ord('S'):
                self.printGps()
            elif key == ord('I'):
                self.printInertialUnit()
            elif key == ord('F'):
                self.printFootSensors()
            elif key == ord('B'):
                self.printFootBumpers()
            elif key == ord('U'):
                self.printUltrasoundSensors()
            elif key == ord('T'):
                self.startMotion(self.taiChi)
            elif key == ord('W'):
                self.startMotion(self.wipeForhead)
            elif key == ord('K'):
                self.startMotion(self.Shoot)
            elif key == ord('M'):
                self.startMotion(self.StandUpFromFront)
            elif key == Keyboard.HOME:
                self.printCameraImage(self.cameraTop)
            elif key == Keyboard.END:
                self.printCameraImage(self.cameraBottom)
            elif key == Keyboard.PAGEUP:
                self.setHandsAngle(0.96)
            elif key == Keyboard.PAGEDOWN:
                self.setHandsAngle(0.0)
            elif key == ord('7'):
                self.setAllLedsColor(0xff0000)  # red
            elif key == ord('8'):
                self.setAllLedsColor(0x00ff00)  # green
            elif key == ord('9'):
                self.setAllLedsColor(0x0000ff)  # blue
            elif key == ord('0'):
                self.setAllLedsColor(0x000000)  # off
            elif key == ord('H'):
                self.printHelp()

            if robot.step(self.timeStep) == -1:
                break

            elif key == ord('L'):
                gps = robot.getDevice("gps")
                gps.enable(timestep)
                imu = robot.getDevice("inertial unit")
                imu.enable(timestep)

                # set the target waypoint which comes as a variable
                # test waypoint = [2.0, 2.0, 00]  # x, z coordinates, uncomment to test
                receiver = robot.getDevice("receiver")  # access the node
                receiver.enable(64)

                # Initialize variables

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


                # Loop
                while robot.step(timestep) != -1:
                    
                    if receiver.getQueueLength() > 0:
                        received_data_string = receiver.getString()
                        received_numbers = [float(num) for num in received_data_string.split(",")]

                        if len(received_numbers) == 9:
                        
                            s, a, j, k, v, p, x, y, z = received_numbers
                            print(f"Received 4D coordinates: ({s}, {a}, {j}, {k}, {v}, {p}, {x}, {y}, {z})")
                            waypoint = received_numbers[3:6]

                        elif len(received_numbers) == 4 and received_numbers[0]== 1 :
                                        h, q, r, t = received_numbers
                                        print(f"Received 3D coordinates: ({h}, {q}, {r}, {t})")
                                    
                                        GetBall= [q,r,t]
                                        print(f"***ROBOT 1 GOING FOR THE BALL*** cords : {GetBall}")
                        else:
                           
                            print("Invalid or no data received.")
                            
                   # print(f"Formation coordinates: {formation}")
                    print(f"Robot B Waypoint coordinates: {waypoint}")      

                        # Clear the received data from the queue
                    receiver.nextPacket()

                    def calculate_orientation_difference(desired_orientation, current_orientation):
        # Calculate orientation difference (normalized to [-pi, pi])
                        orientation_difference = desired_orientation - current_orientation
                        while orientation_difference > math.pi:
                            orientation_difference -= 2 * math.pi
                        while orientation_difference < -math.pi:
                            orientation_difference += 2 * math.pi
                        return orientation_difference
                    def main():
                        supervisor = Robot()
                        gps = supervisor.getDevice("gps")
                        imu = supervisor.getDevice("imu")
                
                    # Loop
                   
                    
                # Get current position and orientation
                    position = gps.getValues()
                    orientation = imu.getRollPitchYaw()
    
                    direction = [waypoint[0] - position[0], waypoint[1] - position[1]]  # Use x and y coordinates
                    desired_orientation = math.atan2(direction[1], direction[0])
                    orientation_difference = calculate_orientation_difference(desired_orientation, orientation[2])
                    distance = math.sqrt(direction[0]**2 + direction[1]**2)  # Use x and y coordinates
            
                    print(f"Robot B Target orientation: {desired_orientation:.2f}")
                    print(f"Robot B Orientation Difference: {orientation_difference:.2f}")
                    print(f"Robot B Distance to waypoint: {distance:.2f}")


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
                                    
            
    '''
                    if abs(orientation_difference) > 0.05:
                        turn_speed = 0.1  # Adjust turning speed
                        if orientation_difference > 0:
                            self.startMotion(self.turnLeft20)
                            print("Robot B Turning left")
                        else:
                            self.startMotion(self.turnRight20)  # Turn right
                            print("Robot B Turning right")
                    else:
                        forward_speed = 0.2  # Adjust forward speed
                        if distance > 0.5:
                            self.startMotion(self.forwards) # Move forward
                            print("Robot B Moving forward")
                        else:
                            print("Robot B Reached the waypoint!")
                            break
                            '''


# create the Robot instance and run main loop
robot = Nao()
robot.run()


                    
    