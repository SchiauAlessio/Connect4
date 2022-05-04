import numpy as numpy
import pygame

from board.board_specifications import BoardSpecifications


class Board(BoardSpecifications):
    def __init__(self):
        BoardSpecifications.__init__(self)
        self.__board = self.create_board()

    def get_board(self):
        return self.__board

    def create_board(self):
        """
        creates a board that has ROW_COUNT rows and COLUMN_COUNT columns
        :return: the board
        """
        board = numpy.zeros((super().get_row_count(), super().get_column_count()))
        return board

    def location_is_valid(self, board, column):
        """
        checks whether the current position where the user wants to place the piece is valid or not
        :param board: the current board
        :param column: the column where the player wants to place the piece
        :return: whether the position is valid (nothing is placed there, therefore a zero is found at that location
        """
        return board[super().get_row_count() - 1][column] == 0

    def get_valid_locations(self, board):
        """
        creates a list of all valid locations where a piece can be placed on the board
        :param board: the current board
        :return: the list with all the valid locations
        """
        valid_locations = []
        for column in range(super().get_column_count()):
            if self.location_is_valid(board, column):
                valid_locations.append(column)
        return valid_locations

    def get_number_of_valid_locations(self,board):
        """
        using the get_valid_locations function, return the number of valid locations(how many free spaces
        that where a move can be made"
        :param board: the current_board
        :return: the length of the list of valid locations
        """
        valid_locations=self.get_valid_locations(board)
        return len(valid_locations)

    def get_next_open_row(self, board, column):
        """
        finds the row where a piece can be placed
        :param board: the current board
        :param column: the column on which the search is made
        :return: the row
        """
        for row in range(self.get_row_count()):
            if board[row][column] == 0:
                return row
