import unittest
from dictionary_transform.app import dictionary_transform


class TestNestedDict(unittest.TestCase):

    def setUp(self):
        self.levels = ["a", "b", "c"]
        self.test_dict = dictionary_transform.NestedDict(self.levels)
        self.test_dict.set_data = {'a': 1, 'b': 2, 'c': 3, 'd': 4}
        self.data_dict = {}

    def test_constructor_positive(self):
        result = dictionary_transform.NestedDict(self.levels)
        expected_result = list(dict.fromkeys(self.levels))
        self.assertListEqual(result.levels, expected_result)

    def test_constructor_negative(self):
        with self.assertRaises(dictionary_transform.NestedException):
            dictionary_transform.NestedDict([])

    def test_add_next_key_positive(self):
        result = self.test_dict.add_next_key(self.levels, {'a': 1, 'c': 2, 'b': 3})
        expected_result = {1: {3: {2: [{}]}}}
        self.assertDictEqual(result, expected_result)

    def test_add_next_key_negative(self):
        with self.assertRaises(dictionary_transform.NestedException):
            self.test_dict.add_next_key(self.levels, {'a': 1, 'b': 3})

    def test_combine_dicts(self):
        self.test_dict.combine_dicts({1: {3: {2: [{}]}}}, self.data_dict)
        expected_result = {1: {3: {2: [{}]}}}
        self.assertDictEqual(self.data_dict, expected_result)

    def test_combine_dicts_multiple(self):
        self.test_dict.combine_dicts({1: {3: {2: [{}]}}}, self.data_dict)
        self.test_dict.combine_dicts({1: {2: {2: [{}]}}}, self.data_dict)
        expected_result = {1: {2: {2: [{}]}, 3: {2: [{}]}}}
        self.assertCountEqual(self.data_dict, expected_result)

    def test_combine_duplicates(self):
        self.test_dict.combine_dicts({1: {4: {2: [{}]}}}, self.data_dict)
        self.test_dict.combine_dicts({1: {4: {2: [{}]}}}, self.data_dict)
        expected_result = {1: {4: {2: [{}]}}}
        self.assertCountEqual(self.data_dict, expected_result)


if __name__ == '__main__':
    unittest.main()
