from unittest import TestCase

from orderNumKivyLogin import ScrollGridLayout


class TestLogin(TestCase):
    def test_CorrectAnswer(self):
        screen = ScrollGridLayout()
        screen.passdict = {
            "Test": "12345"
        }

        screen.logname.text = "Test"
        screen.password.text = "12345"

        self.assertTrue(screen.CorrectAnswer())

        screen.logname.text = "Test"
        screen.password.text = "23456"

        self.assertFalse(screen.CorrectAnswer())
