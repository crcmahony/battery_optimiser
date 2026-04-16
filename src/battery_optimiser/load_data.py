import pandas as pd

def load_prices_from_excel(filename, sheetname):
    df = pd.read_excel(filename, sheet_name=sheetname, names=["date_time", "price"], index_col="date_time")
    hourly_prices = df["price"].values
    return hourly_prices