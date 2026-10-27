"""
Tech Hub Kenya — September 2026 sales analytics.
Tasks 1-7 use only Python's standard library. Pandas is imported only for verification.
"""
import csv
import math
from pathlib import Path

DATA_PATH = Path(__file__).parent / "data" / "electronics_sales.csv"
OUTPUT_PATH = Path(__file__).parent / "output" / "sales_report.txt"
HIGH_VALUE_THRESHOLD = 50_000.0


def read_sales(path=DATA_PATH):
    """Read raw sales using csv.DictReader and report row count and columns."""
    with open(path, "r", newline="", encoding="utf-8-sig") as file:
        reader = csv.DictReader(file)
        rows = list(reader)
        columns = reader.fieldnames or []
    print(f"Rows read: {len(rows)}")
    print(f"Columns found: {', '.join(columns)}")
    return rows


def parse_number(value):
    """Parse trustworthy numeric strings; return None for blank/invalid/non-finite values.

    Repairs deliberately limited to whitespace, thousands commas, and a leading KES
    currency label. Words and ambiguous formats are not guessed.
    """
    if value is None:
        return None
    cleaned = str(value).strip()
    if not cleaned:
        return None
    if cleaned.upper().startswith("KES"):
        cleaned = cleaned[3:].strip()
    cleaned = cleaned.replace(",", "").replace(" ", "")
    try:
        number = float(cleaned)
    except (TypeError, ValueError):
        return None
    if not math.isfinite(number):
        return None
    return number


def convert_rows(rows):
    """Return (clean_rows, skipped_rows), with an explicit reason per rejected row."""
    clean_rows, skipped_rows = [], []
    for raw in rows:
        row = dict(raw)
        reasons = []
        quantity = parse_number(raw.get("quantity"))
        price = parse_number(raw.get("unit_price_kes"))

        if quantity is None:
            reasons.append("quantity is blank or not numeric")
        elif quantity <= 0:
            reasons.append("quantity must be positive")
        elif not quantity.is_integer():
            reasons.append("quantity must be a whole number")

        if price is None:
            reasons.append("unit price is blank or not numeric")
        elif price <= 0:
            reasons.append("unit price must be positive")

        if reasons:
            skipped_rows.append({
                **row,
                "reason": "; ".join(reasons),
            })
            continue

        row["quantity"] = int(quantity)
        row["unit_price_kes"] = price
        row["revenue"] = row["quantity"] * row["unit_price_kes"]
        clean_rows.append(row)
    return clean_rows, skipped_rows


def total_revenue(rows):
    """Sum transaction revenue; calculate it if the row has no revenue field."""
    return sum(row.get("revenue", row["quantity"] * row["unit_price_kes"]) for row in rows)


def revenue_by(rows, field):
    """Aggregate revenue by a column using a plain dictionary."""
    totals = {}
    for row in rows:
        key = row[field]
        totals[key] = totals.get(key, 0.0) + row.get(
            "revenue", row["quantity"] * row["unit_price_kes"]
        )
    return totals


def top_n(totals, n=3):
    """Return highest (name, revenue) pairs; ties break alphabetically by name."""
    if n < 0:
        raise ValueError("n must be zero or greater")
    return sorted(totals.items(), key=lambda item: (-item[1], item[0]))[:n]


def high_value(rows, threshold):
    """Return transactions with revenue greater than or equal to threshold."""
    return [row for row in rows if row["revenue"] >= threshold]


def mean(values):
    if not values:
        raise ValueError("mean() requires at least one value")
    return sum(values) / len(values)


def median(values):
    if not values:
        raise ValueError("median() requires at least one value")
    ordered = sorted(values)
    middle = len(ordered) // 2
    if len(ordered) % 2:
        return ordered[middle]
    return (ordered[middle - 1] + ordered[middle]) / 2


def minimum_maximum(values):
    """Find min and max in one pass, without min()/max() built-ins."""
    if not values:
        raise ValueError("minimum_maximum() requires at least one value")
    smallest = largest = values[0]
    for value in values[1:]:
        if value < smallest:
            smallest = value
        if value > largest:
            largest = value
    return smallest, largest


