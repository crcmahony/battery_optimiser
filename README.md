# Battery Optimiser

A Python package that finds the profit-maximising charge/discharge schedule for a battery given hourly electricity prices.

The optimiser uses linear programming (PuLP with CBC solver) to determine when to charge (buy cheap) and discharge (sell expensive), subject to the battery's physical constraints.

## Installation

Requires Python 3.12+.

```bash
git clone 
cd battery_optimiser
pip install -e .
```

## Quick Start

```python
from battery_optimiser import load_prices_from_excel, battery_optimiser

hourly_prices = load_prices_from_excel("data/prices_example.xlsx", "Hourly data")
result = battery_optimiser(hourly_prices)

print(result)
```
For further details see example.py.

## Battery Parameters

The optimiser uses the following default parameters, which can be adjusted:

| Parameter              | Default | Unit | Description                                                                          |
|------------------------|---------|------|--------------------------------------------------------------------------------------|
| max_charging_rate      | 2.0     | MW   | The maximum power that the battery can import from the grid                          |
| max_discharging_rate   | 2.0     | MW   | The maximum power that the battery can export to the grid                            |
| max_storage_volume     | 4.0     | MWh  | Maximum volume of energy that the battery can store                                  |
| charging_efficiency    | 0.05    | -    | Fraction of energy imported from grid that is lost prior to storage in the battery   |
| discharging_efficiency | 0.05    | -    | Fraction of energy exported from the battery that is lost prior to reaching the grid |
| initial_soc            | 0.0     | MWh  | State of charge at the start of the battery schedule                                 |

## Input Data

The package expects an Excel file with a `datetime` column and a `price` column (£/MWh). Prices should be hourly. Example data can be found in data/prices_example.xlsx

## Running Tests

```bash
pip install pytest
pytest
```
## How It Works

The optimiser formulates the problem as a linear program (LP):

**Objective:** maximise total profit (earnings from discharging minus
cost of charging), accounting for efficiency losses.

**Decision variables:** for each hour, how much to charge, how much
to discharge, and the resulting state of charge.

**Constraints:**
- Charge and discharge rates cannot exceed the battery's maxima
- State of charge must stay between 0 and the battery's maximum storage volume
- Next state of charge is dependent on the previous state of charge, energy conservation.

The LP is solved using PuLP with the CBC solver.

## Possible Extensions

- Half-hourly prices
- Add second market
- Additional battery behaviours such as, degradation, lifetime, operational costs
- Module for visualising the schedule

## Summary of approach

I approached this task by first simplifying the problem, to aid my understanding and make it tractable in the time available. I used one market with hourly prices, and a core set of battery parameters. I initially worked through the problem in a jupyter notebook, which I have included in the repository to show my working (first_draft_of_battery_optimisation.ipynb). I used linear programming because the objective and constraints are all linear, and decided to use PuLP with the CBC solver as it was very readable and didn’t require any configuration. Once I had some basic functions I converted them into an installable Python package, with separate modules for loading data and optimisation, using pyproject.toml. Given more time I would add an additional module for visualising the results. I then added some reproducible tests that can be run with pytest. Finally, I created a readme to explain the package and also checked that I could install and run the package on a different laptop. 