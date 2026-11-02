class Economy:
    def __init__(self, market, investment_pool, buildings_info, save_data, pops_info):
        self.market = market
        self.investment_pool = investment_pool
        self.buildings_info = buildings_info
        self.save_data = save_data
        self.pops_info = pops_info

    #calculate the profit
    def calculate_profit(self, building_type, employment_ratio=1):
        info = self.buildings_info[building_type]

        revenue = 0
        for good, amount in info["outputs"].items():
            revenue += amount * self.market.prices[good]

        costs = 0
        for good, amount in info["inputs"].items():
            costs += amount * self.market.prices[good]

        wages = info["workers"] * info["wage"]

        return (revenue - costs - wages) * employment_ratio

    def calculate_total_profit(self):
        total_profit = 0

        for building_type, building in self.save_data["buildings"].items():
            info = self.buildings_info[building_type]

            required_workers = building["count"] * info["workers"]

            if required_workers == 0:
                continue

            employment_ratio = building["employees"] / required_workers

            profit = self.calculate_profit(building_type, employment_ratio)

            total_profit += profit * building["count"]

        return total_profit

    def calculate_investment(self):
        buildings = self.save_data["buildings"]
        unemployed = self.save_data["population"]["unemployed"]

        while self.investment_pool >= 100:

            best_building = None
            best_profit = 0

            for building_type, info in self.buildings_info.items():

                required_workers = info["workers"]

                if required_workers > unemployed:
                    continue
                
                profit = self.calculate_profit(building_type)

                if profit > best_profit:
                    best_profit = profit
                    best_building = building_type

            if best_building is None:
                break

            if best_building not in buildings:
                buildings[best_building] = {
                    "count": 0,
                    "employees": 0
                }

            buildings[best_building]["count"] += 1

            self.investment_pool -= 100

            unemployed -= self.buildings_info[best_building]["workers"]

        self.save_data["investment_pool"] = self.investment_pool
        
    def assign_workers(self): 
        population = self.save_data["population"]
        buildings = self.save_data["buildings"]

        remaining_workers = population["total"]

        for building in buildings.values():
            building["employees"] = 0

        sorted_buildings = sorted(
            buildings.items(),
            key=lambda item: self.buildings_info[item[0]]["wage"], 
            reverse=True
        )

        for building_type, building in sorted_buildings:

            info = self.buildings_info[building_type]

            available_jobs = building["count"] * info["workers"]

            assigned = min(remaining_workers, available_jobs)

            building["employees"] = assigned
            remaining_workers -= assigned

        population["unemployed"] = remaining_workers
        
    def calculate_wages(self):
        total_wages = 0

        for building_type, building in self.save_data["buildings"].items():

            wage = self.buildings_info[building_type]["wage"]

            total_wages += building["employees"] * wage

        self.save_data["population"]["income"] = total_wages

        return total_wages

    def calculate_production(self):
        buildings = self.save_data["buildings"]

        for building_type, building in buildings.items():
            info = self.buildings_info[building_type]

            required_workers = building["count"] * info["workers"]

            if required_workers == 0:
                continue

            employment_ratio = building["employees"] / required_workers

            for good, amount in info["outputs"].items():
                production = amount * building["count"] * employment_ratio
                self.market.add_supply(good, production)

            for good, amount in info["inputs"].items():
                consumption = amount * building["count"] * employment_ratio
                self.market.add_demand(good, consumption)

    def calculate_consumption(self):
        income = self.calculate_wages()

        for good, ratio in self.pops_info["workers"]["consumption"].items():
            spending = income * ratio
            quantity = spending / self.market.prices[good]

            self.market.add_demand(good, quantity)
    
    def advance_month(self):
        self.market.reset_market()

        self.assign_workers()

        self.calculate_investment()

        self.assign_workers()

        self.calculate_production()

        self.calculate_consumption()

        self.market.update_prices()

        profit = self.calculate_total_profit()
        self.investment_pool += profit

        self.save_data["investment_pool"] = self.investment_pool

        print(f"Monthly profit: {profit:.2f}")
        print(f"Investment pool: {self.investment_pool:.2f}")
