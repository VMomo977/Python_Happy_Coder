from unittest import TestCase, mock
from readFile import load_menu

class TestLoad_menu(TestCase):
    def test_load_menu(self):

        menu = load_menu('menu.txt')
        self.assertIsInstance(menu, dict)
        self.assertIsNotNone(menu)


        with mock.patch('builtins.open', mock.mock_open(read_data='test')):
            with open('/dev/null') as f:
                f.read()



