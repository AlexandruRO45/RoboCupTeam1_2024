import math
from controller import Supervisor


class TeamSupervisor(Supervisor):

    def __init__(self):
        super().__init__()
        print("TeamSupervisor created")

        # inistialize all entities

        self.emitter = self.getDevice("emitter")

        self.ball = self.getFromDef("RobocupSoccerBall")

        self.robots = {
        "RED_GK"    : self.getFromDef("RED_GOALKEEPER"),
        "RED_DEF_L" : self.getFromDef("RED_DEFENDER"),
        "RED_FW_R" : self.getFromDef("RED_RIGHT_ATTACKER"),
        "RED_FW_L"    : self.getFromDef("RED_LEFT_ATTACKER"),
        "BLUE_GK"   : self.getFromDef("BLUE_GOALKEEPER"),
        "BLUE_DEF_L"  : self.getFromDef("BLUE_LEFT_DEFENDER"),
        "BLUE_DEF_R" : self.getFromDef("BLUE_RIGHT_DEFENDER"),
        "BLUE_FF" : self.getFromDef("BLUE_ATTACKER")
        }



        self.new_ball_pos = [0,0,0.1] # starts at center field [x,y,z]        

    

    def getBallPos(self):
        # can set ball zone in red blue or neutral zones later to enact the supporter and striker behaviour
        return self.ball.getField("translation").getSFVec3f()

    def setBallPos(self, current_ball_pos):
        self.new_ball_pos = current_ball_pos
        self.ball.resetPhysics()

    def setBallZone(self, ball_pos):
        if ball_pos[0] < -1.5:
            return "Red"
        elif ball_pos[0] >=-1.5 and ball_pos[0] <= 1.5:
            return "Neutral"
        else:
            return "Blue"


    def getRobotPos(self, robotName):
        return self.robots[robotName].getField("translation").getSFVec3f()

    def getBallPossessor(self):
        ballpos = self.getBallPos()
        min_dist = 16
        possessor = ""
        for robot in self.robots:
            temp_pos = self.getBallPos(robot.key())
            temp_dist = math.sqrt(temp_pos[0]**2 + temp_pos[1]**2)
            if temp_dist < min_dist:
                min_dist=temp_dist
                possessor = robot.key()
            
        return possessor

    def resetSimulation(self):
        self.previousBallLocation = [0, 0, 0.1]
        self.simulationReset()
        for robot in self.robots.values():
            robot.resetPhysics()
  
    def stopSimulation(self):
        self.simulationSetMode(self.SIMULATION_MODE_PAUSE)