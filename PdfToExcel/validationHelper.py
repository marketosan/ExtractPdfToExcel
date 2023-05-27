from re import match
from datetime import datetime

from pdfminer.layout import LTTextBoxHorizontal, LTTextLineHorizontal


class ValidationHelper:
    PURCHASE_ORDER_FORMAT = r'^PURCHASE ORDER:(\s)*\d+$'
    PART_NUMBER_PATTERN = r'^(\d+-)+\d+$'
    PART_NUMBER_PATTERN_WITH_AA = r'^\d+\s+(\d+-)+\d+$'
    DATE_FORMAT = '%d.%m.%Y'

    def __init__(self):
        pass

    @staticmethod
    def validate_x_location(text_line_horizontal, range_start, range_end):
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
            raise ValueError("Unable to find valid purchase order")

    def validate_and_get_part_number(self, textbox_or_text_line):
        if isinstance(textbox_or_text_line.layout, LTTextBoxHorizontal):
            for child_text_line_horizontal in textbox_or_text_line.iterchildren():
                if len(child_text_line_horizontal.getchildren()) == 1:
                    value = self.get_value(child_text_line_horizontal)
                    if self.has_format(value, self.PART_NUMBER_PATTERN) and self.validate_x_location(
                            child_text_line_horizontal, 44, 46):
                        return self.get_value(child_text_line_horizontal)

        if isinstance(textbox_or_text_line.layout, LTTextLineHorizontal):
            value = self.get_value(textbox_or_text_line)
            if self.has_format(value, self.PART_NUMBER_PATTERN_WITH_AA):
                value = value.split()[1]
            if self.has_format(value, self.PART_NUMBER_PATTERN):
                return value

        raise ValueError("Unable to find valid part number")

    def validate_and_get_description(self, text_line_horizontal):
        if self.validate_x_location(text_line_horizontal, 228, 232):
            return self.get_value(text_line_horizontal)
        raise ValueError("Unable to find valid description")

    def validate_and_get_quantity(self, text_line_horizontal):
        if self.validate_x_location(text_line_horizontal, 510, 523):
            value = self.get_value(text_line_horizontal)
            if value.isnumeric():
                return value
        raise ValueError("Unable to find valid quantity")

    def validate_and_get_delivery_date(self, text_line_horizontal):
        date = self.get_value(text_line_horizontal)
        if self.validate_x_location(text_line_horizontal, 750, 753) and self.validate_date(date, self.DATE_FORMAT):
            return date
        raise ValueError("Unable to find valid delivery date")
