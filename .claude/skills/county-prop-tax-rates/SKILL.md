---
name: county-prop-tax-rates
description: Build a state's average effective property tax rates by county for DataCenterAtlas.org — the `data/XX/cnty_prop_tax_rates_xx_YYYY.csv` file, plus the raw source data, the `code/XX/xx_analyses.py` script that generates it, and the `data/XX/README.md` that documents it. Use when asked to add a new US state, finish a partially done state, or update a state to a newer data year.
---

# County average effective property tax rates for a US state

DataCenterAtlas.org estimates the property tax revenue a data center would generate in each US county. The key input is the **average effective property tax rate by county**: the tax liability per dollar of **fair market value (FMV)** that a commercial property, ideally a data center, pays in that county.

$$
\tau_{avg,eff,j} = \frac{\sum_i L_{i,j}}{\sum_i FMV_{i,j}}
$$

$L_{i,j}$ is the total tax levied on property $i$ in county $j$ by **every** overlapping jurisdiction: state levy (if any), county, municipal/town, school district, and special districts. $FMV_{i,j}$ is the property's market value, **not** its assessed or taxable value.

Each state needs four deliverables:

| # | Deliverable | Path |
|---|---|---|
| 1 | Raw source file(s), saved unmodified | `data/XX/<original filename>` |
| 2 | Analysis script that reads only the files in (1) and writes (3) | `code/XX/xx_analyses.py` |
| 3 | Output CSV | `data/XX/cnty_prop_tax_rates_xx_YYYY.csv` |
| 4 | Documentation | `data/XX/README.md` |

`XX` is the uppercase two-letter USPS abbreviation (folder names) and `xx` is lowercase (filenames).

## Before you start

1. Read [references/state-precedents.md](references/state-precedents.md). It summarizes how each finished state was done. The precedent closest to your state's data is usually the best template.
2. Check the current status. Don't rely on memory or on the precedents file:
   ```bash
   ls data/*/cnty_prop_tax_rates_*.csv      # finished states
   ls data/XX/ code/XX/ 2>/dev/null         # any partial work for your state
   ```
   If `data/XX/README.md` already exists, read it first. The user may already have chosen a source and method (for example, FL has a chosen source and README but no code or output yet). Build on that work; don't replace it without asking.
3. Read at least two finished states end to end, README plus code. Pick one with a similar method; for most states that means GA or TX (levy ÷ value) and WA or OR (published rate).

## Step 1: Research the state's property tax system

Answer these before choosing a source. The answers go in the README.

