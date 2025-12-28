from __future__ import annotations
from .buildable import Buildable
from .functions import euclidean_distance
import json


class Keyboard(Buildable):
    def __init__(
        self,
        keys: dict[str, tuple[float, float]],
    ):
        """
        Builder method of the class Keyboard.

        Args:
            keys (dict[str, tuple[float, float]]): the dictionary with the keys and the coordinates

        Example:
        >>> Keyboard({"z":(2, 0), "a":(1.5, 1), "q":(1, 2), "`":(0, 3)})

        """
        self._keys: dict[str, tuple[float, float]] = keys
        self._keys_weight: dict[str, dict[str, int]] = {}

        keys_list = list(self._keys.items())
        for i, (key_i, coordinate_i) in enumerate(keys_list):
            self._keys_weight.setdefault(key_i, {key_i: 0})
            for ii in range(i + 1, len(keys_list)):
                key_ii: str = keys_list[ii][0]
                coordinate_ii: tuple[float, float] = keys_list[ii][1]
                weight = int(round(euclidean_distance(coordinate_i, coordinate_ii)))

                if weight > 1:
                    continue

                self._keys_weight[key_i][key_ii] = weight
                self._keys_weight.setdefault(key_ii, {key_ii: 0})[key_i] = weight

    def __repr__(self) -> str:
        """
        Return the representation of the instance in a string format

        Returns:
            str: the instance of the class in a string format

        Example:
        >>> print(k)
        {
          "`": [
            0,
            3
          ],
          "z": [
            2,
            0
          ]
        }
        """
        class_output: list[str] = []
        for key, coordinate in self._keys.items():
            class_output.append(f"\n{key} {coordinate}")
            for k, w in self._keys_weight[key].items():
                class_output.append(f"\n |-- ({w}) {k}")

        return "".join(class_output)

    def __getitem__(self, key: str | tuple[str, str]) -> dict[str, int] | int:
        """
        Return the neighbours if passed a single key or the weight between the two keys if a tuple has given

        Args:
            key (str | tuple[str, str]): a key or a tuple of key

        Returns:
            dict[str, int]: the neighbours if a key has been given
            int: the weight based on the distance if a tuple has been given

        Raises:
            KeyError: if the argument is a str and not exist
            TypeError: if the argument is not a str or a tuple of len = 2

        Example:
        >>> k['a']
        {'a': 0, 'z': 1, 's': 1, 'q': 1, 'w': 1}

        >>> k['a', 'b']
        2
        """
        if isinstance(key, str):
            if not self.has_key(key):
                raise KeyError(f"Key {key} not exists")

            return self._keys_weight[key]
        elif isinstance(key, tuple) and len(key) == 2:
            return self.get_weight(key[0], key[1])
        else:
            raise TypeError("The index must be a str or a tuple[str, str]")

    def has_key(self, key: str) -> bool:
        """
        Check if the key exist in the instance

        Args:
            key (str): a key to Check

        Returns:
            bool: True in case the key exist, False otherwise

        Example:
        >>> k.has_key("f")
        True
        """
        return key in self._keys

    def get_weight(self, k1: str, k2: str, default_weight: int = 2) -> int:
        """
        Return the weight based on the distance between the two keys:
         - 0 if they are the same key
         - 1 if they are neighbours
         - default_weight otherwise

        Args:
            k1 (str): the first key
            k2 (str): the second key
            default_weight (int) = 2: the default weight

        Returns:
            int: the weight based on the distance between the keys

        Example:
        >>> k.get_weight("a", "s")
        1
        >>> k.get_weight("a", "l")
        2
        """
        return (
            self._keys_weight[k1].get(k2, default_weight)
            if self.has_key(k1)
            else default_weight
        )

    def add_key(self, key: str, coordinate: tuple[float, float]):
        """
        Add a key to the instance

        Args:
            key (str): a key to add to the instance
            coordinate (tuple[float, float]): the coordinate of the new key

        Raises:
            ValueError: if the key already exists

        Example:
        >>> k.add_key('~', (0, 3))
        """
        if key in self._keys:
            raise ValueError(f"Key `{key}` exists")

        self._keys[key] = coordinate
        self._keys_weight[key] = {key: 0}
        for k in self._keys:
            weight: int = int(round(euclidean_distance(self._keys[k], coordinate)))

            if weight > 1:
                continue
            self._keys_weight[k].setdefault(key, weight)
            self._keys_weight.setdefault(key, {key: 0}).setdefault(k, weight)

    def update_key(self, key: str, coordinate: tuple[float, float]):
        """
        Update the coordinate of the key

        Args:
            key (str): the key with the new coordinate
            coordinate tuple[float, float]: the new coordinate

        Raises:
            ValueError: if the key not exist

        Example:
        >>> k.update_key("z", (10, 10))
        """
        if not self.has_key(key):
            raise ValueError(f"Key `{key}` not exists")

        self.del_key(key)
        self.add_key(key, coordinate)

    def del_key(self, key: str):
        """
        Removed the given key

        Args:
            key (str): the key to remove

        Raises:
            ValueError: if the key not exist

        Example:
        >>> k.del_key("z")
        """
        if not self.has_key(key):
            raise ValueError(f"Key `{key}` not exists")

        for k in list(self._keys_weight[key].keys()):
            del self._keys_weight[k][key]
        del self._keys_weight[key]
        del self._keys[key]

    def clear(self):
        """
        Clear all the values in the instance

        Example:
        >>> k.clear()
        """
        self._keys.clear()
        self._keys_weight.clear()

    def dumps(self, indent: int = 2) -> str:
        """
        Return the instance as a string in json format

        Args:
            indent (int) = 2: number of spaces for the indentation

        Returns:
            str: the instance as a string in json format

        Example:
        >>> print(k.dumps())
        {
          "`": [
            0,
            3
          ],
          "z": [
            2,
            0
          ]
        }
        """
        return json.dumps(self._keys, indent=indent)

    def dump(self, ptr_file, indent: int = 0):
        """
        Write the instance in the given file in json format

        Args:
            ptr_file (SupportsWrite[str]): pointer to the file to write the instance
            indent (int) = 2: number of spaces for the indentation
        Example:
        >>> with open("en.json", "w+") as file:
        ...   k.dump(file, indent=2)
        """
        json.dump(self._keys, ptr_file, indent=indent)


