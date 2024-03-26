from controllers.models.nao_robot import NaoRobot

class BaseController:

    def __init__(self, robot: NaoRobot):
        self._robot = robot
        self._timestep = int(robot.getBasicTimeStep())
        self._can_see_the_ball = False
        # Initialize communication devices
        self._receiver = self._robot.getReceiver("receiver")
        self._receiver.enable(self._timestep)
        self._emitter = self._robot.getEmitter("emitter")
        # Initial state
        self._state = 'searching'

    def connect_to_supervisor(self):
        # Placeholder for any additional setup for connecting to the supervisor if needed
        pass

    def can_see_the_ball(self):
        return self._can_see_the_ball

    def find_the_ball(self):
        if not self.can_see_the_ball():
            # Example of a simple search routine
            self._robot.rotate(angle=30)  # Assuming there's a rotate method
        self._can_see_the_ball = self._robot.ballDetected(
            self._robot.upperCamera, max_distance=500
        ) or self._robot.ballDetected(
            self._robot.lowerCamera, max_distance=500
        )
        if self._can_see_the_ball:
            self._state = 'tracking'
        else:
            self._state = 'searching'

    def update_the_supervisor_with_the_ball_location(self):
        if self.can_see_the_ball():
            ball_position = self._robot.getBallPosition()
            message = f"ball:{ball_position[0]},{ball_position[1]},{ball_position[2]}"
            self._emitter.send(message.encode('utf-8'))

    def take_order(self):
        if self._receiver.getQueueLength() > 0:
            message = self._receiver.getData().decode('utf-8')
            self._receiver.nextPacket()
            # Example command parsing
            if message.startswith('move_to'):
                _, x, y = message.split(':')
                self._robot.moveTo(float(x), float(y))  # Assuming a moveTo method
            elif message == 'kick':
                self._robot.kick()
            self._state = 'executing_order'

    def main(self):
        self.connect_to_supervisor()
        while self._robot.step(self._timestep) != -1:
            if self._state == 'searching':
                self.find_the_ball()
            elif self._state == 'tracking':
                self.update_the_supervisor_with_the_ball_location()
            elif self._state == 'executing_order':
                self.take_order()
            # The robot can continue checking or switch to other states as needed

if __name__ == "__main__":
    # Assuming NaoRobot is initialized and passed correctly
    nao_robot = NaoRobot()  # This line is placeholder and needs actual robot initialization
    controller = BaseController(nao_robot)
    controller.main()
