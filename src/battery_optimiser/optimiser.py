import pandas as pd
import pulp

def battery_optimiser(hourly_prices, max_charging_rate, max_discharging_rate, max_storage_volume, charging_efficiency, discharging_efficiency, initial_soc, solver=pulp.PULP_CBC_CMD(msg=0)):
    
    model = pulp.LpProblem("battery_optimisation", pulp.LpMaximize)
    
    n_hours = len(hourly_prices)
    charge = pulp.LpVariable.dicts("charge", range(n_hours), 0, max_charging_rate)
    discharge = pulp.LpVariable.dicts("discharge", range(n_hours), 0, max_discharging_rate)
    soc = pulp.LpVariable.dicts("soc", range(n_hours), 0, max_storage_volume)
   
    model += pulp.lpSum(hourly_prices[t] * discharge[t] * (1 - discharging_efficiency) - hourly_prices[t] * charge[t] for t in range(n_hours))
    
    for t in range(n_hours):
        previous_soc = initial_soc if t == 0 else soc[t - 1]
        model += soc[t] == previous_soc + charge[t] * (1 - charging_efficiency) - discharge[t]

    model.solve(solver)

    schedule = pd.DataFrame({"price": hourly_prices,
                             "charge": [charge[t].varValue for t in range(n_hours)],
                             "discharge": [discharge[t].varValue for t in range(n_hours)],
                             "soc": [soc[t].varValue for t in range(n_hours)]})
    
    profit = pulp.value(model.objective)

    return pulp.LpStatus[model.status], schedule, profit