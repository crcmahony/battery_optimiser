from battery_optimiser import load_prices_from_excel, battery_optimiser

hourly_prices = load_prices_from_excel("data/prices_example.xlsx", "Hourly data")

max_charging_rate = 2 #units MW
max_discharging_rate = 2 #units MW
max_storage_volume = 4 #units MWh
charging_efficiency = 0.05 #Fraction of energy imported from grid that is lost prior to storage in the battery
discharging_efficiency = 0.05 #Fraction of energy exported from the battery that is lost prior to reaching the grid
initial_soc = 0.0

result = battery_optimiser(hourly_prices, max_charging_rate, max_discharging_rate, max_storage_volume, charging_efficiency, discharging_efficiency, initial_soc)

print(result)
