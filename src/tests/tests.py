import unittest
import pygame
import math
from board.board import Board
from computer.computerAI import ComputerPlayer
from game.game import Game
from settings.settings import Settings


class Tests(unittest.TestCase):
    def test_board(self):
        board = Board()
        new_board = board.get_board()
        self.assertTupleEqual(board.get_purple_ish(), (153, 102, 255))
        self.assertTupleEqual(board.get_blue(), (0, 0, 255))
        self.assertTupleEqual(board.get_black(), (0, 0, 0))
        self.assertTupleEqual(board.get_lime(), (57, 255, 20))
        self.assertTupleEqual(board.get_mango_tango(), (255, 130, 67))
        self.assertEqual(board.get_ai_piece(), 2)
        self.assertEqual(board.get_ai(), 1)
        self.assertEqual(board.get_player_piece(), 1)
        self.assertEqual(board.get_player(), 0)
        self.assertEqual(board.get_empty(), 0)
        self.assertEqual(board.get_row_count(), 6)
        self.assertEqual(board.get_column_count(), 7)
        self.assertEqual(board.get_square_size(), 100)
        self.assertEqual(board.get_width(), 700)
        self.assertEqual(board.get_height(), 700)
        self.assertTupleEqual(board.get_size(), (700, 700))
        self.assertEqual(board.get_radius(), 45)
        self.assertEqual(board.get_screen(), pygame.display.set_mode((700, 700)))
        self.assertEqual(board.get_window_length(), 4)
        self.assertTrue(board.location_is_valid(new_board, 1))
        self.assertEqual(len(board.get_valid_locations(new_board)), 7)
        self.assertEqual(board.get_next_open_row(new_board, 1), 0)

    def test_computer(self):
        computer = ComputerPlayer()
        board = Board()
        new_board = board.create_board()
        column = 3
        row = 0
        piece = 1
        columns_array = [int(i) for i in list(new_board[:, column])]
        window = columns_array[row:row + Game.get_window_length(board)]
        self.assertEqual(computer.give_score_to_window(window, piece), 0)
        self.assertEqual(computer.give_score_to_current_position(new_board, piece), 0)
        best_column = computer.pick_best_move(new_board, piece)
        self.assertGreaterEqual(best_column, 0)
        self.assertLessEqual(best_column, 6)
        column, minimax_score = computer.minimax(new_board, 5, -math.inf, math.inf, True)
        self.assertEqual(column, best_column)
        new_board[3][2] = 1
        column, minimax_score = computer.minimax(new_board, 5, -math.inf, math.inf, True)
        new_board = board.create_board()
        new_board[5][1] = 1
        column, minimax_score = computer.minimax(new_board, 5, -math.inf, math.inf, True)
        new_board[5][4] = 1
        column, minimax_score = computer.minimax(new_board, 5, -math.inf, math.inf, True)
        new_board[5][6] = 1
        column, minimax_score = computer.minimax(new_board, 5, -math.inf, math.inf, True)
        new_board[5][5] = 1
        column, minimax_score = computer.minimax(new_board, 5, -math.inf, math.inf, True)
        new_board[5][2] = 1
        column, minimax_score = computer.minimax(new_board, 5, -math.inf, math.inf, True)
        new_board[4][5] = 1
        column, minimax_score = computer.minimax(new_board, 5, -math.inf, math.inf, True)
        new_board[4][6] = 1
        column, minimax_score = computer.minimax(new_board, 5, -math.inf, math.inf, True)
        new_board[3][6] = 1
        column, minimax_score = computer.minimax(new_board, 5, -math.inf, math.inf, True)

        board=Board()
        new_board=board.create_board()
        column=computer.computer_random_move(new_board)
        self.assertGreaterEqual(column,0)
        self.assertLessEqual(column,6)
        self.assertEqual(board.get_number_of_valid_locations(new_board),7)


    def test_game(self):
        game = Game()
        board = Board()
        new_board = board.create_board()
        new_board[5][0] = 1
        new_board[4][0] = 1
        new_board[3][0] = 1
        new_board[2][0] = 1
        self.assertTrue(game.winning_move(new_board, 1))

        new_board = board.create_board()
        new_board[5][1] = 1
        new_board[5][2] = 1
        new_board[5][3] = 1
        new_board[5][4] = 1
        self.assertTrue(game.winning_move(new_board, 1))

        new_board = board.create_board()
        new_board[5][0] = 1
        new_board[4][1] = 1
        new_board[3][2] = 1
        new_board[2][3] = 1
        self.assertTrue(game.winning_move(new_board, 1))

        new_board = board.create_board()
        new_board[5][6] = 1
        new_board[4][5] = 1
        new_board[3][4] = 1
        new_board[2][3] = 1
        self.assertTrue(game.winning_move(new_board, 1))

    def test_settings(self):
        settings=Settings("testing.properties")
        current_difficulty="minimax"
        self.assertEqual(settings.get_difficulty(),current_difficulty)