from datetime import datetime

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