from controller import Supervisor
from controllers.models.goalkeeper import Goalkeeper


class GoalKeeperSupervisor(Goalkeeper, Supervisor):

    def __init__(self):
        super(GoalKeeperSupervisor, self).__init__()
        print("GoalKeeperSupervisor created")
