import traceback

import tkinter as tk

from pdfminer.layout import LTTextLineHorizontal, LTTextBoxHorizontal

from PdfToExcel.main.ExcelPrinter import ExcelPrinter
from PdfToExcel.main.FileSelectGUI import FileSelectGUI
from PdfToExcel.main.Product import Product
from PdfToExcel.main.ValidationHelper import ValidationHelper
from pdfquery import PDFQuery
from tkinter import messagebox


class MyPdfToExcelExtractor:
    ITEMS_LINE_SEPARATOR = '---------------'
    PART_NO_X_RANGE = (45, 46)
    PART_NO_WITH_AA_X_RANGE = (8, 9)
    DESCRIPTION_X_RANGE = (228, 234)
    DATE_X_RANGE = (750, 752)

    def __init__(self, file_paths_set):
        self.validation_helper = ValidationHelper()

        if isinstance(file_paths_set, set) or isinstance(file_paths_set, list):
            self.file_paths_set = file_paths_set
        else:
            self.file_paths_set = {file_paths_set}

        self.extracted_products = list()

    def extract_files(self):
        for file_path in self.file_paths_set:
            try:
                pdf = PDFQuery(file_path)
                pdf.load()
                self.extract_and_save_all_fields(pdf)
                pdf.file.close()
            except Exception as e:
                self.show_error_popup(e, file_path)
                print(e)
                exit()
        print("Received data successfully")

    def extract_and_save_all_fields(self, pdf):
        purchase_order_value = self.get_purchase_order(pdf)

        # find where the column titles are to help find parent table with info (might have more depending one pages)
        text_lines_horizontal_matched = pdf.pq('LTTextLineHorizontal:contains("UN.PRICE(USD)")')

        for matched_table in text_lines_horizontal_matched:
            parent_rect_with_info = matched_table.getparent()

            # then searching for line separators e.g. ------
            for idx, child_text_line_horizontal in enumerate(parent_rect_with_info.iterchildren()):
                if isinstance(child_text_line_horizontal.layout, LTTextLineHorizontal):
                    try:
                        line_text_value = self.validation_helper.get_value(child_text_line_horizontal)
                    except Exception:
                        line_text_value = ""

                    if self.ITEMS_LINE_SEPARATOR in line_text_value:
                        next_value = self.validation_helper.get_value(parent_rect_with_info.getchildren()[idx + 1].getchildren()[0])
                        if "TOTAL AMOUNT FOR ORDER" in next_value or self.ITEMS_LINE_SEPARATOR in next_value:
                            continue
                        else:
                            # using the index of the line separators we can find all items after it
                            self.extracted_products.append(self.get_product_from_parent_rect(idx, parent_rect_with_info, purchase_order_value))

    def get_purchase_order(self, pdf):
        purchase_order_matched = pdf.pq('LTTextLineHorizontal:contains("PURCHASE ORDER:")')
        return self.validation_helper.validate_and_get_purchase_order(purchase_order_matched.children()[0])

    def in_range(self, x_range, line: LTTextLineHorizontal):
        x = self.get_x_location(line)
        return x_range[0] < x < x_range[1]

    def get_x_location(self, line: LTTextLineHorizontal):
        return float(line.attrib.get('x0'))

    def check_and_update_lists(self, item, next_field_to_find, found_values):
        if item is not None:
            next_field_to_find.pop(0)
            found_values.append(item)

    def check_and_return_if_part_number(self, text_line: LTTextLineHorizontal):
        if self.in_range(self.PART_NO_X_RANGE, text_line):
            return self.validation_helper.validate_and_get_part_number(text_line)
        elif self.in_range(self.PART_NO_WITH_AA_X_RANGE, text_line):
            return self.validation_helper.validate_and_get_part_number_without_aa(text_line)
        return None

    def check_and_return_if_description(self, text_line: LTTextLineHorizontal):
        if self.in_range(self.DESCRIPTION_X_RANGE, text_line):
            return self.validation_helper.validate_and_get_description(text_line)
        return None

    def check_and_return_if_date(self, text_line: LTTextLineHorizontal):
        if self.in_range(self.DATE_X_RANGE, text_line):
            return self.validation_helper.validate_and_get_delivery_date(text_line)
        return None

    def get_product_from_parent_rect(self, line_separator_index, parent_rect, purchase_order_value):
        rect_children = parent_rect.getchildren()

        idx = line_separator_index + 1
        next_field_to_find = [self.check_and_return_if_part_number, self.check_and_return_if_description, self.check_and_return_if_date]
        found_values = list()

        while len(next_field_to_find) > 0 and line_separator_index < line_separator_index + 10:

            if isinstance(rect_children[idx].layout, LTTextBoxHorizontal):
                for child_text_line in rect_children[idx].iterchildren():
                    item = next_field_to_find[0](child_text_line)
                    self.check_and_update_lists(item, next_field_to_find, found_values)
                    if len(next_field_to_find) == 0:
                        break
            else:
                item = next_field_to_find[0](rect_children[idx])
                self.check_and_update_lists(item, next_field_to_find, found_values)
            idx += 1

        quantity = self.validation_helper.validate_and_get_quantity(rect_children[idx - 4])
        return Product(found_values[0], found_values[1], quantity, found_values[2], purchase_order_value)

    def print_extracted_data(self):
        for item in self.extracted_products:
            print(item)
            print('-----------------')

    # only to create xml representation of pdf
    # def extract_pdf_to_xml_file(self):
    #     self.pdf.tree.write(f'generated_xmls/my_pdf_as_xml.xml', pretty_print=True)

    @staticmethod
    def show_error_popup(exception, file):
        file = file.strip().split('/')[-1]
        root = tk.Tk()
        root.withdraw()  # Hide the main window
        error_message = f"{type(exception).__name__}: {str(exception)}\n Please contact admin to resolve issue.\n\nTraceback:\n{traceback.format_exc()}"
        messagebox.showerror("Error on file: " + file, error_message)


# ==============================================================================
# MAIN
if __name__ == '__main__':
    ui_interface = FileSelectGUI()

    pdf_to_excel_extractor = MyPdfToExcelExtractor(ui_interface.file_paths_to_extract)
    pdf_to_excel_extractor.extract_files()

    excel_printer = ExcelPrinter()
    excel_printer.print_to_pdf(pdf_to_excel_extractor.extracted_products, ui_interface.extracted_file_name_with_path)
