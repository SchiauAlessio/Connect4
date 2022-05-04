import pygame

class BoardSpecifications:
    def __init__(self):
        """
        measurements and rgb used for creating the board
        """
        self.__blue_color = (0, 0, 255)
        self.__black_color = (0, 0, 0)
        self.__lime_color = (57, 255, 20)
        self.__mango_tango_color = (255, 130, 67)
        self.__purple_ish=(153, 102, 255)
        self.__row_count = 6
        self.__column_count = 7

        self.__player_digit = 0
        self.__ai_digit = 1

        self.__empty_space = 0
        self.__player_piece = 1
        self.__ai_piece = 2

        self.__window_length = 4

        self.__square_size = 100

        self.__width = self.__column_count * self.__square_size
        self.__height = (self.__row_count + 1) * self.__square_size

        self.__size = (self.__width, self.__height)

        self.__radius = int(self.__square_size / 2 - 5)
        self.__screen = pygame.display.set_mode(self.__size)

    def get_blue(self):
        return self.__blue_color

    def get_purple_ish(self):
        return self.__purple_ish

    def get_black(self):
        return self.__black_color

    def get_lime(self):
        return self.__lime_color

    def get_mango_tango(self):
        return self.__mango_tango_color

    def get_ai_piece(self):
        return self.__ai_piece

    def get_ai(self):
        return self.__ai_digit

    def get_player_piece(self):
        return self.__player_piece

    def get_player(self):
        return self.__player_digit

    def get_empty(self):
        return self.__empty_space

    def get_row_count(self):
        return self.__row_count

    def get_column_count(self):
        return self.__column_count

    def get_square_size(self):
        return self.__square_size

    def get_width(self):
        return self.__width

    def get_height(self):
        return self.__height

    def get_size(self):
        return self.__size

    def get_radius(self):
        return self.__radius

    def get_screen(self):
        return self.__screen

    def get_window_length(self):
        return self.__window_length