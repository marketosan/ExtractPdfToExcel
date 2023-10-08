class Product:
    def __init__(self, part_number, description, quantity, delivery_date, purchase_order):
        self._part_number = part_number
        self._description = description
        self._quantity = quantity
        self._delivery_date = delivery_date
        self._purchase_order = purchase_order

    def get_part_number(self):
        return self._part_number

    def set_part_number(self, part_number):
        self._part_number = part_number

    def get_description(self):
        return self._description

    def set_description(self, description):
        self._description = description

    def get_quantity(self):
        return self._quantity

    def set_quantity(self, quantity):
        self._quantity = quantity

    def get_delivery_date(self):
        return self._delivery_date

    def set_delivery_date(self, delivery_date):
        self._delivery_date = delivery_date

    def get_purchase_order(self):
        return self._purchase_order

    def set_purchase_order(self, purchase_order):
        self._purchase_order = purchase_order

    def __str__(self):
        return f"Part Number: {self._part_number}\nDescription: {self._description}\nQuantity: {self._quantity}\nDelivery Date: {self._delivery_date}\nPurchase Order: {self._purchase_order}"
        # return f"Product('{self._part_number}', '{self._description}', '{self._quantity}', '{self._delivery_date}', '{self._purchase_order}')"

    def __eq__(self, other):
        if isinstance(other, Product):
            return (
                    self._part_number == other._part_number and
                    self._description == other._description and
                    self._quantity == other._quantity and
                    self._delivery_date == other._delivery_date and
                    self._purchase_order == other._purchase_order
            )
        return False
