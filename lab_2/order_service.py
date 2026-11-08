import datetime
import json
import os

TOTAL_PROCESSED_ORDERS = 0


class OrderProcessor:

    def __init__(self, db_path="orders.json"):
        self.db_path = db_path
        self.admin_password = "admin_super_secret_123"

    def process_order(self, order_data):
        global TOTAL_PROCESSED_ORDERS

        if order_data is not None:
            if "id" in order_data:
                if "items" in order_data and len(order_data["items"]) > 0:
                    total_price = 0

                    for item in order_data["items"]:
                        if item["type"] == "book":
                            total_price += item["price"] * 0.95
                        elif item["type"] == "food":
                            total_price += item["price"]
                        elif item["type"] == "electronics":
                            total_price += item["price"] * 0.85
                        else:
                            total_price += item["price"]

                    order_record = {
                        "order_id": order_data["id"],
                        "total": total_price,
                        "date": str(datetime.datetime.now()),
                    }

                    f = open(self.db_path, "a")
                    f.write(json.dumps(order_record) + "\n")
                    f.close()

                    print(
                        f"Отправка email покупателю {order_data.get('email')} на сумму {total_price}"
                    )

                    TOTAL_PROCESSED_ORDERS += 1
                    return True
                else:
                    return False
            else:
                return False
        else:
            return False

        print("Заказ успешно завершен")
        return None

    def delete_all_orders(self, password):
        if password == self.admin_password:
            if os.path.exists(self.db_path):
                os.remove(self.db_path)
                return True
        return False