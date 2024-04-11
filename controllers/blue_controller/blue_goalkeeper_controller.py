import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))))

from controllers.base.base_controller import BaseController


class Goalkeeper(BaseController):

    def __init__(self, robot):
        self.robot = robot
        print("Goalkeeper created")

    def run(self):
        # Add your secondary attacker logic here
        pass
    
    
    
    # def __init__(self):
    #     super().__init__(Goalkeeper())
    #     self.robot = Goalkeeper()




    # def run(self):
    #     super().main()

    #     while not self.can_see_the_ball():
    #         self.find_the_ball()

    #     self.update_the_supervisor_with_the_ball_location()

    #     self.take_order()