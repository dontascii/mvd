"""

"""
from typing import TypeVar, Dict, Set, Generic
import logging

T = TypeVar("T")
V = TypeVar("V", set, str)



class ValueExistsException(Exception):
    ...

class ValueMissingException(Exception):
    ...

class KeyMissingException(Exception):
    ...


class MultiValueDict(Generic[T, V]):
    """
    a generic multi-value dictionary class
    \b
    values are an unordered collection of unique items
    """

    def __init__(self):
        self._dict: Dict[T, Set[V]] = {}
        self.logger = logging.getLogger(__name__)


    def __getitem__(self, key: T):
        return self._dict[key]

    def __setitem__(self, key: T, value: V) -> None:
        self.add_item(key, value)

    def __delitem__(self, key):
        del self._dict[key]

    def add_item(self, key: T, value: V) -> None:
        if key not in self._dict:
            self._dict[key] = set()

        if value not in self._dict[key]:
            self._dict[key].add(value)
            self.logger.info("Added")
        else:
            raise ValueExistsException("ERROR, value already exists.")

    def remove_value_from_key(self, key: T, value: V) -> None:
        if key not in self._dict:
            raise KeyMissingException("ERROR, key does not exist.")

        if value in self._dict[key]:
            self._dict[key].remove(value)
            self.logger.info("Removed")

            if len(self._dict[key]) == 0:
                del self._dict[key]
        else:
            raise ValueMissingException("ERROR, value does not exist.")

    def remove_key(self, key: T) -> None:
        if key in self._dict:
            del self._dict[key]
            self.logger.info("Removed")
        else:
            raise KeyMissingException("ERROR, key does not exist.")

    def clear(self) -> None:
        self._dict.clear()
        self.logger.info("Cleared")

    def key_exists(self, key: T) -> bool:
        return key in self._dict

    def get_dictionary(self) -> Dict[T, Set[V]]:
        return self._dict

    def key_value_exists(self, key: T, value: V) -> bool:
        return key in self._dict and value in self._dict[
            key]

    def get_values_for_key(self, key: T) -> Set[V]:
        if key in self._dict:
            return self._dict[key]
        else:
            raise KeyMissingException('ERROR, key not found.')

