from re import match
from datetime import datetime

class ValidationHelper:
    PURCHASE_ORDER_FORMAT = r'^PURCHASE ORDER:(\s)*\d+$'
    PART_NUMBER_PATTERN = r'^[A-Z0-9-]+'  # e.g 400-0178-123 or A123 or A123-
    PART_NUMBER_PATTERN_WITH_AA = r'^\d{5}\s+[A-Z0-9-]+'  # e.g 0010 400-0178 or part number as above
    DATE_FORMAT = '%d.%m.%Y'

    def __init__(self):
        pass

    @staticmethod
    def valid_x_location(text_line_horizontal, range_start, range_end):
        x0_position = float(text_line_horizontal.attrib.get('x0'))
        return x0_position >= range_start and x0_position <= range_end

    @staticmethod
    def get_value(text_line_horizontal):
        item_children = text_line_horizontal.getchildren()
        if len(item_children) == 1:
            return item_children[0].layout.get_text().strip().replace('\n', '')

        elif len(item_children) == 0:
            return text_line_horizontal.layout.get_text().strip().replace('\n', '')

        raise ValueError("Was unable to get value from given item as had more children than expected")

    @staticmethod
    def has_format(string_value, pattern):
        return bool(match(pattern, string_value.strip()))

    @staticmethod
    def validate_date(date_string, date_format):
        try:
            datetime.strptime(date_string, date_format)
            return True
        except ValueError:
            return False

    def validate_and_get_purchase_order(self, text_box_hor_element):
        value = text_box_hor_element.layout.get_text()
        if self.has_format(value, self.PURCHASE_ORDER_FORMAT):
            return value.strip().replace('\n', '').split(':')[1].strip()
        else:
            raise ValueError("Unable to find purchase order")

    @staticmethod
    def append_confirm(value):
        return value + " (CONFIRM)"

    def validate_and_get_part_number(self, text_line):
        part_number = self.get_value(text_line)
        if self.has_format(part_number, self.PART_NUMBER_PATTERN):
            return part_number
        raise ValueError("Unable to find part number")

    def validate_and_get_part_number_without_aa(self, text_line):
        part_number = self.get_value(text_line)
        if self.has_format(part_number, self.PART_NUMBER_PATTERN_WITH_AA):
            return part_number.split()[1]
        return None

    def validate_and_get_description(self, text_line_horizontal):
        description = self.get_value(text_line_horizontal)
        if description is not None:
            return description
        raise ValueError("Unable to find description")

    def validate_and_get_quantity(self, text_line_horizontal):
        quantity = self.get_value(text_line_horizontal)
        if quantity.replace('.', '').isnumeric():
            if not self.valid_x_location(text_line_horizontal, 508, 545):
                quantity = self.append_confirm(quantity)
            return quantity
        raise ValueError("Unable to find valid quantity")

    def validate_and_get_delivery_date(self, text_line_horizontal):
        delivery_date = self.get_value(text_line_horizontal)
        if self.validate_date(delivery_date, self.DATE_FORMAT):
            return delivery_date
        raise ValueError("Unable to find valid delivery date")
