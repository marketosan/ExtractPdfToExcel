import openpyxl
from openpyxl.styles import Alignment
from PdfToExcel.main.Product import Product
from datetime import datetime


class ExcelPrinter:
    COLUMN_TITLES = ["Part Number", "Description", "Qty", "PO", "Delivery date"]
    PART_NUMBER_SIZE = 15
    DESCRIPTION_SIZE = 30
    QUANTITY_SIZE = 8
    PURCHASE_ORDER_SIZE = 15
    DELIVERY_DATE_SIZE = 20
    RESULT_FILE_PREFIX = "extracted_pdf-"
    DATE_TIME_FORMAT = "%d_%b_%Y-%H_%M_%S"

    def __init__(self):
        self.workbook = openpyxl.Workbook()
        self.sheet = self.workbook.active
        self.sheet.column_dimensions["A"].width = self.PART_NUMBER_SIZE
        self.sheet.column_dimensions["B"].width = self.DESCRIPTION_SIZE
        self.sheet.column_dimensions["C"].width = self.QUANTITY_SIZE
        self.sheet.column_dimensions["D"].width = self.PURCHASE_ORDER_SIZE
        self.sheet.column_dimensions["E"].width = self.DELIVERY_DATE_SIZE

        self.sheet.append(self.COLUMN_TITLES)

        for row in self.sheet.rows:
            cell_A = row[:1][0]
            cell_A.alignment = Alignment(horizontal="left")

    def print_to_pdf(self, data):
        for product in data:
            self.sheet.append(product.to_list())
        filen_name = self.get_file_name()
        self.workbook.save(filen_name)
        print("Pdf files were successfully extracted to " + filen_name)
        return filen_name

    def get_file_name(self):
        current_date_time = datetime.now()
        formatted_date_time = current_date_time.strftime(self.DATE_TIME_FORMAT)
        return self.RESULT_FILE_PREFIX + formatted_date_time + ".xlsx"


if __name__ == "__main__":
    p1 = Product("400-0530", "Cover, Plastic, MSFD Alarm PCB", "3", "01.06.2023", "4900046964")
    p2 = Product("400-0531", "Cover, Plastic, MSFD Voltage M", "2", "01.06.2023", "4900046964")
    data = list()
    data.append(p1)
    data.append(p2)

    excel_printer = ExcelPrinter()
    excel_printer.print_to_pdf(data)
