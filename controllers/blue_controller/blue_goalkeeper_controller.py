import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))))

from controllers.models.goalkeeper_supervisor import GoalKeeperSupervisor
from controllers.base.base_controller import BaseController


# Define the controller classes: Goalkeeper, Defender, MainAttacker, SecondaryAttacker
class Goalkeeper:
    def __init__(self, robot):
        self.robot = robot
        # Add your goalkeeper initialization code here

    def run(self):
        # Add your goalkeeper logic here
        pass

