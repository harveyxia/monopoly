class Square(object):
    """ A monopoly square
    """

    def __init__(self, data):
        self.name = data['name']
        self.type = data['type']
        self.color = data['color']
        self.position = data['position']
        self.price = data['price']
        self.price_build = data['price_build']
        self.rent = {
            0 : data['rent'],
            1 : data['rent_build_1'],
            2 : data['rent_build_2'],
            3 : data['rent_build_3'],
            4 : data['rent_build_4'],
            5 : data['rent_build_5']
        }

        self.owner = None
        self.num_building = 0           # 5 buildings == 1 hotel

    def add_building(self):
        if self.num_building == 5:
            raise ValueError('Square already has max buildings.')
        self.num_building += 1

    def remove_building(self):
        if self.num_building == 0:
            raise ValueError('Square has no buildings.')
        self.num_building -= 1

    def get_rent(self):
        return self.rent[self.num_building]
