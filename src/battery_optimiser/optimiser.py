import pandas as pd
import pulp

def battery_optimiser(hourly_prices, max_charging_rate=2, max_discharging_rate=2, max_storage_volume=4, charging_efficiency=0.05, discharging_efficiency=0.05, initial_soc=0.0, solver=pulp.PULP_CBC_CMD(msg=0)):
    """
    Maximise profit from battery charging and discharging via linear programming.
    
    Returns (schedule DataFrame, total profit).
    Raises RuntimeError if no optimal solution is found 
    """
    model = pulp.LpProblem("battery_optimisation", pulp.LpMaximize)
    
    #Decision variables: charge, discharge, and state of charge each hour
    n_hours = len(hourly_prices)
    charge = pulp.LpVariable.dicts("charge", range(n_hours), 0, max_charging_rate)
    discharge = pulp.LpVariable.dicts("discharge", range(n_hours), 0, max_discharging_rate)
    soc = pulp.LpVariable.dicts("soc", range(n_hours), 0, max_storage_volume)
   
    #Objective: earnings from discharging (after efficiency losses) minus cost of charging
    model += pulp.lpSum(hourly_prices[t] * discharge[t] * (1 - discharging_efficiency) - hourly_prices[t] * charge[t] for t in range(n_hours))
    
    #Constraints: energy conservation at each timestep
    for t in range(n_hours):
        previous_soc = initial_soc if t == 0 else soc[t - 1]
        model += soc[t] == previous_soc + charge[t] * (1 - charging_efficiency) - discharge[t]

    model.solve(solver)

    status = pulp.LpStatus[model.status]
    if status != "Optimal":
        raise RuntimeError(f"Solver didn't find optimal solution. Status:{status}")

    schedule = pd.DataFrame({"price": hourly_prices,
                             "charge": [charge[t].varValue for t in range(n_hours)],
                             "discharge": [discharge[t].varValue for t in range(n_hours)],
                             "soc": [soc[t].varValue for t in range(n_hours)]})
    
    profit = pulp.value(model.objective)

    return schedule, profit