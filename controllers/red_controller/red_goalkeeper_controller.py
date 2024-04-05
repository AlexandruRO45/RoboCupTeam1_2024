import sys
import os
from abc import abstractmethod

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))))

from controllers.models.goalkeeper_supervisor import GoalKeeperSupervisor
from controllers.base_controller import BaseController


class RedGoalkeeperController(BaseController):

    def __init__(self):
        super().__init__(GoalKeeperSupervisor())
        self.robot = GoalKeeperSupervisor()

    @abstractmethod
    def main(self):
        super().main()

        while not self.can_see_the_ball():
            self.find_the_ball()

        self.update_the_supervisor_with_the_ball_location()

        self.take_order()


if __name__ == '__main__':
    controllers = RedGoalkeeperController()
    controllers.main()

"""
V1
        goalkeeper_supervisor = GoalKeeperSupervisor()
        timestep = int(goalkeeper_supervisor.getBasicTimeStep())

        # Sending a message
        # emitter = goalkeeper_supervisor.getDevice("super_emitter")
        # emitter.setChannel(5)

        # message = "Hello".encode('utf-8')
        # emitter.send(message)
        # print("message sent from: red_goalkeeper", message)

        # while goalkeeper_supervisor.step(timestep) != -1:
        #     goalkeeper_supervisor.startMotion(goalkeeper_supervisor.wipeForhead)

        # RED_DEFENDER object
        # robot_node = goalkeeper_supervisor.getFromDef("RED_DEFENDER")
        # if robot_node:
        # print(robot_node)
        # translation_field = robot_node.getField("translation")
        # translation_field.setSFVec3f([1, 2, 3])
        # pass
"""
