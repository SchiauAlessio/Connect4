"""
render(text, antialias, color, background=None) -> Surface
rect(surface, color, rect, width=0, border_radius=0, border_top_left_radius=-1, border_top_right_radius=-1, border_bottom_left_radius=-1, border_bottom_right_radius=-1) -> Rect
circle(surface, color, center, radius) -> Rect
"""
import pygame
import sys
import random
import math
import numpy as numpy


class UI:
    def __init__(self, board, game, computer, difficulty_setting):
        pygame.init()
        self.__board = board
        self.__game = game
        self.__computer = computer
        self.__game_over = False
        self.__new_board = self.__board.get_board()
        self.__turn = random.randint(self.__board.get_player(), self.__board.get_ai())
        self.__myfont = pygame.font.SysFont("TimesNewRoman", 85)
        self.__difficulty_setting = difficulty_setting

    def print_board(self, board):
        """
        prints the board
        :param board: the given board that needs to be printed
        :return:
        """
        print(numpy.flip(board, 0))
        print("\n")

    def draw_board(self, board):
        """
        draws the graphical board that the player may choose to use
        :param board: the board that gets "converted" into its graphical counterpart
        :return:
        """
        for column in range(self.__board.get_column_count()):
            for row in range(self.__board.get_row_count()):
                surface = self.__board.get_screen()
                color = self.__board.get_purple_ish()
                rectangle = (column * self.__board.get_square_size(),
                             row * self.__board.get_square_size() + self.__board.get_square_size(),
                             self.__board.get_square_size(),
                             self.__board.get_square_size())
                pygame.draw.rect(surface, color, rectangle)
                circle_surface = self.__board.get_screen()
                circle_color = self.__board.get_black()
                circle = (int(column * self.__board.get_square_size() + self.__board.get_square_size() / 2),
                          int(
                              row * self.__board.get_square_size() + self.__board.get_square_size() + self.__board.get_square_size() / 2))
                circle_radius = self.__board.get_radius()
                pygame.draw.circle(circle_surface, circle_color, circle, circle_radius)

        for column in range(self.__board.get_column_count()):
            for row in range(self.__board.get_row_count()):
                if board[row][column] == self.__board.get_player_piece():
                    circle_surface = self.__board.get_screen()
                    circle_color = self.__board.get_lime()
                    circle = (
                        int(column * self.__board.get_square_size() + self.__board.get_square_size() / 2),
                        self.__board.get_height() - int(
                            row * self.__board.get_square_size() + self.__board.get_square_size() / 2))
                    radius = self.__board.get_radius()
                    pygame.draw.circle(circle_surface, circle_color, circle, radius)
                elif board[row][column] == self.__board.get_ai_piece():
                    circle_surface = self.__board.get_screen()
                    circle_color = self.__board.get_mango_tango()
                    circle = (
                        int(column * self.__board.get_square_size() + self.__board.get_square_size() / 2),
                        self.__board.get_height() - int(
                            row * self.__board.get_square_size() + self.__board.get_square_size() / 2))
                    radius = self.__board.get_radius()
                    pygame.draw.circle(circle_surface, circle_color, circle, radius)
        pygame.display.update()

    def main_game_human_vs_computer_gui(self, new_board):
        """
        Creates a board at each step and displays the human and the ai as circles at each step.
        For every mouse motion a piece is dropped at the corresponding position, determined by
        user input or by the minimax algorithm for the case of the ai
        A message is displayed, symbolizing the winning player at the end of the game
        :param new_board:the current board
        :return: -
        """
        while not self.__game_over:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

                if event.type == pygame.MOUSEMOTION:
                    pygame.draw.rect(self.__board.get_screen(), self.__board.get_black(),
                                     (0, 0, self.__board.get_width(), self.__board.get_square_size()))
                    position = event.pos[0]
                    if self.__turn == self.__board.get_player():
                        pygame.draw.circle(self.__board.get_screen(), self.__board.get_lime(),
                                           (position, int(self.__board.get_square_size() / 2)),
                                           self.__board.get_radius())

                pygame.display.update()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    pygame.draw.rect(self.__board.get_screen(), self.__board.get_black(),
                                     (0, 0, self.__board.get_width(), self.__board.get_square_size()))
                    if self.__turn == self.__board.get_player():
                        position = event.pos[0]
                        column = int(math.floor(position / self.__board.get_square_size()))

                        if self.__board.location_is_valid(new_board, column):
                            open_row = self.__board.get_next_open_row(new_board, column)
                            self.__game.place_piece(new_board, open_row, column, self.__board.get_player_piece())

                            if self.__game.winning_move(new_board, self.__board.get_player_piece()):
                                message_label = self.__myfont.render("Player 1 wins!", 1, self.__board.get_lime())
                                self.__board.get_screen().blit(message_label, (40, 10))
                                self.__game_over = True

                            self.__turn = self.__turn + 1
                            self.__turn = self.__turn % 2

                            self.print_board(new_board)
                            self.draw_board(new_board)
            if self.__turn == self.__board.get_ai() and not self.__game_over:
                if self.__difficulty_setting.get_difficulty() == "minimax" or self.__difficulty_setting.get_difficulty() == "hardest":
                    column, minimax_score = self.__computer.minimax(new_board, 5, -math.inf, math.inf, True)
                elif self.__difficulty_setting.get_difficulty() == "medium" or self.__difficulty_setting.get_difficulty() == "hard":
                    column = self.__computer.pick_best_move(new_board, self.__board.get_ai_piece())
                else:
                    column = self.__computer.computer_random_move(new_board)
                if self.__board.location_is_valid(new_board, column):
                    open_row = self.__board.get_next_open_row(new_board, column)
                    self.__game.place_piece(new_board, open_row, column, self.__board.get_ai_piece())

                    if self.__game.winning_move(new_board, self.__board.get_ai_piece()):
                        message_label = self.__myfont.render("Player 2 wins!", 1, self.__board.get_mango_tango())
                        self.__board.get_screen().blit(message_label, (40, 10))
                        self.__game_over = True

                    self.print_board(new_board)
                    self.draw_board(new_board)

                    self.__turn = self.__turn + 1
                    self.__turn = self.__turn % 2

            if self.__game_over:
                pygame.time.wait(6000)

    def main_game_human_vs_human_gui(self, board):
        """
        Creates a board at each step and displays the players as circles at each step.
        For every mouse motion a piece is dropped at the corresponding position, determined by
        user input
        A message is displayed, symbolizing the winning player at the end of the game or "draw" when
        the score is equal
        :param board:the current board
        :return: -
        """
        while not self.__game_over:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

                if event.type == pygame.MOUSEMOTION:
                    pygame.draw.rect(self.__board.get_screen(), self.__board.get_black(),
                                     (0, 0, self.__board.get_width(), self.__board.get_square_size()))
                    position = event.pos[0]
                    if self.__turn == 0:
                        pygame.draw.circle(self.__board.get_screen(), self.__board.get_lime(),
                                           (position, int(self.__board.get_square_size() / 2)),
                                           self.__board.get_radius())
                    else:
                        pygame.draw.circle(self.__board.get_screen(), self.__board.get_mango_tango(),
                                           (position, int(self.__board.get_square_size() / 2)),
                                           self.__board.get_radius())
                pygame.display.update()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    pygame.draw.rect(self.__board.get_screen(), self.__board.get_black(),
                                     (0, 0, self.__board.get_width(), self.__board.get_square_size()))
                    if self.__turn == 0:
                        position = event.pos[0]
                        column = int(math.floor(position / self.__board.get_square_size()))

                        if self.__board.location_is_valid(board, column):
                            next_row = self.__board.get_next_open_row(board, column)
                            self.__game.place_piece(board, next_row, column, 1)

                            if self.__game.winning_move(board, 1):
                                message_label = self.__myfont.render("Player 1 wins!", 1, self.__board.get_lime())
                                self.__board.get_screen().blit(message_label, (40, 10))
                                self.__game_over = True
                        else:
                            self.__turn = 1

                        if len(self.__board.get_valid_locations(board)) == 0:
                            message_label = self.__myfont.render("WOW, A DRAW!", 1, self.__board.get_lime())
                            self.__board.get_screen().blit(message_label, (40, 10))
                            self.__game_over = True
                            self.__turn = self.__turn + 1
                            self.__turn = self.__turn % 2

                            self.print_board(board)
                            self.draw_board(board)
                    else:
                        position = event.pos[0]
                        column = int(math.floor(position / self.__board.get_square_size()))

                        if self.__board.location_is_valid(board, column):
                            next_row = self.__board.get_next_open_row(board, column)
                            self.__game.place_piece(board, next_row, column, 2)

                            if self.__game.winning_move(board, 2):
                                message_label = self.__myfont.render("Player 2 wins!", 1,
                                                                     self.__board.get_mango_tango())
                                self.__board.get_screen().blit(message_label, (40, 10))
                                self.__game_over = True
                        else:
                            self.__turn = 0
                        if len(self.__board.get_valid_locations(board)) == 0:
                            message_label = self.__myfont.render("WOW, A DRAW!", 1, self.__board.get_lime())
                            self.__board.get_screen().blit(message_label, (40, 10))
                            self.__game_over = True
                            self.__turn = self.__turn + 1
                            self.__turn = self.__turn % 2

                            self.print_board(board)
                            self.draw_board(board)

                    self.print_board(board)
                    self.draw_board(board)

                    self.__turn = self.__turn + 1
                    self.__turn = self.__turn % 2

                    if self.__game_over:
                        pygame.time.wait(6000)

    def main_game_human_vs_computer_normal(self, new_board):
        """
        Creates a board at each step and displays it as a list. The user's actions are marked with 1
        and the ai's with 2
        determined by user input, a piece is dropped at the input location
        or by the minimax algorithm for the case of the ai
        A message is displayed, symbolizing the winning player at the end of the game
        :param new_board:the current board
        :return: -
        """
        self.print_board(self.__new_board)
        while not self.__game_over:
            if self.__turn == self.__board.get_player():
                column = int(input("Choose column: ")) - 1

                if self.__board.location_is_valid(new_board, column):
                    next_open_row = self.__board.get_next_open_row(new_board, column)
                    self.__game.place_piece(new_board, next_open_row, column, self.__board.get_player_piece())

                    if self.__game.winning_move(new_board, self.__board.get_player_piece()):
                        print("PLAYER 1 WINS!!!")
                        self.__game_over = True

                    self.__turn += 1
                    self.__turn = self.__turn % 2

                    self.print_board(new_board)

            if self.__turn == self.__board.get_ai() and not self.__game_over:

                if self.__difficulty_setting.get_difficulty() == "minimax" or self.__difficulty_setting.get_difficulty() == "hardest":
                    column, minimax_score = self.__computer.minimax(new_board, 5, -math.inf, math.inf, True)
                elif self.__difficulty_setting.get_difficulty() == "medium" or self.__difficulty_setting.get_difficulty() == "hard":
                    column = self.__computer.pick_best_move(new_board, self.__board.get_ai_piece())
                else:
                    column = self.__computer.computer_random_move(new_board)

                if self.__board.location_is_valid(new_board, column):
                    open_row = self.__board.get_next_open_row(new_board, column)
                    self.__game.place_piece(new_board, open_row, column, self.__board.get_ai_piece())
                    if self.__game.winning_move(new_board, self.__board.get_ai_piece()):
                        print("PLAYER 2 WINS!!!")
                        self.__game_over = True

                    self.print_board(new_board)

                    self.__turn = self.__turn + 1
                    self.__turn = self.__turn % 2

            if self.__game_over:
                return

    def main_game_human_vs_human_normal(self, board):
        """
        Creates a board at each step and displays the players as circles at each step.
        For every mouse motion a piece is dropped at the corresponding position, determined by
        user input
        A message is displayed, symbolizing the winning player at the end of the game or "draw" when
        the score is equal
        :param board:the current board
        :return: -
        """
        self.print_board(self.__new_board)
        while not self.__game_over:
            if self.__turn == 0:
                column = int(input("PLAYER 1, choose the column: ")) - 1

                if self.__board.location_is_valid(board, column):
                    open_row = self.__board.get_next_open_row(board, column)
                    self.__game.place_piece(board, open_row, column, 1)

                    if self.__game.winning_move(board, 1):
                        print("PLAYER 1 WINS!!!\n")
                        self.__game_over = True
                else:
                    self.__turn = 1
                if len(self.__board.get_valid_locations(board)) == 0:
                    print("DRAW!!!\n")
                    self.__game_over = True
                    self.__turn += 1
                    self.__turn = self.__turn % 2

            else:
                column = int(input("PLAYER 2, choose the column: ")) - 1
                if self.__board.location_is_valid(board, column):
                    open_row = self.__board.get_next_open_row(board, column)
                    self.__game.place_piece(board, open_row, column, 2)

                    if self.__game.winning_move(board, 2):
                        print("PLAYER 2 WINS!!!")
                        self.__game_over = True
                else:
                    self.__turn = 0
                if len(self.__board.get_valid_locations(board)) == 0:
                    print("DRAW!!!\n")
                    self.__game_over = True
                    self.__turn += 1
                    self.__turn = self.__turn % 2

            self.print_board(board)
            self.draw_board(board)

            self.__turn += 1
            self.__turn = self.__turn % 2

            if self.__game_over:
                pygame.time.wait(6000)

    def user_choice_console(self):
        functions = {
            1: self.main_game_human_vs_computer_normal,
            2: self.main_game_human_vs_human_normal
        }
        while True:
            print("\n1. Player vs AI")
            print("2.Player vs Player")
            try:
                user_choice = int(input("Your choice: "))
                if user_choice in functions:
                    functions[user_choice](self.__new_board)
                    return
                else:
                    print("Option not available!!!\n")
            except ValueError:
                print("Option not available\n")
            except IndexError:
                print("Columns need to be between 1 and 7")

    def user_choice_gui(self):
        functions = {
            1: self.main_game_human_vs_computer_gui,
            2: self.main_game_human_vs_human_gui
        }
        while True:
            print("\n1. Player vs AI")
            print("2.Player vs Player")
            try:
                user_choice = int(input("Your choice: "))
                if user_choice in functions:
                    functions[user_choice](self.__new_board)
                    return
                else:
                    print("Option not available!!!\n")
            except ValueError:
                print("Option not available\n")

    def user_menu(self):
        while True:
            print("1. Console")
            print("2. GUI")
            try:
                choice = int(input("Your choice: "))
                if choice == 1:
                    self.user_choice_console()
                    return
                elif choice == 2:
                    # self.__screen = pygame.display.set_mode(self.__size)
                    self.draw_board(self.__new_board)
                    pygame.display.update()
                    self.user_choice_gui()
                    return
                else:
                    print("Option not available!!!\n")
            except ValueError:
                print("Option not available\n")
