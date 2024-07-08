import unittest
from pdf_utils.reader import extract_pdf_info


class TestPDFReader(unittest.TestCase):
    def test_extract_pdf_info(self):
        pdf_file_path = 'test_task.pdf'
        info = extract_pdf_info(pdf_file_path)
        self.assertIn("PN", info)
        self.assertEqual(info["PN"], "tst")
        self.assertIn("SN", info)
        self.assertEqual(info["SN"], "123123")


if __name__ == '__main__':
    unittest.main()
