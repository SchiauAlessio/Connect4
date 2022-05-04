from UI.console import UI
from board.board import Board
from board.board_specifications import BoardSpecifications
from computer.computerAI import ComputerPlayer
from game.game import Game
import pygame
import sys
import random
import math

from settings.settings import Settings

if __name__ == '__main__':
    pygame.init()
    board_specifications = BoardSpecifications()
    board = Board()
    new_board = board.get_board()
    game = Game()
    computer = ComputerPlayer()
    settings=Settings("settings.properties")
    ui = UI(board, game, computer,settings)
    ui.draw_board(new_board)
    pygame.display.update()
    
    ui.user_menu()
