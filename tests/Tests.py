'''Юнит-тесты не работают из-за структуры кода класса GetCourses в обёртке while true'''

import unittest
from io import StringIO
from unittest.mock import patch
import requests
import xml.etree.ElementTree as ET

from main import GetCourses

class TestGetCourses(unittest.TestCase):

    def setUp(self):
        self.getcourses = GetCourses()

    @patch('requests.get')
    @patch('xml.etree.ElementTree.fromstring')
    def test_run(self, mock_fromstring, mock_get):
        mock_get.return_value.text = """
            <?xml version="1.0" encoding="ISO-8859-1"?>
            <ValCurs DateRange1="22/07/2023" DateRange2="22/07/2023" name="Foreign Currency Market">
                <Record Date="22.07.2023" Id="R01235">
                    <Nominal>1</Nominal>
                    <Value>70.1234</Value>
                </Record>
            </ValCurs>
        """
        expected_output = 'USD (Доллар США) : 70.1234\n'
        with patch('sys.stdout', new=StringIO()) as fake_output:
            self.getcourses.run(continue_loop=False)
            self.assertEqual(fake_output.getvalue(), expected_output)

    @patch('requests.get')
    def test_getCodeWithISO(self, mock_get):
        mock_get.return_value.json.return_value = {
            "Valute": {
                "USD": {
                    "ID": "R01235",
                    "NumCode": "840",
                    "CharCode": "USD",
                    "Nominal": 1,
                    "Name": "Доллар США",
                    "Value": 70.1234,
                    "Previous": 70.5678
                }
            }
        }
        uniq_code, valute_name = self.getcourses.getCodeWithISO('USD')
        self.assertEqual(uniq_code, 'R01235')
        self.assertEqual(valute_name, 'Доллар США')

if __name__ == '__main__':
    unittest.main()
