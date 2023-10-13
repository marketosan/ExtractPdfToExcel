import unittest

from PdfToExcel.main.ExcelPrinter import ExcelPrinter
from PdfToExcel.main.Main import MyPdfToExcelExtractor
from PdfToExcel.main.Product import Product
import pandas as pd
import os



class pdfExtractionTest(unittest.TestCase):

    def test_extract_one_pdf_full_data(self):
        pdf_to_excel_extractor = MyPdfToExcelExtractor({f"./samples/PDF_files/mypdf1.PDF"})
        pdf_to_excel_extractor.extract_files()
        # pdf_to_excel_extractor.print_extracted_data()
        self.assert_products_equal(pdf_to_excel_extractor.extracted_products[0], Product('400-0530', 'Cover, Plastic, MSFD Alarm PCB', '3', '01.06.2023', '4900046964'))
        self.assert_products_equal(pdf_to_excel_extractor.extracted_products[1], Product('400-0531', 'Cover, Plastic, MSFD Voltage M', '2', '01.06.2023', '4900046964'))
        self.assert_products_equal(pdf_to_excel_extractor.extracted_products[2], Product('400-0736', 'Bracket, Back Divider CPRI 1U 19”', '2', '01.06.2023', '4900046964'))
        self.assert_products_equal(pdf_to_excel_extractor.extracted_products[3], Product('400-1165', 'Bracket, Step, 12 Position, Neutral', '30', '01.06.2023', '4900046964'))
        self.assert_products_equal(pdf_to_excel_extractor.extracted_products[4], Product('400-1453', 'Cover Asm, Top, 3-Pos 1U Alarm RM', '100', '01.06.2023', '4900046964'))

        self.assert_products_equal(pdf_to_excel_extractor.extracted_products[5], Product('400-1472', 'Bracket, Mounting, Universal YH/YQ-ZH/ZQ', '61', '01.06.2023', '4900046964'))
        self.assert_products_equal(pdf_to_excel_extractor.extracted_products[6], Product('810-0496', 'Harness, 3 Chan Strikesorb Alarm', '50', '01.06.2023', '4900046964'))
        self.assert_products_equal(pdf_to_excel_extractor.extracted_products[7], Product('850-0259', 'Busbar, GND A Box GEN', '20', '01.06.2023', '4900046964'))
        self.assert_products_equal(pdf_to_excel_extractor.extracted_products[8], Product('850-0304', 'Busbar, Ground, GB3-3-00-X', '50', '01.06.2023', '4900046964'))
        self.assert_products_equal(pdf_to_excel_extractor.extracted_products[9], Product('850-0577', 'Busbar, Bridge, 7 Pos, 26mm Pitch, L1', '60', '01.06.2023', '4900046964'))
        self.assert_products_equal(pdf_to_excel_extractor.extracted_products[10], Product('850-0660', 'Busbar, Return, Strikesorb 30, AL', '145', '01.06.2023', '4900046964'))
        self.assert_products_equal(pdf_to_excel_extractor.extracted_products[11], Product('850-0677', 'Bus Bar, Neutral, RMx-ED', '23', '01.06.2023', '4900046964'))

    def test_extract_multiple_pdfs(self):
        pdf_files = list()
        for i in range(1,7):
            pdf_files.append(f"./samples/PDF_files/mypdf{i}.PDF")
        pdf_to_excel_extractor = MyPdfToExcelExtractor(pdf_files)
        pdf_to_excel_extractor.extract_files()
        self.assertEqual(len(pdf_to_excel_extractor.extracted_products), 39)

    def test_extract_multiple_pdfs_to_excel(self):
        pdf_files = list()
        for i in range(1,7):
            pdf_files.append(f"./samples/PDF_files/mypdf{i}.PDF")
        pdf_to_excel_extractor = MyPdfToExcelExtractor(pdf_files)
        pdf_to_excel_extractor.extract_files()

        excel_printer = ExcelPrinter()
        result_file_name = "some_filename.xlsx"
        excel_printer.print_to_pdf(pdf_to_excel_extractor.extracted_products, result_file_name)
        expected_result = pd.read_excel("./samples/XLSX_files/extracted_pdf-expected1.xlsx")
        actual_result = pd.read_excel(result_file_name)
        self.assertEqual(len(pdf_to_excel_extractor.extracted_products), 39)
        self.assertTrue(expected_result.equals(actual_result))
        os.remove(result_file_name)

    def assert_products_equal(self, actual: Product, expected: Product):
        self.assertEqual(expected.get_part_number(), actual.get_part_number())
        self.assertEqual(expected.get_description(), actual.get_description())
        self.assertEqual(expected.get_quantity(), actual.get_quantity())
        self.assertEqual(expected.get_delivery_date(), actual.get_delivery_date())
        self.assertEqual(expected.get_purchase_order(), actual.get_purchase_order())

if __name__ == '__main__':
    unittest.main()