from datetime import datetime, timedelta

def read_price(file_path: str):

    records = []

    with open(file_path, "r", encoding="utf-8") as file:

        for line in file:
            line = line.strip()
            if not line:
                continue

            parts = [part.strip() for part in line.split(",")]

            if len(parts) != 3:
                raise ValueError(f"Неправильний формат: {line}")

            product_name, date_str, price_str = parts

            record = {
                "product_name": product_name,
                "date": datetime.strptime(date_str, "%Y-%m-%d"),
                "price": float(price_str)
            }

            records.append(record)

    return records

def product_filter(records, product_name: str):
    
    results = []

    for record in records:
        if record["product_name"].lower() == product_name.lower():
            results.append(record)

    return results

def last_month_records(records):

    if not records:
        return []
    
    sorted_records = sorted(records, key=lambda x: x["date"])
    latest_date = sorted_records[-1]["date"]

    month = latest_date - timedelta(days=30)

    result = []

    for record in sorted_records:
        if record["date"] >= month:
            result.append(record)

    return result