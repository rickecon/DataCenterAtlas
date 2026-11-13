"""
Code for replicating analyses for <State name> (XX) in DataCenterAtlas.org

Calculates average effective property tax rates by county for <YYYY> from
<agency>, "<report/table title>" (<official URL>), accessed <Mon. DD, YYYY>.
Method: <Tier A/B/C/D/E: one-line description>. See data/XX/README.md.

TEMPLATE NOTES (delete before committing):
- Replace XX/xx/YYYY placeholders. Keep only the cells your method needs.
- Read raw files only from data/XX/. Never overwrite a raw input file.
"""
# %%
# Import packages
import os
from pathlib import Path
import numpy as np
import pandas as pd

# %%
# Set up some directory paths
proj_dir = Path(__file__).resolve().parent.parent.parent
data_dir = os.path.join(proj_dir, "data", "XX")
images_dir = os.path.join(proj_dir, "images", "XX")

DATA_YEAR = YYYY
N_COUNTIES = 0  # Census county/county-equivalent count for XX
OUT_FILE = f"cnty_prop_tax_rates_xx_{DATA_YEAR}.csv"

# %%
# Read the source data. Use explicit header/usecols/nrows/names/dtype so the
# extraction is auditable. Comment why nrows stops where it does (e.g., drop
# the statewide total row at the bottom).
src_df = pd.read_excel(
    os.path.join(data_dir, "<source file>.xlsx"),
    sheet_name="<sheet>",
    header=0,
    usecols="A,B",
    nrows=N_COUNTIES,
    names=["county_name", "<source_var>"],
    dtype={"county_name": str, "<source_var>": np.float64},
)
src_df["county_name"] = src_df["county_name"].str.strip()
# Fix known county-name problems one at a time, e.g.:
# src_df["county_name"] = src_df["county_name"].replace(
#     {"Dekalb": "DeKalb", "Mcduffie": "McDuffie"}
# )
# src_df["county_name"] = src_df["county_name"].str.replace(
#     " County", "", regex=False
# )

print("DETAILS FOR src_df")
print(src_df.dtypes)
print(src_df.keys())
print(src_df.head(10))
print(src_df.tail(10))
print(src_df.describe())

# %%
# Compute the average effective property tax rate. Keep the pattern that
# matches your tier and delete the others.
cnty_df = src_df.copy()

# Tier A: published rate in percent
# cnty_df["avg_eff_prop_tax_rate"] = cnty_df["<rate_pct>"] / 100
# Tier A/C: published rate in mills ($ per $1,000)
# cnty_df["avg_eff_prop_tax_rate"] = cnty_df["<mill_rate>"] / 1_000
# Tier B: levies / fair market value, where FMV is backed out of assessed
# value using the assessment ratio (and exemption mix, if needed)
# ASSESS_RATIO = 1.0
# cnty_df["fmv_prop_val"] = cnty_df["tot_assess_val"] / ASSESS_RATIO
# cnty_df["avg_eff_prop_tax_rate"] = (
#     cnty_df["tot_levies"] / cnty_df["fmv_prop_val"]
# )
# Tier D: equal-weighted mean of combined rates across tax areas
# cnty_df = (
#     area_df.groupby("county_name", as_index=False)["comb_rate"].mean()
#     .rename(columns={"comb_rate": "avg_eff_prop_tax_rate"})
# )

cnty_df["avg_eff_prop_tax_pct"] = cnty_df["avg_eff_prop_tax_rate"] * 100

# Standard column order: county_name, [county_fips], intermediate inputs,
# avg_eff_prop_tax_rate, avg_eff_prop_tax_pct
cnty_df = cnty_df[
    ["county_name", "<source_var>", "avg_eff_prop_tax_rate",
     "avg_eff_prop_tax_pct"]
]
cnty_df = cnty_df.sort_values("county_name").reset_index(drop=True)

# %%
# Validation checks
assert len(cnty_df) == N_COUNTIES, (
    f"Expected {N_COUNTIES} counties, got {len(cnty_df)}"
)
assert not cnty_df["county_name"].duplicated().any(), "Duplicate counties"
assert cnty_df["avg_eff_prop_tax_rate"].notna().all(), "Missing rates"
assert (cnty_df["avg_eff_prop_tax_rate"] > 0).all(), "Non-positive rates"
out_of_range = cnty_df[
    (cnty_df["avg_eff_prop_tax_rate"] < 0.002) |
    (cnty_df["avg_eff_prop_tax_rate"] > 0.035)
]
if len(out_of_range) > 0:
    print("WARNING: counties outside the 0.2%-3.5% plausibility range:")
    print(out_of_range)

print("DETAILS FOR cnty_df")
print(cnty_df.dtypes)
print(cnty_df.describe())
print("Highest 5 counties:")
print(cnty_df.nlargest(5, "avg_eff_prop_tax_rate"))
print("Lowest 5 counties:")
print(cnty_df.nsmallest(5, "avg_eff_prop_tax_rate"))

# %%
# Save this DataFrame as a csv file in the data/XX directory
cnty_df.to_csv(os.path.join(data_dir, OUT_FILE), index=False)
print(f"Wrote data/XX/{OUT_FILE}")

# %%
