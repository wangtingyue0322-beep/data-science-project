# `gss_income.csv` — provenance and reuse terms

## What this file is

A reduced extract of the **General Social Survey (GSS)**, a repeated cross-sectional survey of U.S.
adults run by NORC at the University of Chicago since 1972. One row per respondent; 55,343 rows;
five columns.

| Column | Type | Meaning |
|---|---|---|
| `year` | int | survey year (31 waves, 1972–2016) |
| `educ` | float | years of schooling completed |
| `degree` | int | highest degree: 0 = less than high school, 1 = high school, 2 = junior college, 3 = bachelor's, 4 = graduate |
| `realinc` | float | respondent's **family income in constant dollars**, deflated by the GSS |
| `wtssall` | float | GSS person weight (corrects for subsampling and non-response) |

## How it was produced

The starting point is `gss.hdf5`, the GSS data package distributed with Allen Downey's *ThinkStats2*
course materials. It carries the GSS cumulative file as a single table of 62,466 rows × 101 columns.
The extract applies exactly four steps, in this order:

```python
df = pd.read_hdf("gss.hdf5", "gss")[["year", "educ", "degree", "realinc", "wtssall"]]
df = df[df["degree"].isin([0, 1, 2, 3, 4])]      # drop 8 = don't know, 9 = no answer
df = df[df["realinc"].notna() & (df["realinc"] > 0)]
df = df.dropna(subset=["wtssall", "educ"])
```

62,466 rows → **55,343 rows** (88.6%). Every number in the analysis is computed from this file, and
the notebook in the repository root regenerates all statistics and figures from it.

## Privacy: what was removed and why

The upstream table has 101 columns, including case identifiers and demographic and attitudinal
variables. **All of them were dropped.** The extract keeps only the five variables the analysis
actually uses. The GSS public-use file contains no direct identifiers, but the case number and the
full demographic block are not needed to answer the research question, so they are not redistributed
here. No API keys, credentials or personal data of any kind are present in this repository.

## Reuse terms

GSS data are **public-use data distributed by NORC free of charge for research and teaching**. This
repository redistributes a reduced subset of five variables for the sole purpose of making the
analysis reproducible. The data are not for commercial use, and any publication based on them should
cite the source below and acknowledge NORC.

Because the upstream file (`gss.hdf5`) carries no release metadata, the exact GSS release year of
this snapshot cannot be recovered from the file itself; the access route is recorded instead.

## Citation

> NORC at the University of Chicago. *General Social Survey, 1972–2016 cumulative file* [Data set].
> https://gss.norc.org
>
> Accessed via the `gss.hdf5` data package distributed with A. B. Downey, *Think Stats* (2nd ed.),
> O'Reilly Media.

## Known properties that affect the analysis

* **The income variable is top-coded.** Each survey year caps `realinc` at a single value, and that
  cap absorbs 7–11% of respondents in each period. The analysis trims those observations before
  computing tail statistics; see the notebook, section 2.
* **Income is family income, not equivalised household income.** Households changed size over the
  period, so cross-decade comparisons carry an unquantified bias.
* **Item non-response is not random.** 11.2% of GSS respondents have no valid income value and are
  excluded, which most likely under-represents the poorest and the richest households.
