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
        self.num_buildings = 0  # 5 buildings == 1 hotel
        self.owner = None

        # use original owner's years
        self.original_owner = None
        self.purchase_years = [None] * len(rent)
        self.payoffs = [0] * len(rent)

    def add_building(self):
        if self.num_buildings == 5:
            raise ValueError('Square already has max buildings.')
        self.num_buildings += 1
        if self.should_update_npv():
            self.purchase_years[num_buildings] = self.original_owner.years
            self.update_payoff(num_buildings, -1*self.price_build)

    def remove_building(self):
        if self.num_buildings == 0:
            raise ValueError('Square has no buildings.')
        self.num_buildings -= 1

    def get_rent(self):
        return self.rent[self.num_buildings]

    def set_owner(self, player):
        self.owner = player
        if self.original_owner == None:
            self.original_owner = player
            self.purchase_years[0] = self.original_owner.years
            self.update_payoff(0, -1*self.price)

    def should_update_npv(self):
        # only care about result for original owner
        return self.original_owner and not self.original_owner.bankrupt

    def track_payment(self, payment):
        if self.should_update_npv():
            building_number = 0
            while payment > 0:
                # only count the extra payment for that building
                already_paid = self.rent[building_number-1] if building_number > 0 else 0
                to_pay = self.rent[building_number] - already_paid
                payoff = to_pay if to_pay <= payment else payment
                self.update_payoff(building_num, payoff)
                payment -= payoff
                building_number += 1

    # updates payoff for a given building number
    def update_payoff(self, building_number, payoff):
        years_elapsed = self.original_owner.years - self.purchase_years[building_number]
        self.payoff[building_number] += payoff / (1+0.05)**(years_elapsed)
