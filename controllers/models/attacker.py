from controllers.models.nao_robot import NaoRobot


class Attacker(NaoRobot):

    def __init__(self):
        super().__init__()
        print("Attacker created")


    def run(self):
        
        # while no error is occouring:
        # check in there is new data avaialbale
        # get the new data
        # assign new data to appropriate variables (ball position and self position)

        # if new motion option is avaialble
        # check if shot is avaialble
        # check if dribble is available

        # if error occours
        # pass
        
        pass
    
    def decision(self, ball_pos, self_pos):
        # check if a goal has been scored --> if ball position is between y dimensions(goal posts) and pass an x dimension(base line)
        # check if self has fallen over
        # if self has ball
        #  if in goal quadrent
            # find position of goalie
            # change heading to face goal around the ball
            # kick ball
        # if not in goal quadrant
            # change heading to face goal around the ball
            # move towards the goal
        # 


        pass
