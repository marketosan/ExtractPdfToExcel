import pdfquery, re
from pdfminer.layout import LTTextLineHorizontal, LTTextBoxHorizontal

from PdfToExcel.product import Product


class MyPdfToExcelExtractor:
    PART_NUMBER_PATTERN = r'^\d+-\d+$'
    ITEMS_LINE_SEPARATOR = '---------------'

    PART_NUMBER_INX_AFTER_LINE = 1
    DESCRIPTION_INX_AFTER_LINE = 2
    QUANTITY_INX_AFTER_LINE = 4
    DELIVERY_DATE_INX_AFTER_LINE = 7

    def __init__(self, file_path):
        self.final_items = list()
        self.pdf = pdfquery.PDFQuery(file_path)
        self.pdf.load()

        self.get_purchase_order()
        self.get_parent_rect_with_all_info()

    def extract_pdf_to_xml_file(self):
        self.pdf.tree.write('my_pdf_as_xml.xml', pretty_print=True)
        self.pdf

    def get_purchase_order(self):
        purchase_order_matched = self.pdf.pq('LTTextLineHorizontal:contains("PURCHASE ORDER:")')
        self.purchase_order_value = \
            purchase_order_matched.children()[0].layout.get_text().strip().replace('\n', '').split(':')[1].strip()

    def get_parent_rect_with_all_info(self):
        # find the lines containing a unique constant key word such as 'UN.PRICE(USD)"' and then use its parent to retrieve rest info
        self.text_lines_horizontal_matched = self.pdf.pq('LTTextLineHorizontal:contains("UN.PRICE(USD)")')

    def extract_and_save_all_fields(self):
        for line in self.text_lines_horizontal_matched:
            parent_rect_with_info = line.getparent()
            for idx, child_text_line_horizontal in enumerate(parent_rect_with_info.iterchildren()):

                if isinstance(child_text_line_horizontal.layout, LTTextLineHorizontal):
                    line_text_value = self.getValue(child_text_line_horizontal)
                    if self.ITEMS_LINE_SEPARATOR in line_text_value:
                        self.final_items.append(self.get_product_from_parent_rect(idx, parent_rect_with_info))
                    # print(f"{idx}: {value}")

    def getValue(self, text_line_horizontal):
        return text_line_horizontal.getchildren()[0].layout.get_text().strip().replace('\n', '')

    def get_product_from_parent_rect(self, index, parent_rect):
        rect_children = parent_rect.getchildren()

        part_number = self.get_and_validate_part_number(rect_children[index + self.PART_NUMBER_INX_AFTER_LINE])
        description = self.getValue(rect_children[index + self.DESCRIPTION_INX_AFTER_LINE])
        quantity = self.getValue(rect_children[index + self.QUANTITY_INX_AFTER_LINE])
        delivery_date = self.getValue(rect_children[index + self.DELIVERY_DATE_INX_AFTER_LINE])

        return Product(part_number, description, quantity, delivery_date, self.purchase_order_value)

    def get_and_validate_part_number(self, textbox):
        if isinstance(textbox.layout, LTTextBoxHorizontal):
            for child_text_line_horizontal in textbox.iterchildren():
                if len(child_text_line_horizontal.getchildren()) == 1:
                    value = self.getValue(child_text_line_horizontal)
                    if re.match(self.PART_NUMBER_PATTERN, value):
                        return value

        raise ValueError("Unable to find part number")

    def print_extracted_data(self):
        for item in self.final_items:
            print(item)
            print('-----------------')


# ==============================================================================
# MAIN
if __name__ == '__main__':
    pdfToExcelExtractor = MyPdfToExcelExtractor('./mypdf.PDF')
    pdfToExcelExtractor.extract_and_save_all_fields()
    pdfToExcelExtractor.print_extracted_data()
