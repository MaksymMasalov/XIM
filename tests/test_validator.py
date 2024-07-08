import unittest
from pdf_utils.validator import check_pdf_structure


class TestPDFValidator(unittest.TestCase):
    def test_check_pdf_structure(self):
        template_info = {
            "PN": "tst",
            "SN": "123123",
            "DESCRIPTION": "PART",
            "LOCATION": "111",
            "CONDITION": "FN",
            "RECEIVER#": "9",
            "UOM": "EA",
            "EXP DATE": "13.04.2022",
            "PO": "P101",
            "CERT SOURCE": "wef",
            "REC.DATE": "18.04.2022",
            "MFG": "efwfe",
            "BATCH#": "1",
            "DOM": "13.04.2022",
            "REMARK": "LOT#",
            "TAGGED BY": "",
            "Qty": "1",
            "NOTES": "inspection notes"
        }

        test_info = {
            "PN": "tst",
            "SN": "123123",
            "DESCRIPTION": "PART",
            "LOCATION": "111",
            "CONDITION": "FN",
            "RECEIVER#": "9",
            "UOM": "EA",
            "EXP DATE": "13.04.2022",
            "PO": "P101",
            "CERT SOURCE": "wef",
            "REC.DATE": "18.04.2022",
            "MFG": "efwfe",
            "BATCH#": "1",
            "DOM": "13.04.2022",
            "REMARK": "LOT#",
            "TAGGED BY": "",
            "Qty": "1",
            "NOTES": "inspection notes"
        }

        result = check_pdf_structure(template_info, test_info)
        self.assertTrue(result)

        # Проверка с отсутствующими ключами
        test_info_missing_keys = {
            "PN": "tst",
            "SN": "123123"
        }
        result = check_pdf_structure(template_info, test_info_missing_keys)
        self.assertFalse(result)


if __name__ == '__main__':
    unittest.main()