def verify_with_pandas(path, my_results):
    """Independently clean the source with pandas and compare headline results."""
    try:
        import pandas as pd
    except ImportError:
        print("Pandas verification: SKIPPED (install pandas on your laptop)")
        return

    frame = pd.read_csv(path, dtype=str, keep_default_na=False)
    frame["quantity_num"] = frame["quantity"].map(parse_number)
    frame["price_num"] = frame["unit_price_kes"].map(parse_number)
    valid_quantity = (
        frame["quantity_num"].notna()
        & (frame["quantity_num"] > 0)
        & (frame["quantity_num"] % 1 == 0)
    )
    valid_price = frame["price_num"].notna() & (frame["price_num"] > 0)
    cleaned = frame[valid_quantity & valid_price].copy()
    cleaned["revenue"] = cleaned["quantity_num"] * cleaned["price_num"]
    pandas_total = float(cleaned["revenue"].sum())
    pandas_products = cleaned.groupby("product")["revenue"].sum().to_dict()
    pandas_top = sorted(pandas_products.items(), key=lambda item: (-item[1], item[0]))[:3]
    pandas_mean = float(cleaned["revenue"].mean())
    pandas_median = float(cleaned["revenue"].median())

    def close(a, b):
        return math.isclose(float(a), float(b), rel_tol=1e-9, abs_tol=1e-6)

    checks = [
        ("Total revenue", close(my_results["total_revenue"], pandas_total),
         my_results["total_revenue"], pandas_total),
        ("Revenue by product", my_results["product_revenue"] == pandas_products,
         my_results["product_revenue"], pandas_products),
        ("Top 3", my_results["top_three"] == pandas_top,
         my_results["top_three"], pandas_top),
        ("Mean / median", close(my_results["mean"], pandas_mean)
         and close(my_results["median"], pandas_median),
         (my_results["mean"], my_results["median"]), (pandas_mean, pandas_median)),
    ]
    for label, matched, pure, pandas_value in checks:
        if matched:
            print(f"{label:<20}: MATCH")
        else:
            print(f"{label:<20}: MISMATCH (pure={pure!r}, pandas={pandas_value!r})")


def money(value):
    return f"{value:,.2f}"


def build_report(raw_rows, clean_rows, skipped_rows):
    total = total_revenue(clean_rows)
    products = revenue_by(clean_rows, "product")
    stores = revenue_by(clean_rows, "store")
    payments = revenue_by(clean_rows, "payment_method")
    top_three = top_n(products, 3)
    qualifying = high_value(clean_rows, HIGH_VALUE_THRESHOLD)
    revenues = [row["revenue"] for row in clean_rows]
    low, high = minimum_maximum(revenues)
    store_names = sorted({row["store"] for row in clean_rows})
    high_value_counts = {
        store: sum(1 for row in qualifying if row["store"] == store)
        for store in store_names
    }
    results = {
        "total_revenue": total,
        "product_revenue": products,
        "top_three": top_three,
        "mean": mean(revenues),
        "median": median(revenues),
    }

    lines = [
        "=== Sales report: September 2026 ===",
        f"Rows read          : {len(raw_rows)}",
        f"Rows used          : {len(clean_rows)}",
        f"Rows skipped       : {len(skipped_rows)}",
    ]
    if skipped_rows:
        lines.append("Skipped rows:")
        lines.extend(f"  {row.get('sale_id', '(unknown ID)')}: {row['reason']}"
                     for row in skipped_rows)
    lines += [
        "",
        f"Total revenue (KES): {money(total)}",
        "",
        "Revenue by product (KES)",
    ]
    for product, amount in sorted(products.items(), key=lambda item: (-item[1], item[0])):
        lines.append(f"  {product:<28} {money(amount):>14}")
    lines += ["", "Top 3 products"]
    for index, (product, amount) in enumerate(top_three, 1):
        lines.append(f"  {index}. {product} - KES {money(amount)}")
    lines += [
        "",
        f"High-value transactions (>= KES {money(HIGH_VALUE_THRESHOLD)}): {len(qualifying)}",
    ]
    for row in qualifying:
        lines.append(
            f"  {row['sale_id']}  {row['sale_date']}  {row['store']}  "
            f"{row['product']}  KES {money(row['revenue'])}"
        )
    lines += ["", "High-value transaction count by store"]
    for store, count in high_value_counts.items():
        lines.append(f"  {store:<24} {count}")
    lines += ["", "Revenue by store (KES)"]
    for store, amount in sorted(stores.items(), key=lambda item: (-item[1], item[0])):
        lines.append(f"  {store:<24} {money(amount):>14}")
    lines += ["", "Revenue by payment method (KES)"]
    for method, amount in sorted(payments.items(), key=lambda item: (-item[1], item[0])):
        lines.append(f"  {method:<24} {money(amount):>14}")
    lines += [
        "",
        "Transaction revenue statistics",
        f"  mean   : KES {money(results['mean'])}",
        f"  median : KES {money(results['median'])}",
        f"  min    : KES {money(low)}",
        f"  max    : KES {money(high)}",
        "",
        "=== pandas verification ===",
    ]
    return "\n".join(lines) + "\n", results


def main():
    raw_rows = read_sales(DATA_PATH)
    clean_rows, skipped_rows = convert_rows(raw_rows)
    report, results = build_report(raw_rows, clean_rows, skipped_rows)
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(report, encoding="utf-8")
    print("\n" + report, end="")
    verify_with_pandas(DATA_PATH, results)


if __name__ == "__main__":
    main()
