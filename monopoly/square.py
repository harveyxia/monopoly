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
        self.mortgaged = False

        # use original owner's years
        self.original_owner = None
        self.purchase_years = [None] * len(self.rent)
        self.caps = [0] * (len(self.rent) + 3)
        self.status = None

    def add_building(self):
        if self.num_buildings == 5:
            raise ValueError('Square already has max buildings.')
        self.num_buildings += 1
        if self.should_update_cap():
            self.purchase_years[self.num_buildings] = self.original_owner.years

    def remove_building(self):
        if self.num_buildings == 0:
            raise ValueError('Square has no buildings.')
        self.num_buildings -= 1

    def get_rent(self):
        # if self.num_buildings > 1:
        #     print self.num_buildings
        #     print self.rent[self.num_buildings]
        return self.rent[self.num_buildings]

    def set_owner(self, player, index):
        self.owner = player
        if self.original_owner == None:
            self.original_owner = player
            self.purchase_years[0] = self.original_owner.years
            self.status = index

    def mortgage(self):
        if not self.mortgaged:
            self.mortgaged = True

    def unmortgage(self):
        if self.mortgaged:
            self.mortgaged = False

    def should_update_cap(self):
        # only care about result for original owner
        return self.original_owner and not self.original_owner.bankrupt

    def track_payment(self, payment):
        if self.should_update_cap():
            # print("payment of {0} on {1}".format(payment, self.name))
            if self.type == "Street":
                total_spent = self.price + self.price_build*self.num_buildings
                base_payoff = payment * (float(self.price)/total_spent)
                building_payoff = payment * (float(self.price_build)/total_spent)
                self.update_cap(0, base_payoff)
                for building_number in range(0, self.num_buildings):
                    self.update_cap(building_number, building_payoff)
            else:
                # Tracking payments for utilities and railroads
                self.update_cap(0, payment)

    # updates cap for a given building number
    def update_cap(self, building_number, payoff):
        if self.purchase_years[building_number] is None:
            return
        # print("payoff of {0} for {1} building number {2}".format(payoff, self.name, building_number))

        if building_number == 0:
            if self.status is None:
                caps_number = 0
            else:
                caps_number = self.status
        else:
            caps_number = building_number + 3
        years_elapsed = self.original_owner.years - self.purchase_years[building_number]
        self.caps[caps_number] += payoff * (1/(1+0.01))**(years_elapsed)

        if building_number == 0: 
            price = self.price 
        else: 
            price = self.price_build

        if price < self.caps[caps_number]:
            if years_elapsed > 0:
                self.caps[caps_number] = 1 / (years_elapsed * price / self.caps[caps_number])

            if self.caps[caps_number] > 1:
                self.caps[caps_number] = 1
            self.purchase_years[building_number] = None

    def clean_cap(self):
        for building_number in range(0, 6):
            if self.purchase_years[building_number] != None:
                if building_number == 0:
                    self.caps[self.status] = 0
                else:
                    self.caps[building_number + 3] = 0

