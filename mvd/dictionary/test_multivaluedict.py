import unittest
from mvd.dictionary import multivaluedict
from  typing import Set


class DictionaryTests(unittest.TestCase):
    def test_add_item(self):
        dictionary: multivaluedict.MultiValueDict[str, Set[str]] = \
            multivaluedict.MultiValueDict()
        dictionary.add_item("key1", "value1")
        dictionary.add_item("key1", "value2")
        dictionary.add_item("key2", "value1")
        dictionary.add_item("key2", "value2")

        self.assertTrue(dictionary.key_exists("key1"))
        self.assertTrue(dictionary.key_exists("key2"))
        self.assertTrue(dictionary.key_value_exists("key1", "value1"))
        self.assertTrue(dictionary.key_value_exists("key1", "value2"))
        self.assertTrue(dictionary.key_value_exists("key2", "value1"))
        self.assertTrue(dictionary.key_value_exists("key2", "value2"))

    def test_remove_value_from_key(self):
        dictionary: multivaluedict.MultiValueDict[str, Set[str]] = \
            multivaluedict.MultiValueDict()
        dictionary.add_item("key1", "value1")
        dictionary.add_item("key1", "value2")

        dictionary.remove_value_from_key("key1", "value1")
        self.assertFalse(dictionary.key_value_exists("key1", "value1"))
        self.assertTrue(dictionary.key_value_exists("key1", "value2"))

        dictionary.remove_value_from_key("key1", "value2")
        self.assertFalse(dictionary.key_value_exists("key1", "value2"))
        self.assertFalse(dictionary.key_exists("key1"))

    def test_remove_key(self):
        dictionary: multivaluedict.MultiValueDict[str, Set[str]] = \
            multivaluedict.MultiValueDict()
        dictionary.add_item("key1", "value1")
        dictionary.add_item("key2", "value1")

        dictionary.remove_key("key1")
        self.assertFalse(dictionary.key_exists("key1"))
        self.assertTrue(dictionary.key_exists("key2"))

        dictionary.remove_key("key2")
        self.assertFalse(dictionary.key_exists("key2"))

    def test_clear(self):
        dictionary: multivaluedict.MultiValueDict[str, Set[str]] = \
            multivaluedict.MultiValueDict()
        dictionary.add_item("key1", "value1")
        dictionary.add_item("key1", "value2")
        dictionary.add_item("key2", "value1")
        dictionary.add_item("key2", "value2")

        dictionary.clear()
        self.assertFalse(dictionary.key_exists("key1"))
        self.assertFalse(dictionary.key_exists("key2"))

    def test_get_dictionary(self):
        dictionary: multivaluedict.MultiValueDict[str, Set[str]] = \
            multivaluedict.MultiValueDict()
        dictionary.add_item("key1", "value1")
        dictionary.add_item("key1", "value2")
        dictionary.add_item("key2", "value1")
        dictionary.add_item("key2", "value2")

        expected_dict = {
            "key1": {"value1", "value2"},
            "key2": {"value1", "value2"}
        }
        self.assertEqual(dictionary.get_dictionary(), expected_dict)

    def test_key_exists(self):
        dictionary: multivaluedict.MultiValueDict[str, Set[str]] = \
            multivaluedict.MultiValueDict()
        dictionary.add_item("key1", "value1")

        self.assertTrue(dictionary.key_exists("key1"))
        self.assertFalse(dictionary.key_exists("key2"))

    def test_key_value_exists(self):
        dictionary: multivaluedict.MultiValueDict[str, Set[str]] = \
            multivaluedict.MultiValueDict()
        dictionary.add_item("key1", "value1")
        dictionary.add_item("key1", "value2")

        self.assertTrue(dictionary.key_value_exists("key1", "value1"))
        self.assertTrue(dictionary.key_value_exists("key1", "value2"))
        self.assertFalse(dictionary.key_value_exists("key1", "value3"))
        self.assertFalse(dictionary.key_value_exists("key2", "value1"))


if __name__ == "__main__":
    unittest.main()
