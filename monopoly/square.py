class Square(object):
    """
    A monopoly square
    """

    def __init__(self, data):
        self.name = data['name']
        self.type = data['type']
        self.color = data['color']
        self.position = int(data['position'])
        self.price = int(data['price'])
        self.price_build = int(data['price_build'])
        self.rent = {
            0: int(data['rent']),
            1: int(data['rent_build_1']),
            2: int(data['rent_build_2']),
            3: int(data['rent_build_3']),
            4: int(data['rent_build_4']),
            5: int(data['rent_build_5'])
        }
        self.num_building = 0  # 5 buildings == 1 hotel
        self.owner = None

        # use original owner's years
        self.original_owner = None

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

    def set_owner(self, player):
        self.owner = player
        if self.original_owner == None:
            self.original_owner = player
            self.purchase_year = player.years

    def update_npv(self, payment):
        pass
