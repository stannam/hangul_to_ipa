import unittest
from src.worker import convert


class TestConvert(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        test_item_path = 'test_items'
        cls.test_cases = []

        with open(test_item_path, 'r', encoding='utf-8') as f:
            for line in f:
                input_str, correct_output = line.strip().split('\t')
                cls.test_cases.append((input_str, correct_output))

    def test_convert(self):
        for input_str, correct_output in self.test_cases:
            with self.subTest(input_str=input_str, expected=correct_output):
                self.assertEqual(convert(input_str), correct_output)
                print(f'Success: {input_str} -> {correct_output}')


if __name__ == "__main__":
    unittest.main()
