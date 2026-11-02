class Market:
    def __init__(self, goods): 
        self.goods = goods
        self.supply = {}
        self.demand = {}
        self.prices = {}

        for good, data in goods.items():
            self.supply[good] = 0
            self.demand[good] = 0
            self.prices[good] = data["base_price"]

    def add_supply(self, good, amount):
        self.supply[good] += amount

    def add_demand(self, good, amount):
        self.demand[good] += amount

    def reset_market(self):
        for good in self.goods:
            self.supply[good] = 0
            self.demand[good] = 0

    def update_prices(self):
        for good in self.goods:
            supply = self.supply[good]
            demand = self.demand[good]
            base_price = self.goods[good]["base_price"]

            self.prices[good] = base_price * (
                    1 + (demand - supply) / (demand + supply + 1)
            )

