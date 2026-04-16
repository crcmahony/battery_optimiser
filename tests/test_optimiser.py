from battery_optimiser import battery_optimiser

def test_basic_example_with_defaults():
    prices = [3,6,2,5]
    schedule, profit = battery_optimiser(prices)
    assert profit == 9.854999999999999