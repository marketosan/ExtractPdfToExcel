import openpyxl
from openpyxl.styles import Alignment


class ExcelPrinter:
    PART_NUMBER_TITLE = 'Part Number'
    DESCRIPTION_TITLE = 'Description'
    QUANTITY_TITLE = 'Qty'
    PURCHASE_ORDER_TITLE = 'PO'
    DELIVERY_DATE_TITLE = 'Delivery date'

    PART_NUMBER_SIZE = 15
    DESCRIPTION_SIZE = 30
    QUANTITY_SIZE = 8
    PURCHASE_ORDER_SIZE = 15
    DELIVERY_DATE_SIZE = 20

    def __init__(self):
        self.workbook = openpyxl.Workbook()
        self.sheet = self.workbook.active
        self.sheet.column_dimensions['A'].width = self.PART_NUMBER_SIZE
        self.sheet.column_dimensions['B'].width = self.DESCRIPTION_SIZE
        self.sheet.column_dimensions['C'].width = self.QUANTITY_SIZE
        self.sheet.column_dimensions['D'].width = self.PURCHASE_ORDER_SIZE
        self.sheet.column_dimensions['E'].width = self.DELIVERY_DATE_SIZE

        self.data = [
            [self.PART_NUMBER_TITLE, self.DESCRIPTION_TITLE, self.QUANTITY_TITLE, self.PURCHASE_ORDER_TITLE, self.DELIVERY_DATE_TITLE],
            ['400-0530', 'Cover, Plastic, MSFD Alarm PCB', 3, '4900046964', '01.06.2023']
        ]

        for row in self.sheet.rows:
            cell_A = row[:1][0]
            cell_A.alignment = Alignment(horizontal='left')

    def extract_data(self, file_name):
        for row in self.data:
            self.sheet.append(row)
        self.workbook.save(file_name)

if __name__ == "__main__":
    excel_printer = ExcelPrinter()
    excel_printer.extract_data('my_data.xlsx')
