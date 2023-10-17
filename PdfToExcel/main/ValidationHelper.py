from re import match
from datetime import datetime

from pdfminer.layout import LTTextBoxHorizontal, LTTextLineHorizontal


class ValidationHelper:
    PURCHASE_ORDER_FORMAT = r'^PURCHASE ORDER:(\s)*\d+$'
    PART_NUMBER_PATTERN = r'^(\d+-)+\d+$'  # e.g 400-0178-123
    PART_NUMBER_PATTERN_WITH_AA = r'^\d+\s+(\d+-)+\d+$'  # e.g 0010 400-0178
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

    def validate_and_get_part_number(self, textbox_or_text_line, allow_numeric_part_number):
        part_number = None
        if isinstance(textbox_or_text_line.layout, LTTextBoxHorizontal):
            for child_text_line_horizontal in textbox_or_text_line.iterchildren():
                # we should never allow numeric in current case as we search among multiple lines to find part number
                # and we dont have enough info to differentiate it from AA if it is numeric
                part_number = self.get_part_number(child_text_line_horizontal)
                if part_number is not None:
                    return part_number
        elif isinstance(textbox_or_text_line.layout, LTTextLineHorizontal):
            part_number = self.get_part_number(textbox_or_text_line, allow_numeric_part_number)

        if part_number is None and allow_numeric_part_number:
            ValueError("Unable to find part number")

        return part_number

    def get_part_number(self, text_line, allow_numeric_part_number=False):
        part_number = self.get_value(text_line)
        if self.has_format(part_number, self.PART_NUMBER_PATTERN_WITH_AA):
            part_number = part_number.split()[1]
        if self.has_format(part_number, self.PART_NUMBER_PATTERN):
            if not (self.valid_x_location(text_line, 44, 46) or self.valid_x_location(text_line, 8, 9)):
                part_number = self.append_confirm(part_number)
            return part_number
        if allow_numeric_part_number and part_number.isnumeric():
            return part_number
        return None

    def validate_and_get_description(self, text_line_horizontal):
        description = self.get_value(text_line_horizontal)
        if not self.valid_x_location(text_line_horizontal, 228, 234):
            description = self.append_confirm(description)
        return description
        # raise ValueError("Unable to find valid description")

    def validate_and_get_quantity(self, text_line_horizontal):
        quantity = self.get_value(text_line_horizontal)
        if quantity.replace('.', '').isnumeric():
            if not self.valid_x_location(text_line_horizontal, 508, 545):
                quantity = self.append_confirm(quantity)
            return quantity
        raise ValueError("Unable to find valid quantity")

    def validate_and_get_delivery_date(self, text_line_horizontal):
        delivery_date = self.get_value(text_line_horizontal)
        if not self.validate_date(delivery_date, self.DATE_FORMAT):
            raise ValueError("Unable to find valid delivery date")
        if not self.valid_x_location(text_line_horizontal, 747, 756):
            delivery_date = self.append_confirm(delivery_date)
        return delivery_date
