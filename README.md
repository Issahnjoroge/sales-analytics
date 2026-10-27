# Tech Hub Kenya — September 2026 Sales Analytics

## Overview

This project analyses the provided September 2026 electronics sales CSV. The main reporting pipeline (CSV reading, cleaning, aggregation, ranking, filtering, and statistics) uses only Python's standard library. Pandas is imported only inside the optional verification function.

## How to run

Requires Python 3.10 or newer.

```bash
python sales_analysis.py
```

The script prints the report and writes the report body to `output/sales_report.txt`. If pandas is installed, the verification block is printed after the report.

To install pandas on a laptop for verification:

```bash
python -m pip install -r requirements.txt
python sales_analysis.py
```

The production/reporting environment can run the core analysis without pandas. If pandas is absent, the script clearly says verification was skipped.

## Cleaning rules and assumptions

The supplied file has 50 rows. Each row is treated as one transaction. Revenue means `quantity × unit_price_kes`; it is not profit, and no cost-of-goods data was supplied.

`parse_number` applies only these conservative repairs:

1. Strip leading/trailing whitespace.
2. Remove commas used as thousands separators, so `38,999` becomes `38999`.
3. Remove a leading `KES` currency label, so `KES 18999` becomes `18999`.
4. Parse the result as a number and reject non-numeric values, infinities, and NaN.

No attempt is made to guess words such as `two`, `N/A`, or a missing value. The script does not silently invent quantities or prices.

A row is skipped if quantity is blank/non-numeric, non-positive, or not a whole number; or if unit price is blank/non-numeric or non-positive. If more than one field is invalid, all applicable reasons are recorded. Skipped rows are excluded from every revenue calculation. This is preferable to guessing a transaction amount, which could materially distort financial reporting. A business owner could later check the original till receipt and correct the source data.

`KES 18999` and `38,999` are accepted because the currency label and thousands comma are unambiguous in this dataset. Negative and zero quantities/prices are rejected as invalid sales assumptions. Decimal quantities are rejected because these electronics are counted as whole units.

## Analysis choices

- Product, store, and payment totals use a plain dictionary.
- Rankings sort by revenue descending. Ties break alphabetically by product/store/method name, making output deterministic.
- High-value transactions use `revenue >= KES 50,000`, including a transaction exactly on the threshold.
- The high-value count dictionary includes every store represented in the cleaned data, including stores with zero qualifying transactions.
- Mean and median are calculated from the cleaned per-transaction revenue values. For an even number of transactions, the median is the average of the two central sorted values.
- The minimum/maximum function uses a loop rather than `min()` or `max()`.
- Every custom statistical function raises `ValueError` for an empty list.

## Pandas verification

The verification reads the source CSV independently with pandas, applies the same documented numeric parsing and row-validity rules, recomputes revenue, product totals, top three products, mean, and median, and prints `MATCH` or `MISMATCH`. Top-product ties use the same alphabetical tie-break. If a mismatch appears, compare the cleaning mask and the tie-break rule first; floating-point totals use a small tolerance to avoid harmless representation differences.

## Project structure

```text
day2-sales-analytics/
├── sales_analysis.py
├── data/
│   └── electronics_sales.csv
├── output/
│   └── sales_report.txt
├── requirements.txt
└── README.md
```
