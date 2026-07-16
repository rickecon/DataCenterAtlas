"""
Code for replicating analyses for New York (NY) in DataCenterAtlas.org
"""
# %%
# Import packages
import numpy as np
import pandas as pd
import os
from pathlib import Path
import geopandas as gpd
import matplotlib.pyplot as plt

# %%
# Set up some directory paths
proj_dir = Path(__file__).resolve().parent.parent.parent
data_dir = os.path.join(proj_dir, "data", "NY")
images_dir = os.path.join(proj_dir, "images", "NY")

# %%
# Import NY OSC tax tables spreadsheet as Pandas DataFrame
county_df = pd.read_excel(
    os.path.join(data_dir, "2025-local-governments.xlsx"), header=3,
    sheet_name="County", nrows=62, usecols="A:H",
    names=[
        "muni_code", "cnty_name", "cnty_levy", "cnty_dist_levy",
        "adj_cnty_levy", "tot_cnty_levy", "cnty_txbl_full_val",
        "full_val_tax_rate_mills"
    ],
    dtype={
        "muni_code": str, "cnty_name": str, "cnty_levy": np.float32,
        "cnty_dist_levy": np.float32, "adj_cnty_levy": np.float32,
        "tot_cnty_levy": np.float32, "cnty_txbl_full_val": np.float32,
        "full_val_tax_rate_mills": np.float32
    }
)

# For each element of the "cnty_name" column, remove the leading "County of "
# string
county_df["cnty_name"] = county_df["cnty_name"].str.replace(
    "County of ", "", regex=True
)

# Add in the five borough counties of New York City (Bronx, Kings, New York,
# Queens, and Richmond) as the full value tax rate from the New York City row
# of the "City" tab of the spreadsheet.

county_df = pd.concat(
    [
        county_df, pd.DataFrame({
            "muni_code": [
                "360050000000", "360470000000", "360610000000", "360810000000",
                "360850000000"
            ],
            "cnty_name": ["Bronx", "Kings", "New York", "Queens", "Richmond"],
            "cnty_levy": [np.nan] * 5,
            "cnty_dist_levy": [np.nan] * 5,
            "adj_cnty_levy": [np.nan] * 5,
            "tot_cnty_levy": [35_311_506_311] * 5,
            "cnty_txbl_full_val": [1_372_240_521_541] * 5,
            "full_val_tax_rate_mills": [25.7327383623287] * 5
        })
    ], ignore_index=True
)

# Sort the DataFrame alphabetically by the "cnty_name" column
county_df = county_df.sort_values(by="cnty_name").reset_index(drop=True)

# Generate average effective property tax rate and percentage variables
county_df["avg_eff_prop_tax_rate"] = (
    county_df["full_val_tax_rate_mills"] / 1_000
)
county_df["avg_eff_prop_tax_pct"] = (
    county_df["avg_eff_prop_tax_rate"] * 100
)

print("DETAILS FOR county_df")
print(county_df.dtypes)
print(county_df.keys())
print(county_df.head(20))
print(county_df.tail(20))
print(county_df.describe())

# Save this DataFrame as a csv file cnty_prop_tax_rates_ny_2025.csv in the
# data/NY directory
county_df.to_csv(
    os.path.join(data_dir, "cnty_prop_tax_rates_ny_2025.csv"), index=False
)
