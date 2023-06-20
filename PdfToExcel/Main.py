import pdfquery
from pdfminer.layout import LTTextLineHorizontal, LTTextBoxHorizontal

from PdfToExcel.Product import Product
from PdfToExcel.ValidationHelper import ValidationHelper


class MyPdfToExcelExtractor:
    ITEMS_LINE_SEPARATOR = '---------------'

    PART_NUMBER_INX_AFTER_LINE = 1
    DESCRIPTION_INX_AFTER_LINE = 2
    QUANTITY_INX_AFTER_LINE = 4
    DELIVERY_DATE_INX_AFTER_LINE = 7

    def __init__(self, file_path):
        self.validation_helper = ValidationHelper()
        self.final_items = list()
        self.pdf = pdfquery.PDFQuery(file_path)
        self.pdf.load()

        self.get_purchase_order()

    # only to create xml representation of pdf
    def extract_pdf_to_xml_file(self):
        self.pdf.tree.write('my_pdf_as_xml.xml', pretty_print=True)

    def get_purchase_order(self):
        purchase_order_matched = self.pdf.pq('LTTextLineHorizontal:contains("PURCHASE ORDER:")')
        self.purchase_order_value = self.validation_helper.validate_and_get_purchase_order(
            purchase_order_matched.children()[0])

    def extract_and_save_all_fields(self):
        text_lines_horizontal_matched = self.pdf.pq('LTTextLineHorizontal:contains("UN.PRICE(USD)")')

        for matched_table in text_lines_horizontal_matched:
            parent_rect_with_info = matched_table.getparent()

            for idx, child_text_line_horizontal in enumerate(parent_rect_with_info.iterchildren()):
                if isinstance(child_text_line_horizontal.layout, LTTextLineHorizontal):
                    line_text_value = self.validation_helper.get_value(child_text_line_horizontal)
                    if self.ITEMS_LINE_SEPARATOR in line_text_value:
                        self.final_items.append(self.get_product_from_parent_rect(idx, parent_rect_with_info))


    def get_product_from_parent_rect(self, index, parent_rect):
        rect_children = parent_rect.getchildren()
        if len(rect_children) < index + self.DELIVERY_DATE_INX_AFTER_LINE:
            raise ValueError("Received unexpected PDF format, wont be able to retrieve data")

        part_number = self.validation_helper.validate_and_get_part_number(
            rect_children[index + self.PART_NUMBER_INX_AFTER_LINE])
        description = self.validation_helper.validate_and_get_description(
            rect_children[index + self.DESCRIPTION_INX_AFTER_LINE])
        quantity = self.validation_helper.validate_and_get_quantity(rect_children[index + self.QUANTITY_INX_AFTER_LINE])
        delivery_date = self.validation_helper.validate_and_get_delivery_date(
            rect_children[index + self.DELIVERY_DATE_INX_AFTER_LINE])

        return Product(part_number, description, quantity, delivery_date, self.purchase_order_value)

    def print_extracted_data(self):
        for item in self.final_items:
            print(item)
            print('-----------------')


# ==============================================================================
# MAIN
if __name__ == '__main__':
    pdfToExcelExtractor = MyPdfToExcelExtractor('./samples/mypdf3.PDF')
    pdfToExcelExtractor.extract_and_save_all_fields()
    pdfToExcelExtractor.print_extracted_data()
