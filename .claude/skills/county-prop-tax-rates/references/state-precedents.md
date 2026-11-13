# State precedents

How each state already in the repo was handled. Each state's `data/XX/README.md` and `code/XX/*.py` are the authoritative versions; this is a quick index for choosing a template. Status as of Nov. 2026. Re-check with `ls data/*/cnty_prop_tax_rates_*.csv`.

## Finished: `cnty_prop_tax_rates_xx_YYYY.csv` exists

### CA: Tier A (published average tax rate)
- **Source:** CA Board of Equalization, "Property Tax Allocations (Table 14, 15)", `PropTaxGenPropTaxLevies.csv`.
- **Method:** Uses the "Average Tax Rate" column (total levies of county, city, school, and special districts ÷ net taxable assessed value). Reads only the first 58 rows, because later rows are prior years. The published value is a percent, so ÷100.
- **Notes:** Prop 13 (1% base rate, at most 2% annual growth in assessed value until sale) means assessed value lags FMV for long-held property, so the rate is a lower bound for new data centers, which are assessed at near-FMV.
- **Output columns:** `county, net_txbl_assessed_val, tot_prop_tax_alloc_levies, avg_eff_prop_tax_rate, avg_eff_prop_tax_pct`.

### GA: Tier B (levies ÷ assessed value converted to FMV)
- **Sources:** GA DOR "2025 Summary of Ad Valorem Taxes Levied Report.pdf" (county total levies, extracted to `county_tot_levies_ga_2025.csv`) and "Digest Export 4.6.26.xlsx" (rows with District Code 0 give the county "Total Assessed Value – M&O").
- **Method:** All property is assessed at 40% of FMV. The README assumes about 60% of value is residential, where the homestead exemption cuts the effective ratio to 39%: `FMV = 0.6·TAV/0.39 + 0.4·TAV/0.40`, then rate = levies ÷ FMV. The output also keeps the unadjusted `avg_prop_tax_rate` (levies ÷ assessed value).
- **Gotchas:** County names in the digest have typos (`ATKINS`, `HEARD KA`, `WHEELE`) and need title-casing with exceptions (`DeKalb`, `McDuffie`, `McIntosh`). The script asserts names match after the merge.
- **Rejected:** The millage-rate PDF, because it's unclear which rates stack and there are no weights.

### ID: Tier A (published overall average rate)
- **Source:** ID State Tax Commission, Chart VIII "2025 Average Property Tax Rates Based on Levied Amounts" (EPB00129 PDF), extracted to `EPB00129_12-04-2025.csv`.
- **Method:** Uses the overall (not urban or rural) average rate. Commercial property is assessed at 100% of market value; residential gets a homeowner's exemption (50%, capped at $125k).
- **Output columns:** keeps the urban and rural rates as intermediate columns.

### NV: Tier E (third-party rates; official route rejected)
- **Source used:** Property Tax Explorer / Tax Foundation county effective rates, hard-coded in the script with the URL.
- **Why:** Assessed value is 35% of "taxable value", which isn't FMV. Statewide data center abatements (up to 75% of personal property tax) and capped growth in assessed value make an official-data calculation unreliable.
- **Alternative kept in the script but unused:** FY26 total allowed ad valorem revenue ÷ (assessed value after exemptions × statewide before/after-exemption ratio ÷ 0.35). It gave implausible rates.
- **Lesson:** If the official computation gives implausible numbers, document the attempt and the fallback in the README.

### NY: Tier A (OSC full-value tax rate) plus a NYC special case
- **Source:** NY Office of the State Comptroller, `2025-local-governments.xlsx`, "County" tab, full value tax rate (mills, adjusted for payments between counties and their local governments).
- **Method:** mills ÷ 1000. The five NYC borough counties (Bronx, Kings, New York, Queens, Richmond) aren't on the County tab, so all five get the City of New York full-value rate from the "City" tab.
- **Gotchas:** Strip the `"County of "` prefix. Level of assessment varies by town (0–100%), which is why a full-value (equalized) measure is required.

