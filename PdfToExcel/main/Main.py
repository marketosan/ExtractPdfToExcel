import traceback

import tkinter as tk

from pdfminer.layout import LTTextLineHorizontal

from PdfToExcel.main.ExcelPrinter import ExcelPrinter
from PdfToExcel.main.FileSelectGUI import FileSelectGUI
from PdfToExcel.main.Product import Product
from PdfToExcel.main.ValidationHelper import ValidationHelper
from pdfquery import PDFQuery
from tkinter import messagebox


class MyPdfToExcelExtractor:
    ITEMS_LINE_SEPARATOR = '---------------'

    PART_NUMBER_INX_AFTER_LINE = 1
    DESCRIPTION_INX_AFTER_LINE = 2
    QUANTITY_INX_AFTER_LINE = 4
    DELIVERY_DATE_INX_AFTER_LINE = 7

    def __init__(self, file_paths_set):
        self.validation_helper = ValidationHelper()

        if not file_paths_set:
            print("Was expecting a set or list but received: ", type(file_paths_set))
            exit()

        self.file_paths_set = file_paths_set
        self.extracted_products = list()

    # './samples/PDF_files/mypdf3.PDF'
    def extract_files(self):
        for file_path in self.file_paths_set:
            pdf = PDFQuery(file_path)
            pdf.load()
            self.extract_and_save_all_fields(pdf)
            pdf.file.close()

    def extract_and_save_all_fields(self, pdf):
        purchase_order_value = self.get_purchase_order(pdf)

        # find where the column titles are to help find parent table with info (might have more depending one pages)
        text_lines_horizontal_matched = pdf.pq('LTTextLineHorizontal:contains("UN.PRICE(USD)")')

        for matched_table in text_lines_horizontal_matched:
            parent_rect_with_info = matched_table.getparent()

            # then searching for line separators e.g. ------
            for idx, child_text_line_horizontal in enumerate(parent_rect_with_info.iterchildren()):
                if isinstance(child_text_line_horizontal.layout, LTTextLineHorizontal):
                    line_text_value = self.validation_helper.get_value(child_text_line_horizontal)
                    if self.ITEMS_LINE_SEPARATOR in line_text_value:
                        if "TOTAL AMOUNT FOR ORDER" in self.validation_helper.get_value(parent_rect_with_info.getchildren()[idx + 1].getchildren()[0]):
                            continue
                        # using thre index of the line separators we can find all items after it
                        self.extracted_products.append(self.get_product_from_parent_rect(idx, parent_rect_with_info, purchase_order_value))

    def get_purchase_order(self, pdf):
        purchase_order_matched = pdf.pq('LTTextLineHorizontal:contains("PURCHASE ORDER:")')
        return self.validation_helper.validate_and_get_purchase_order(purchase_order_matched.children()[0])

    def get_product_from_parent_rect(self, line_separator_index, parent_rect, purchase_order_value):
        rect_children = parent_rect.getchildren()

        if len(rect_children) < line_separator_index + self.DELIVERY_DATE_INX_AFTER_LINE:
            raise ValueError("Received unexpected PDF format, wont be able to retrieve data")

        part_number = self.validation_helper.validate_and_get_part_number(rect_children[line_separator_index + self.PART_NUMBER_INX_AFTER_LINE])
        description = self.validation_helper.validate_and_get_description(rect_children[line_separator_index + self.DESCRIPTION_INX_AFTER_LINE])
        quantity = self.validation_helper.validate_and_get_quantity(rect_children[line_separator_index + self.QUANTITY_INX_AFTER_LINE])
        delivery_date = self.validation_helper.validate_and_get_delivery_date(rect_children[line_separator_index + self.DELIVERY_DATE_INX_AFTER_LINE])

        return Product(part_number, description, quantity, delivery_date, purchase_order_value)

    def print_extracted_data(self):
        for item in self.extracted_products:
            print(item)
            print('-----------------')

    # only to create xml representation of pdf
    # def extract_pdf_to_xml_file(self, number):
    #     self.pdf.tree.write(f'generated_xmls/my_pdf_as_xml{number}.xml', pretty_print=True)

    @staticmethod
    def show_error_popup(exception):
        root = tk.Tk()
        root.withdraw()  # Hide the main window
        error_message = f"{type(exception).__name__}: {str(exception)}\n Please contact admin to resolve issue.\n\nTraceback:\n{traceback.format_exc()}"
        messagebox.showerror("Error", error_message)


# ==============================================================================
# MAIN
if __name__ == '__main__':
    try:
        ui_interface = FileSelectGUI()

        pdf_to_excel_extractor = MyPdfToExcelExtractor(ui_interface.file_paths_to_extract)
        pdf_to_excel_extractor.extract_files()

        excel_printer = ExcelPrinter()
        excel_printer.print_to_pdf(pdf_to_excel_extractor.extracted_products, ui_interface.extracted_file_name_with_path)

    except Exception as e:
        MyPdfToExcelExtractor.show_error_popup(e)
