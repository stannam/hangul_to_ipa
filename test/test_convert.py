import unittest
import sys
import os

# Add the directory containing worker.py to sys.path
script_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.join(script_dir, '..', 'src')
sys.path.append(src_dir)

from worker import convert


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
                print('Success:')


if __name__ == "__main__":
    unittest.main()
