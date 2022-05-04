from game.game import Game
import math
import random
#kinda hard
class AdvancedComputer(Game):
    def __init__(self):
        Game.__init__(self)

    def give_score_to_window(self, window, piece):
        """
        attributes a score to the current move of a piece move depending on the current state of the pieces on the board
        in order to determine the best possible move
        :param window: the current window
        :param piece: the current piece for which the decision needs to be made
        :return: the score
        """
        score = 0
        opponent_piece = Game.get_player_piece(self)
        if piece == Game.get_player_piece(self):
            opponent_piece = Game.get_ai_piece(self)

        if window.count(piece) == 4:
            score = score + 100
        elif window.count(piece) == 3 and window.count(Game.get_empty(self)) == 1:
            score = score + 5
        elif window.count(piece) == 2 and window.count(Game.get_empty(self)) == 2:
            score = score + 2

        if window.count(opponent_piece) == 3 and window.count(Game.get_empty(self)) == 1:
            score = score - 4
        return score

    def give_score_to_current_position(self, board, piece):
        """
        determines the score for all possible moves
        Firstly, the score for the center column is calculated, then horizontal then
        vertical then positive sloped diagonals then negative sloped diagonals
        :param board: the current state of the board
        :param piece: the current piece for which the score is calculated
        :return: the calculated score
        """
        score = 0
        center_array = [int(index) for index in list(board[:, Game.get_column_count(self) // 2])]
        center_array_pieces_count = center_array.count(piece)
        score = score + center_array_pieces_count * 3

        for row in range(Game.get_row_count(self)):
            row_array = [int(index) for index in list(board[row, :])]
            for column in range(Game.get_column_count(self) - 3):
                curent_window = row_array[column:column + Game.get_window_length(self)]
                score = score + self.give_score_to_window(curent_window, piece)

        for column in range(Game.get_column_count(self)):
            columns_array = [int(index) for index in list(board[:, column])]
            for row in range(Game.get_row_count(self) - 3):
                curent_window = columns_array[row:row + Game.get_window_length(self)]
                score = score + self.give_score_to_window(curent_window, piece)

        for row in range(Game.get_row_count(self) - 3):
            for column in range(Game.get_column_count(self) - 3):
                curent_window = [board[row + index][column + index] for index in range(Game.get_window_length(self))]
                score = score + self.give_score_to_window(curent_window, piece)

        for row in range(Game.get_row_count(self) - 3):
            for column in range(Game.get_column_count(self) - 3):
                curent_window = [board[row + 3 - index][column + index] for index in
                                 range(Game.get_window_length(self))]
                score = score + self.give_score_to_window(curent_window, piece)

        return score

    def pick_best_move(self, board, piece):
        """
        makes a move based on the score calculated for each possible move
        :param board: the current state of the board
        :param piece: the current piece that has to be dropped
        :return: the best column on which the ai should drop the piece
        """
        valid_locations = Game.get_valid_locations(self, board)
        best_score = -10000
        best_column = random.choice(valid_locations)
        for column in valid_locations:
            row = Game.get_next_open_row(self, board, column)
            template_board = board.copy()
            Game.place_piece(self, template_board, row, column, piece)
            score = self.give_score_to_current_position(template_board, piece)
            if score > best_score:
                best_score = score
                best_column = column

        return best_column

    def minimax(self, board, depth, alpha, beta, maximizingPlayer):
        valid_locations = Game.get_valid_locations(self, board)
        game_is_terminal = Game.node_is_terminal(self, board)
        if depth == 0 or game_is_terminal:
            if game_is_terminal:
                if Game.winning_move(self, board, Game.get_ai_piece(self)):
                    return (None, 100000000000000)
                elif Game.winning_move(self, board, Game.get_player_piece(self)):
                    return (None, -10000000000000)
                else:  # No valid moves are available so we return a tuple (None,0)
                    return (None, 0)
            else:  # Depth is zero
                return (None, self.give_score_to_current_position(board, Game.get_ai_piece(self)))
        if maximizingPlayer:
            value = -math.inf
            target_column = random.choice(valid_locations)
            for column in valid_locations:
                row = Game.get_next_open_row(self, board, column)
                board_copy = board.copy()
                Game.place_piece(self, board_copy, row, column, Game.get_ai_piece(self))
                new_score = self.minimax(board_copy, depth - 1, alpha, beta, False)[1]
                if new_score > value:
                    value = new_score
                    target_column = column
                alpha = max(alpha, value)
                if alpha >= beta:
                    break
            return target_column, value

        else:  # Minimizing player
            value = math.inf
            target_column = random.choice(valid_locations)
            for column in valid_locations:
                row = Game.get_next_open_row(self, board, column)
                board_copy = board.copy()
                Game.place_piece(self, board_copy, row, column, Game.get_player_piece(self))
                new_score = self.minimax(board_copy, depth - 1, alpha, beta, True)[1]
                if new_score < value:
                    value = new_score
                    target_column = column
                beta = min(beta, value)
                if alpha >= beta:
                    break
            return target_column, value