- **Assessment ratio.** What share of FMV is taxable for commercial/industrial property, and for residential? Is it uniform statewide or set locally? Examples: GA uses 40% for all property, NV uses 35% of "taxable value", NY's level of assessment varies by town, and UT taxes commercial property at 100% and residential at 55%.
- **Value caps.** Are there caps on assessed value growth (CA Prop 13, OR Measures 5 and 50, TX homestead and circuit breaker caps)? Caps push assessed value below FMV, mostly for long-held residential property.
- **Business tangible personal property (TPP).** Are servers, networking, cooling, and electrical equipment taxable? Equipment is most of a data center's value, so this matters a lot. Say so explicitly in the README.
- **State-level levy.** Is there a state property tax that must be added (for example VT, KS, AL, or WA's state school levy)?
- **Residential relief.** Homestead exemptions, circuit breakers, and similar relief lower effective rates on homes but not on commercial property.
- **Data center incentives.** Are there statewide data center property tax abatements or exemptions, or common local ones (NV abatements, OR Enterprise Zones, ME BETE and LD 713)? Describe them in the README; don't bake them into the rate.
- **County count and equivalents.** How many counties or county-equivalents does the Census use? Watch for independent cities (VA, MD's Baltimore City, MO's St. Louis City, NV's Carson City), parishes (LA), boroughs and census areas (AK), consolidated city-counties (NYC's five boroughs), and states with no county government (CT, RI).

Prefer **official sources**: state Department of Revenue or Taxation, Comptroller, Board of Equalization, State Tax Commission, or Office of the State Comptroller. Their annual property tax statistics reports usually hold the table you need. Record each URL and your access date.

## Step 2: Choose a method (use the highest tier the data supports)

| Tier | Method | When to use | Precedents |
|---|---|---|---|
| **A** | **Use a published county effective or full-value rate**: levies ÷ market value (or ÷ a value close to market) computed by the state | The state publishes it, and its denominator is at or near FMV | CA (avg tax rate on net taxable value), WA (levy ÷ value, Table 27), OR (rate on Measure 5 value, *not* net assessed value), NY (OSC full-value tax rate), ID (overall avg rate on levied amounts) |
| **B** | **Compute Σ levies ÷ Σ value by county**, converting assessed value to FMV with the assessment ratio and exemption mix | The state publishes county levy totals and county taxable/assessed values separately | GA (levies ÷ 40%-assessed value, adjusted for residential homestead share), TX (sum of county + school + city + special district calculated levies ÷ county taxable value) |
| **C** | **Total millage by county ÷ 1000** | The state publishes one combined (all-jurisdiction) millage per county and assessment is at 100% of FMV | FL |
| **D** | **Equal-weighted average of combined statutory rates across tax areas in the county** | Only tax-area or municipality rate tables exist | UT (tax areas), NC (municipalities; uses the *statutory* combined rate, because the effective-rate discount mostly reflects residential reassessment lag) |
| **E** | **Third-party county effective rates** (Property Tax Explorer / Tax Foundation) | Only when official data yield implausible results; explain why in the README | NV |

Rules that come from the precedents:

- **Denominator must be at or near market value.** If the source divides by assessed value, convert to FMV: `FMV = AssessedValue / assessment_ratio`, adjusted for exemptions (see GA and the NV alternative). If a state publishes several bases, pick the one closest to real market value (OR: use the M5V-based rate, not the NAV-based one).
- **Count every overlapping jurisdiction.** A county-government-only rate is far too low. School districts are often the biggest piece.
- **Don't sum overlapping district rates without boundaries.** If you can't tell which rates stack and which are alternatives (GA millage PDF, TX total-rates file), don't use that file. Mention it in a "What we did not use" section.
- **Pick a single taxable-value base per county when combining files.** TX divides by the county unit's taxable value; it does not sum taxable values across overlapping units.
- **Make residential bias explicit.** Effective rates computed over all property usually *understate* the commercial rate (homestead exemptions, caps, slow reassessment). Prefer measures that strip out residential relief, and state the direction of bias in the README.
- **Don't adjust for data-center-specific incentives.** The web tool has an exemption slider for that. Document the incentives instead.

If no tier fits cleanly, or two tiers give materially different answers (more than about 20% apart for many counties), **stop and ask the user** which to use. Show a few sample counties under each method.

## Step 3: Get the raw data

- Save each source file **unmodified** in `data/XX/` under its original filename (spaces are fine; GA, ME, and OR do this). Prefer the Excel or CSV release over the PDF when both exist.
- **PDF-only sources:** extract the table to a CSV in `data/XX/` named after the source (for example `EPB00129_12-04-2025.csv` for ID, or `county_tot_levies_ga_2025.csv`). Keep the PDF too. Check the extraction by comparing several rows and any printed totals against the PDF. Record in the README and the script header how you extracted it.
- **Hard-coded numbers** (NV style) are allowed only when the source is a web page with no downloadable file. Put the source URL and access date in a comment directly above the numbers.
- Note the data year. **`YYYY` in the filename is the most recent tax year the data cover.** For a fiscal year spanning two calendar years (for example FY 2024-25), use the year it ends (OR uses `2025` for FY 2024-25). For "taxes due in YYYY" data (WA), use YYYY. Use the newest year published. If the newest year is incomplete or preliminary, ask the user.

## Step 4: Write `code/XX/xx_analyses.py`

Start from [templates/xx_analyses.py](templates/xx_analyses.py) and follow the conventions of the existing scripts:

- A docstring header: `"""Code for replicating analyses for <State> (XX) in DataCenterAtlas.org"""`.
- `# %%` cell separators, so the file runs as a script or interactively in VS Code.
- Build paths from `Path(__file__).resolve().parent.parent.parent`. Never hard-code absolute paths.
- Pass explicit `names=`, `usecols=`, `header=`/`skiprows=`, `nrows=`, `sheet_name=`, and `dtype=` to `pd.read_excel`/`pd.read_csv`. Comment why a given `nrows` drops trailing rows (statewide totals, prior years).
- Fix county name typos with explicit `.replace()` calls, one per known problem (see GA).
- `print()` diagnostic blocks (dtypes, keys, head, tail, describe) after each major DataFrame.
- `assert` that merges are one-to-one and produce no NaNs.
- Plain pandas/numpy only. Don't add dependencies to `pyproject.toml` without asking.

Run it from the repo root:

```bash
uv run python code/XX/xx_analyses.py
```

## Step 5: Output CSV contract

`data/XX/cnty_prop_tax_rates_xx_YYYY.csv`, written with `index=False`.

**Columns, in this order:**

1. `county_name` (string). Census county name **without** the "County"/"Parish"/"Borough" suffix, in Census capitalization (`DeKalb`, `McDuffie`, `St. Louis`, `Carson City`). Independent cities keep "city" where the Census name needs it to be unique (for example `Baltimore city` vs `Baltimore`).
2. *(Optional)* `county_fips` (string, 5 digits, zero-padded, e.g. `"06001"`). Include it when you can. It makes joining to maps reliable.
3. **Intermediate inputs** used to compute the rate, with descriptive snake_case names: levies, taxable/assessed values, FMV, mill rates, and so on (for example `tot_levies`, `tot_assess_val`, `fmv_prop_val`, `full_val_tax_rate_mills`). Keep them so the result can be audited.
4. `avg_eff_prop_tax_rate`: decimal fraction (0.0123 = 1.23%).
5. `avg_eff_prop_tax_pct`: percentage, exactly `avg_eff_prop_tax_rate * 100`.

The last two columns are required and named exactly as shown, **with no year suffix**; the year is in the filename. Older states differ (`county`, `cnty_name`, `_2025` suffixes, TX's `avg_eff_prop_tax_rate_pct`). Don't copy those variants into new states, and don't rename columns in finished states unless the user asks.

**Rows:** exactly one per county or county-equivalent, sorted alphabetically by `county_name`. No statewide total, average, or blank rows.

## Step 6: Validate before reporting

Write and run these checks (in the script or ad hoc):

- [ ] Row count equals the state's Census county count, with no duplicate `county_name` values.
- [ ] No NaN, zero, or negative rates.
- [ ] `avg_eff_prop_tax_pct == avg_eff_prop_tax_rate * 100`.
- [ ] Rates are plausible: nearly all US county effective rates fall between **0.2% and 3.5%**. Investigate anything outside that range and explain it if it's real.
- [ ] Units are right: mills ÷ 1000, percent ÷ 100. A rate of 12.0 or 0.00012 is a units bug.
- [ ] Print the 5 highest and 5 lowest counties. Check that the ranking makes sense (urban and high-service counties usually rank higher).
- [ ] Compare the statewide median or mean with a published statewide figure (the state report, or the Tax Foundation's state effective rate). Explain any large gap.
- [ ] Re-running the script from a clean checkout reproduces the CSV byte for byte.

## Step 7: Write `data/XX/README.md`

Follow [references/readme-template.md](references/readme-template.md). Minimum content:

- The state's property tax structure (Step 1 answers), with cited links and access dates.
- The exact source file(s): official URL **and** repo URL in the form `https://github.com/OpenSourceEcon/DataCenterAtlas/blob/main/data/XX/<file>` (URL-encode spaces as `%20`).
- The method, with the tier and the equation(s) in `$$ ... $$` LaTeX, naming the specific variables, columns, or tables used.
- Links to `code/XX/xx_analyses.py` and the output CSV.
- Caveats: direction of bias, weighting limitations, treatment of TPP, data center incentives.
- A "What we did not use" or "Alternative method" section for sources you considered and rejected, with the reason.

## Step 8: Report back to the user

Summarize: the source and year, the tier and why, the county count, the min/median/max rate with county names, the statewide comparison, and any judgment calls or open questions. **Don't commit or push** unless the user asks. When they do, the repo convention is a feature branch per state (for example `git checkout -b ky`) and a PR to `main`.

## Updating a finished state to a newer year

Download the new source file next to the old one (don't overwrite it). Update the filename, `nrows`, and column letters in the script. Generate the new-year CSV and keep the old one. Update the README links, years, and access dates. Diff the old and new rates and flag any county that moved more than about 0.3 percentage points.
