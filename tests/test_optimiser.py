from battery_optimiser import battery_optimiser

def test_basic_example_with_defaults():
    prices = [3,6,2,5]
    schedule, profit = battery_optimiser(prices)
    assert profit == 9.854999999999999

def test_soc_does_not_exceed_max_storage_volume():
    prices = [361, -18, 159, 352, 220, 101, 49, 330, 337, 21, 226, 302, 87, 137, 356, 486, 210, 27, -40]
    schedule, profit = battery_optimiser(prices)
    assert all(schedule["soc"] <= 4.0)

def test_no_profit_with_flat_prices():
    prices = [50]*20
    schedule, profit = battery_optimiser(prices)
    assert profit == 0