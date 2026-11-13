# README template for `data/XX/README.md`

Replace everything in `<angle brackets>`. Drop sections that don't apply; don't pad. The tone is plain expository prose for an economics audience. Cite with inline links: `Author/Agency, "[Title](url)," date or "accessed Mon. DD, YYYY."` Repo links use `https://github.com/OpenSourceEcon/DataCenterAtlas/blob/main/...`, with spaces encoded as `%20`.

---

```markdown
# <State name> data
<One or two sentences: number of counties/county-equivalents and any special geography (independent cities, parishes, consolidated city-counties).>

<Which jurisdictions levy property tax (state? county, municipal, school, special districts) and which is usually the largest piece.>

<Assessment: ratio for commercial/industrial vs. residential property, whether it's uniform statewide, any caps on assessed value growth, and residential exemptions (homestead, circuit breakers). Cite the official source.>

<Business tangible personal property: is data center equipment (servers, networking, cooling, electrical) taxable, and how is it depreciated? Cite.>

<Data center incentives: statewide or common local property tax abatements and exemptions, with eligibility requirements. Note that these are NOT reflected in the county rates and that users can capture them with the exemption slider in the [DataCenterAtlas.org](https://www.datacenteratlas.org/) web tool.>

## Data and method
<Source agency, report/table title with official link, access date, and repo link to the saved copy:>
"[<Report title>](<official url>)," <Agency>, <date> (accessed <Mon. DD, YYYY>). We have also saved this file as [`/data/XX/<file>`](https://github.com/OpenSourceEcon/DataCenterAtlas/blob/main/data/XX/<file-url-encoded>) in the open source GitHub repository for the [DataCenterAtlas.org](https://www.datacenteratlas.org/) web tool.

<If extracted from a PDF: how, and where the extracted CSV is saved.>

<Exactly which sheet/table/column/rows are used and what the variable means (numerator and denominator).>

<Equation(s), e.g.:>

$$
\tau_{avg,eff,j} = \frac{\sum_i L_{i,j}}{\sum_i FMV_{i,j}} \quad\text{for all}\quad j
$$

<Any conversion from assessed to market value, with the equation and the source of each ratio.>

Our code for calculating the average effective property tax rates by county in <State> for <year> is in the [`/code/XX/xx_analyses.py`](https://github.com/OpenSourceEcon/DataCenterAtlas/blob/main/code/XX/xx_analyses.py) file. The resulting data are saved as [`/data/XX/cnty_prop_tax_rates_xx_YYYY.csv`](https://github.com/OpenSourceEcon/DataCenterAtlas/blob/main/data/XX/cnty_prop_tax_rates_xx_YYYY.csv) in the open source GitHub repository for the [DataCenterAtlas.org](https://www.datacenteratlas.org/) web tool.

<Caveats: direction of bias relative to the rate a new data center would face (e.g., residential relief → understates the commercial rate; value caps → assessed value lags FMV), and any weighting limitation.>

## What we did not use
<Each alternative source or method considered, why it was rejected (no geography to tell which rates stack, assessed-value denominator, implausible results, etc.), with links.>
```
