import csv
import os

from square import Square

dir = os.path.dirname(__file__)

class Board(object):
    """Monopoly board representation
    Board data is loaded from board.csv upon object instantiation.
    """

    def __init__(self):
        self.squares = self._init_board_data()
        self.avail_houses = 32
        self.avail_hotels = 12

    def _init_board_data(self, fname=dir + '/board.csv'):
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
            data = csv.reader(csvfile)
            for row in data:
                output.append(Square(dict(zip(keys, row))))
        return output
