import random
import math

from computer.advanced_computer import AdvancedComputer
from game.game import Game


class ComputerPlayer(AdvancedComputer):
    def __init__(self):
        AdvancedComputer.__init__(self)


    def computer_random_move(self,board):
        """
        picks a random column from the available valid locations and then places the piece there
        :param board: the current board
        :return: the random column that was chosen
        """
        valid_locations=AdvancedComputer.get_valid_locations(self,board)
        random_column=random.choice(valid_locations)
        return random_column
        # open_row_on_chosen_column=Game.get_next_open_row(self,board,random_column)
        # Game.place_piece(self,board,open_row_on_chosen_column,random_column,piece)



