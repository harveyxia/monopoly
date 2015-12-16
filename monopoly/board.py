import csv
import os

from square import Square

directory = os.path.dirname(__file__)


class Board(object):
    """Monopoly board representation
    Board data is loaded from board.csv upon object instantiation.
    """

    def __init__(self):
        self.squares = self._init_board_data()
        self.avail_houses = 32
        self.avail_hotels = 12
        self.color_index = self.build_color_index(self.squares)

    @staticmethod
    def _init_board_data(fname=directory + '/board.csv'):
        output = []
        keys = ('name',
                'type',
                'color',
                'position',
                'price',
                'price_build',
                'rent',
                'rent_build_1',
                'rent_build_2',
                'rent_build_3',
                'rent_build_4',
                'rent_build_5')
        with open(fname, 'rU') as csvfile:
            next(csvfile, None)  # skip first line (header)
            data = csv.reader(csvfile)
            for row in data:
                output.append(Square(dict(zip(keys, row))))
        return output

    @staticmethod
    def build_color_index(squares):
        color_index = {}
        for square in squares:
            if square.color.lower() != 'none':
                if square.color.lower() not in color_index:
                    color_index[square.color.lower()] = [square]
                else:
                    color_index[square.color.lower()].append(square)
        return color_index

    def get_color_group(self, color):
        return self.color_index[color.lower()]
