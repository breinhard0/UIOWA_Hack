import pandas as pd
from taipy import Gui

def get_data(path_to_csv: str):
    # pandas.read_csv() returns a pd.DataFrame
    dataset = pd.read_csv(path_to_csv)
    dataset["Date"] = pd.to_datetime(dataset["Date"])
    return dataset

# Read the dataframe
path_to_csv = "dataset.csv"
dataset = get_data(path_to_csv)




dataset = get_data(path_to_csv)

# Initial value
n_week = 10

# Definition of the page
page = """
# 3D Printing Data

Week number: *<|{n_week}|>*

Interact with this slider to change the week number:

<|{n_week}|slider|min=1|max=52|>

## Dataset:

Display the last three months of data:
<|{dataset[9000:]}|chart|type=bar|x=Date|y=Value|>

<|{dataset}|table|width=100%|>
"""

# Create a Gui object with our page content
Gui(page=page).run(dark_mode=True)