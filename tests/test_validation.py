import unittest
from crew.metrics.api import ValidationError
from crew.metrics import validation


class TestValidation(unittest.TestCase):

    def test_check_float(self):
        # cannot be None
        self.assertRaises(ValidationError, validation.check_float, None)
        # type error
        self.assertRaises(ValidationError, validation.check_float, 1)
        # success
        validation.check_float(1.1)

    def test_check_int(self):
        # cannot be None
        self.assertRaises(ValidationError, validation.check_int, None)
        # type error
        self.assertRaises(ValidationError, validation.check_int, 1.1)
        # success
        validation.check_int(1)

    def test_check_list(self):
        # cannot be None
        self.assertRaises(ValidationError, validation.check_list, None)
        self.assertRaises(ValidationError, validation.check_list, {})
        validation.check_list([])
        validation.check_list([1, 2, None])
        self.assertRaises(ValidationError, validation.check_list, [1, 2],
            check_type=str)
        validation.check_list(['1', '2'], check_type=str)


if __name__ == '__main__':
    unittest.main()
