import json

from engine.market import Market
from engine.economy import Economy

def load_json(filename):
    with open(filename, "r") as file:
        return json.load(file)

goods_info = load_json("data/goods.json")
buildings_info = load_json("data/buildings.json")
pops_info = load_json("data/pops.json")
save_data = load_json("saves/save.json")

market = Market(goods_info)

economy = Economy(
    market,
    save_data["investment_pool"],
    buildings_info,
    save_data,
    pops_info
)

def show_status():
    population = save_data["population"]

    print("\n ===== ECONOMY STATUS =====")
    print(f"Population: {population['total']}")
    print(f"Unemployed: {population['unemployed']}")
    print(f"Investment pool: {economy.investment_pool:.2f}")

    print("\n----- Buildings -----")
    for building_type, building in save_data['buildings'].items():
        print(
                f"{building_type}: {building['count']} buildings, "
                f"{building['employees']} employees" 
        )

    print("\n ----- Market -----")
    for good in goods_info:
        print(
                f"{good}: Price {market.prices[good]:.2f}, "
                f"Supply {market.supply[good]:.2f}, "
                f"Demand {market.demand[good]:.2f}"
        )

def save_game():
    save_data['investment_pool'] = economy.investment_pool

    with open("saves/save.json", "w") as file:
        json.dump(save_data, file, indent=4)

# main game loop by month
while (True):
    command = input("\n> ").strip().lower().split()
    
    if not command:
        continue
    
    if command[0] == "help":
        print("""
            end, advances until next month
            status, shows the current statistics
            save, saves the game under saves/save.json
            quit, exits the game without saving
            """)

    elif command[0] == "end":
        economy.advance_month()
        show_status()
    
    elif command[0] == "status":
        show_status()

    elif command[0] == "save":
        save_game()
        print("Game saved.")

    elif command[0] == "quit":
        save_game()
        print("Game saved. Goodbye!")
        break
    
    else:
        print("Unknown command.")
