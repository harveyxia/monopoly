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
        self.rent = data['rent']
        self.rent_build_1 = data['rent_build_1']
        self.rent_build_2 = data['rent_build_2']
        self.rent_build_3 = data['rent_build_3']
        self.rent_build_4 = data['rent_build_4']
        self.rent_build_5 = data['rent_build_5']

        self.owner = None
        self.num_building = 0           # 5 buildings == 1 hotel

    def set_owner(self, owner):
        self.owner = owner

    def add_building(self):
        if self.num_building == 5:
            raise ValueError('Square already has max buildings.')
        self.num_building += 1

    def remove_building(self):
        if self.num_building == 0:
            raise ValueError('Square has no buildings.')
        self.num_building -= 1