@Keyboard.register_builder("from_json")
def keyboard_builder_from_json(ptr_file) -> Keyboard:
    """
    Builder for the class Keyboard, giving a json file return a Keyboard

    Args:
        ptr_file (SupportsRead[str | bytes]: pointer to the file

    Returns:
        Keyboard: a Keyboard with the weights between the keys

    Example:
    >>> with open("us_keys.json") as file:
    ...   k = Keyboard.build("from_json", file)
    """

    raw_data: dict[str, list[float]] = json.load(ptr_file)
    data: dict[str, tuple[float, float]] = {
        key: tuple(coordinate) for key, coordinate in raw_data.items()
    }

    return Keyboard(data)


@Keyboard.register_builder("from_file")
def keyboard_builder_from_file(ptr_file, delimiter: str = "|") -> Keyboard:
    """
    Builder for the class Keyboard, giving a file return a Keyboard

    Args:
        ptr_file (SupportsRead[str | bytes]): pointer to the file
        delimiter (str) = "|": the delimiter to separate the values

    Returns:
        Keyboard: a Keyboard with the weights between the keys

    Example:
    >>> with open("us_keys") as file:
    ...   k = Keyboard.build("from_file", file)
    """
    keys: dict[str, tuple[float, float]] = {}

    split_line: list[str] = []
    for line in ptr_file:
        split_line = line.rstrip("\n").split(delimiter)

        if len(split_line) != 3:
            continue

        key, x, y = split_line
        keys[key] = (float(x), float(y))

    return Keyboard(keys)
