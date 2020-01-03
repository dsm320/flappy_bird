class GameStats:
    """ A class to keep track of game statistics """

    def __init__(self):
        """ Initialize game statistics based on highscore file """
        self.reset_stats()

        self.game_active = False
        self.ai_active = False

        with open('highscore.txt') as file_object:
            high_score = file_object.read()
        self.high_score = int(high_score)


    def reset_stats(self):
        """ Resets score to 0 upon new game """
        self.score = 0
        self.bird_count = 0
        self.gen_count = 0
