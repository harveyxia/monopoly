import csv

from square import Square

class Board(object):
    """Monopoly board representation
    Board data is loaded from board.csv upon object instantiation.
    """

    def __init__(self):
        self.squares = self._load_board_data()

    def _load_board_data(self, fname='board.csv'):
        output = []
        keys = ('name', 'type', 'color', 'position', 'price', 'price_build', 'rent', 'rent_build_1', 'rent_build_2', 'rent_build_3', 'rent_build_4', 'rent_build_5')
        with open(fname, 'rU') as csvfile:
            data = csv.reader(csvfile)
            for row in data:
                # output.append( dict(zip(keys, row)) )
                output.append(Square(dict(zip(keys, row))))
        return output