import sys
import os
from abc import abstractmethod

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))))

from controllers.models.attacker import Attacker
from controllers.base.base_controller import BaseController


class RedLeftAttackerController(BaseController):

    def __init__(self):
        super().__init__(Attacker())
        self.robot = Attacker()

    @abstractmethod
    def main(self):
        super().main()

        while not self.can_see_the_ball():
            self.find_the_ball()

        self.update_the_supervisor_with_the_ball_location()

        self.take_order()


if __name__ == '__main__':
    controller = RedLeftAttackerController()
    controller.main()
