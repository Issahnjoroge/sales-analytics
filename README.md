# Sales Analytics — September 2026

## 1. Project Overview

This project analyses September 2026 electronics sales data using Python.

The program reads sales records from a CSV file, cleans and validates the data, calculates revenue statistics, identifies top-selling products and high value transactions, and generates a sales report.

The analysis uses Python's standard library. Pandas is used separately to verify the results.

## 2. Project Objectives

- Read sales data from a CSV file.
- Validate and clean quantity and unit price values.
- Calculate total revenue and revenue by product.
- Identify the top three products.
- Identify high value transactions.
- Analyse revenue by store and payment method.
- Calculate mean, median, minimum and maximum transaction revenue.
- Verify analysis results independently using pandas.

## 3. Data Cleaning and Validation

The dataset contained 50 sales records.

After validation:
- 46 records were accepted for analysis.
- 4 records were skipped because of invalid or missing values.

The program applies these validation rules:

- Quantity must be numeric, positive and a whole number.
- Unit price must be numeric and positive.
- Currency prefixes, commas and spaces are cleaned before numeric conversion.
- Invalid or missing values are not guessed or automatically corrected.
- Skipped records retain their original values and include specific reasons for exclusion.

### Skipped Records

| Sale ID | Reason |
|---|---|
| S-3006 | Quantity is not numeric (`two`) |
| S-3030 | Unit price is not numeric (`N/A`) |
| S-3035 | Quantity is blank |
| S-3039 | Unit price is blank |

## 4. Key Analysis Findings

### Overall Revenue

- Total revenue: **KES 1,310,812.00**
- Valid transactions: **46**
- Skipped records: **4**
- High-value transactions: **5**

### Top Three Products

| Product | Revenue (KES) |
|---|---:|
| HP 15 Laptop | 389,994.00 |
| Hisense 43in Smart TV | 272,993.00 |
| Lenovo Tab M10 | 199,992.00 |

HP 15 Laptop generated the highest revenue among the products analysed.

### Revenue by Store

| Store | Revenue (KES) |
|---|---:|
| Kisumu Mega Plaza | 449,678.00 |
| Nairobi CBD | 331,085.00 |
| Westgate | 235,979.00 |
| Mombasa City Mall | 154,082.00 |
| Nakuru Westside | 139,988.00 |

Kisumu Mega Plaza generated the highest store revenue.

### Revenue by Payment Method

| Payment Method | Revenue (KES) |
|---|---:|
| M-Pesa | 738,568.00 |
| Cash | 304,375.00 |
| Card | 267,869.00 |

M-Pesa accounted for the highest revenue by payment method.

### Transaction Revenue Statistics

| Statistic | Amount (KES) |
|---|---:|
| Mean | 28,495.91 |
| Median | 11,097.00 |
| Minimum | 1,499.00 |
| Maximum | 259,996.00 |

## 5. Pandas Verification

The program independently verifies the standard-library analysis using pandas.

The following checks passed:

| Verification | Result |
|---|---|
| Total revenue | MATCH |
| Revenue by product | MATCH |
| Top 3 products | MATCH |
| Mean / median | MATCH |

All four verification checks returned MATCH.

## 6. Project Structure

```text
day2-sales-analytics/
│
├── data/
│   └── electronics_sales.csv
│
├── output/
│   └── sales_report.txt
│
├── sales_analysis.py
├── README.md
└── requirements.txt
```

## 7. Requirements

- Python 3
- Pandas version 2.0 or later

Install the dependency using:

```bash
python3 -m pip install -r requirements.txt
```

## 8. How to Run the Project

Open a terminal in the project directory and run:

```bash
python3 sales_analysis.py
```

The program displays the sales report and saves the generated report to:

```text
output/sales_report.txt
```

## 9. Conclusion

The analysis processed 46 valid sales records out of 50 supplied records, generating total revenue of KES 1,310,812.00.

HP 15 Laptop was the highest revenue product, Kisumu Mega Plaza was the highest revenue store, and M-Pesa was the leading payment method.

All four pandas verification checks matched the results produced by the standard library analysis.

