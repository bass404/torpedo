import time

#TODO: check if theres a better way.
def get_Shopping_detail_information(self):
    date = time.strftime("%Y-%m-%d")
    shipping_address = "New Addresss"
    no_items = sum([1 for car in self.product_details])
    total_price = sum([car.get_price for car in self.product_details])
    total_discount = sum([car.get_discount for car in self.product_details])
    shipping_charge = 15
    tax = (total_price + shipping_charge) * 0.15
    net_price = total_price + shipping_charge + tax - total_discount

    shopping_details = {
        "date": date,
        "address": shipping_address,
        "no_items": no_items,
        "total": total_price,
        "discount": total_discount,
        "shipping": shipping_charge,
        "tax": tax,
        "net": net_price
    }

    return shopping_details
