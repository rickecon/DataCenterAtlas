# New York data
New York has no state property tax rate. New York property taxes are levied by county, city, town, village, municipal, school districts, and special taxing district authorities. School districts are typically the  largest component of a New York property tax bill.

Assesment is done locally, usually by the town/city assessors. Assessed values reflect a locality's chosen level of assessment relative to market value, whyc varies significantly across the state. For this reason, New York publishes equilization rates to make assessments comparable across jurisdictions.

Data centers in New York are generally taxed under the same real property tax rules as other commercial and industrial property. However, because data centers are extremely capital intensive, serveral aspects of New York law are particularly important.

As mentioned above, assessment ratios (called level of assessment or LOA in New York) vary across New York local jurisdictions, usually cities or towns. Table 5 from New York State Department of Taxation and Finance ["Assessment Equity in New York: Results from the 2025 Market Value Survey"](https://www.tax.ny.gov/research/property/reports/cod/2025mvs/reporttext.htm) shows that levels of assessment across jurisdictions in New York in 2025 ranged widely.

Table 5. Level of assessment, as measured by 2025 State equalization rate
| Level of assessment | Number of assessing units | Percent of assessing units |
| :--- | ---: | ---: |
| 0.00 - 10.00  | 57 | 5.8% |
| 10.01 - 25.00 | 36 | 3.7%
| 25.01 - 50.00 | 177 | 18.0% |
| 50.01 - 75.00 | 347 | 35.3% |
| 75.01 - 100.00 | 365 | 37.2% |
| Greater than 100.00 | 0 | 0.0% |
| TOTAL | 982 | 100.0% |

Total property tax liability is equal to the market rate times the assessment ratio times the total (cumulative) property tax rate.

$$
\text{Total prop. tax liability}_i \: = \: FMV_i \quad\times\quad \text{AssessRatio}_j \quad\times\quad \text{CumPropTaxRate}_j
$$

The State of New York has 62 counties. The 5 counties of Bronx, Kings, New York, Queens, and Richmond are equivalent to the five boroughs of New York, with New York County being the Manhattan borough, Kings County being the Brooklyn borough, and Richmond County being the Staten Island borough.

The New York Office of the Swtate Comptroller (OSC) publishes the ["OSC Real Property Tax Levies, Taxable Full Value and Full Value Tax Rates"](https://www.osc.ny.gov/local-government/data/real-property-tax-levies-taxable-full-value-and-full-value-tax-rates) spreadsheet of annual tax tables. We have also included this spreadsheet in the [`/data/NY/2025-local-governments.xlsx`](https://github.com/OpenSourceEcon/DataCenterAtlas/blob/main/data/NY/2025-local-governments.xlsx) path of the open source GitHub repository for the [DataCenterAtlas.org](https://www.datacenteratlas.org/) web tool. The "County" tab of this spreadsheet includes the county full value tax rate.

> The county full value tax rate that is presented in the table has been adjusted to reflect the various payments and credits made between counties and their component local governments. It reflects the most accurate depiction of overall property tax burden at the county level and is comparable from one county to the next (see [Data Description document](https://www.osc.ny.gov/files/local-government/data/pdf/datadescription2015.pdf) for OSC data file).

For our average effective property tax rates by county, we use the full value tax rate variable in the last column of the "County" tab of the spreadsheet [`/data/NY/2025-local-governments.xlsx`](https://github.com/OpenSourceEcon/DataCenterAtlas/blob/main/data/NY/2025-local-governments.xlsx). For the five counties associated with the five boroughs (Bronx, Kings, New York, Queens, and Richmond), we use the "City" tab average effective property tax rate from the "Full Value Tax Rate" column for the City of New York City row. The code for gathering these data from the spreadsheet is available in the [`/code/NY/ny_analyses.py`](https://github.com/OpenSourceEcon/DataCenterAtlas/blob/main/code/NY/ny_analyses.py) file in the open source GitHub repository for the [DataCenterAtlas.org](https://www.datacenteratlas.org/) web tool. The average effective property tax rate data from this computation is stored as [`/data/NY/cnty_prop_tax_rates_ny_2025.csv`](https://github.com/OpenSourceEcon/DataCenterAtlas/blob/main/data/NY/cnty_prop_tax_rates_ny_2025.csv) in the open source GitHub repository for the [DataCenterAtlas.org](https://www.datacenteratlas.org/) web tool.
