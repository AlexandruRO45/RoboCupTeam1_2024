from controllers.models.nao_robot import NaoRobot


class Defender(NaoRobot):

    def __init__(self):
        super().__init__()
        print("Defender created")
