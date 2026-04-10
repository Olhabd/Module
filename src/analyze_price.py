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
    result = []

    for record in records:
        if record["product_name"].lower() == product_name.lower():
            result.append(record)

    return result


def last_month_records(records):
    if not records:
        return []

    sorted_records = sorted(records, key=lambda x: x["date"])
    latest_date = sorted_records[-1]["date"]
    month_ago = latest_date - timedelta(days=30)

    result = []

    for record in sorted_records:
        if record["date"] >= month_ago:
            result.append(record)

    return result


def price_change(records):
    if len(records) < 2:
        raise ValueError("Недостатньо даних для обчислення зміни ціни")

    sorted_records = sorted(records, key=lambda x: x["date"])
    start_price = sorted_records[0]["price"]
    end_price = sorted_records[-1]["price"]

    change = end_price - start_price
    percent_change = (change / start_price) * 100

    return {
        "start_price": start_price,
        "end_price": end_price,
        "change": round(change, 2),
        "percent_change": round(percent_change, 2)
    }


def get_product_price_change(file_path, product_name: str):
    records = read_price(file_path)
    product_records = product_filter(records, product_name)
    recent_records = last_month_records(product_records)

    return price_change(recent_records)


if __name__ == "__main__":
    file_path = "data/products.txt"
    product_name = input("Введіть назву продукта: ")

    try:
        result = get_product_price_change(file_path, product_name)
        print(f"Початкова ціна: {result['start_price']}")
        print(f"Кінцева ціна: {result['end_price']}")
        print(f"Зміна ціни: {result['change']}")
        print(f"Зміна ціни у відсотках: {result['percent_change']}%")
    except ValueError as error:
        print(f"Помилка: {error}")
