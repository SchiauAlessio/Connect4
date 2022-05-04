from board.board import Board


class Game(Board):
    def __init__(self):
        super().__init__()
        self.__game_over = False

    def place_piece(self, board, row, column, piece):
        """
        drops a piece on the board at a location
        :param board: the current state of the board
        :param row: the row on which the piece is inserted
        :param column: the column on which the piece is inserted
        :param piece: the piece to be dropped
        :return: -
        """
        board[row][column] = piece

    def winning_move(self, board, currently_used_piece):
        """
        Checks all possible locations on the board to find whether there is a winning situation
        First we check if there are 4 pieces horizontally, then vertically,
        then on positive sloped diagonals and then on negative sloped diagonals
        :param board: the current state of the board
        :param currently_used_piece: the piece that is checked whether it is winning or not
        :return: True in case it is a winner, otherwise none
        """
        for columns in range(super().get_column_count() - 3):
            for rows in range(super().get_row_count()):
                if board[rows][columns] == currently_used_piece:
                    if board[rows][columns + 1] == currently_used_piece:
                        if board[rows][columns + 2] == currently_used_piece:
                            if board[rows][columns + 3] == currently_used_piece:
                                return True

        for columns in range(super().get_column_count()):
            for rows in range(super().get_row_count() - 3):
                if board[rows][columns] == currently_used_piece:
                    if board[rows + 1][columns] == currently_used_piece:
                        if board[rows + 2][columns] == currently_used_piece:
                            if board[rows + 3][columns] == currently_used_piece:
                                return True

        for columns in range(super().get_column_count() - 3):
            for rows in range(super().get_row_count() - 3):
                if board[rows][columns] == currently_used_piece:
                    if board[rows + 1][columns + 1] == currently_used_piece:
                        if board[rows + 2][columns + 2] == currently_used_piece:
                            if board[rows + 3][columns + 3] == currently_used_piece:
                                return True

        for columns in range(super().get_column_count() - 3):
            for rows in range(3, super().get_row_count()):
                if board[rows][columns] == currently_used_piece:
                    if board[rows - 1][columns + 1] == currently_used_piece:
                        if board[rows - 2][columns + 2] == currently_used_piece:
                            if board[rows - 3][columns + 3] == currently_used_piece:
                                return True

    def node_is_terminal(self, board):
        player_wins=self.winning_move(board,super().get_player_piece())
        computer_wins=self.winning_move(board,super().get_ai_piece())
        number_of_valid_locations=len(super().get_valid_locations(board))
        return player_wins or computer_wins or  number_of_valid_locations==0
