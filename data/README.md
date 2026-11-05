# `gss_income.csv` — provenance and reuse notes

## What this file is

A reduced extract of the **General Social Survey (GSS)**, a repeated cross-sectional survey of U.S.
adults conducted by NORC at the University of Chicago. One row per respondent; 55,343 rows; five
columns. The survey year ranges from 1972 to 2016, while the income question refers to the previous
calendar year.

| Column | Type | Meaning |
|---|---|---|
| `year` | int | Survey year (31 waves, 1972–2016) |
| `educ` | float | Years of schooling completed |
| `degree` | int | Highest degree: 0 = less than high school, 1 = high school, 2 = junior college, 3 = bachelor's, 4 = graduate |
| `realinc` | float | Respondent's **family income in constant 1986 U.S. dollars**, deflated by the GSS |
| `wtssall` | float | GSS person weight used for the descriptive estimates |

The constant-dollar definition follows the GSS methodology for `REALINC`. See NORC's
[Methodological Report No. 64](https://gss.norc.org/content/dam/gss/get-documentation/pdf/reports/methodological-reports/MR064.pdf).

## How the extract was produced

The starting point is `gss.hdf5`, the GSS data package distributed with Allen Downey's *Think Stats,
2nd ed.* course materials. It contains 62,466 rows and 101 columns. The extract applies these four
steps, in order:

```python
df = pd.read_hdf("gss.hdf5", "gss")[["year", "educ", "degree", "realinc", "wtssall"]]
df = df[df["degree"].isin([0, 1, 2, 3, 4])]      # drop 8 = don't know, 9 = no answer
df = df[df["realinc"].notna() & (df["realinc"] > 0)]
df = df.dropna(subset=["wtssall", "educ"])
```

62,466 rows → **55,343 rows (88.6%)**. This is the combined result of all validity filters; the
reduced file cannot decompose the excluded 11.4% by reason. Every reported statistic is computed
from this CSV, and the notebook regenerates the results and figures without accessing the upstream
HDF5 file.

## Privacy and data minimisation

The upstream table contains case identifiers and additional demographic and attitudinal variables.
Those columns are not needed for this analysis and were removed. The extract contains no direct
identifiers, credentials, API keys or restricted GSS variables. Only the five analysed variables are
redistributed.

## Reuse and citation

The source is a GSS public-use dataset used for research and teaching. This reduced extract is
included solely to make the course analysis reproducible; it is not presented as a replacement for
the official GSS release. The underlying data remain subject to NORC's terms. Any reuse should cite
NORC and preserve this provenance note.

The upstream HDF5 file carries no release metadata, so its exact release version cannot be recovered
from that file alone. The access route and the 1972–2016 coverage are recorded rather than assigning
an unverified release number.

Recommended source citation:

> Smith, Tom W., Michael Hout, and Peter V. Marsden. *General Social Survey, 1972–2016* [Cumulative
> File]. NORC at the University of Chicago / ICPSR, 2017.
> https://doi.org/10.3886/ICPSR36797.v1
>
> Accessed here through the `gss.hdf5` package distributed with Allen B. Downey, *Think Stats*,
> 2nd ed., O'Reilly Media.

## Properties that affect interpretation

- **Top-coding.** The open-ended upper bracket is assigned a year-specific single value. The
  analysis marks observations at their survey year's maximum and compares four transparent
  specifications: trimmed, ceiling as recorded, ceiling × 1.5 and ceiling × 2. These bounded
  scenarios test the direction of the result; none reveals the unobserved incomes within the top
  bracket.
- **Family income is not equivalised.** Household size is absent, so comparisons do not adjust for
  household needs or changes in household composition.
- **Selection may be non-random.** If the combined validity exclusions are related to income, the
  analytical sample may not represent the full target population.
- **No survey-design variance variables.** Strata and PSU fields are not included, so the project
  reports descriptive estimates rather than design-based confidence intervals.

## Generated validation outputs

Running all notebook cells writes `results/data_quality.csv` with one row per survey year and
records sample size, top-coded count and share, recorded ceiling, unweighted p75 and median, and
minimum income. The notebook asserts that all 31 years have a top-code cluster of at least 20
observations and that each annual ceiling lies above that year's unweighted p75. It also writes
`results/summary_statistics.csv`, `results/education_summary.csv`,
`results/topcode_sensitivity.csv` and `results/environment.txt`; `scripts/validate_results.py`
checks these files without third-party packages.