### OR: Tier A (rate on the base closest to market value)
- **Source:** OR DOR "FY 2024-25 Property Tax Statistics Detail Tables.xlsx", Table 1.6 (sheet `1.6`).
- **Method:** Uses "Average Tax Rate ($ per 1000) M5V Base", ÷1000. M5V (Measure 5 value) is close to real market value. **Not** the NAV-based rate, because Measure 50 caps NAV growth at 3% a year, so NAV sits far below market value.
- **Year:** FY 2024-25 is labeled `2025`.

### TX: Tier B (sum of levies across unit types ÷ county taxable value)
- **Sources:** TX Comptroller 2025 rates and levies workbooks for counties, school districts, cities, and special districts (four files).
- **Method:** Sum the `calculated_levy` column in all four files by `county_id`, then divide by the county unit's taxable value. Cities and special districts missing from a county are filled with 0.
- **Gotchas:** Strip the `" *"` flag from county names (e.g., `Culberson *`). County IDs 001–254 are alphabetical, and FIPS = 48000 + 2·id − 1.
- **Rejected:** The total-rates file (no geography to tell which rates stack).

### WA: Tier A (published levy ÷ value)
- **Source:** WA DOR "Property Tax Statistics 2025", `Table_27_2025.xlsx`, sheet "Effective Rates", column P (percent). The first 39 rows are counties; the statewide row is dropped.
- **Notes:** County assessment ratios run 75–96%, so a published levy ÷ value table is preferred over raw levy rates per $1,000 of assessed value.

## Partial work: build on it and read the README first

| State | What exists | What's missing / notes |
|---|---|---|
| **FL** | `README.md` chooses Tier C: DOR `millage_taxes_levied.xlsx`, "Millage Rates" sheet, total millage by county ÷ 1000. Assessment at 100% of FMV, TPP taxed. | `code/FL/fl_analyses.py` and the output CSV. |
| **ME** | `ME_FullValuePropTaxRates_cnty_2024.csv` (full-value rates by county, with title and source rows above and below the data), the source `.xls`, README. No code. | Script producing `cnty_prop_tax_rates_me_2024.csv` in the standard format from the `.xls`. README discusses BETE and LD 713, which removed data centers from BETE in 2026. |
| **NC** | `nc_analyses.py` → `avg_proptax_rate_by_cnty_nc_2025_2026.csv` (`cnty_name, rate_cnty_avg`), Tier D on combined statutory municipal rates. | Standard-format `cnty_prop_tax_rates_nc_YYYY.csv`. The equal weighting includes the county's unincorporated row. Ask the user before changing the method. |
| **UT** | `ut_analyses.py` → `avg_proptax_rate_by_cnty_ut_2025.csv`, Tier D on tax areas (`rates_ut_2025.csv` extracted from the PDF). | Standard-format `cnty_prop_tax_rates_ut_2025.csv`. Note that the UT script **rewrites its own input CSV**; don't copy that pattern. |
| **MT** | README stub only (no state levy for local purposes). | Everything. |
| **LA** | README stub only (64 parishes). | Everything. Use parish names without the "Parish" suffix. |

## Non-county special cases in other states

- **AK:** Boroughs and census areas, and large unorganized areas with no local property tax. Use the Census county-equivalents. An unorganized area may legitimately have a rate near 0; document it.
- **CT:** No county government. The Census switched from 8 counties to 9 planning regions in 2022. Property tax is levied by 169 towns (the OPM publishes equalized mill rates by town). Ask the user whether to aggregate to the legacy counties or to the planning regions, and which weights to use (e.g., equalized net grand list).
- **RI:** No county government. Towns levy the tax. Aggregate the 39 municipalities to the 5 counties.
- **MA:** Several counties have no government. Municipal rates are published by the DLS. Aggregate municipalities to counties.
- **VA:** 95 counties plus 38 independent cities, all county-equivalents. Every independent city needs its own row. VA also has significant local data center incentives and a separate business TPP (computer equipment) rate. Document both.
- **HI:** 4 counties levy by property class (commercial and industrial rates differ from residential). Use the commercial or industrial class rate, and treat Kalawao County specially.
- **MD:** 23 counties plus Baltimore City.
- **MO:** 114 counties plus St. Louis City.
