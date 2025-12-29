from __future__ import annotations
from typing import Callable
from .buildable import Buildable
from .node import Node as BKNode
from .functions import levenshtein_distance
import json


class BKTree(Buildable):
    def __init__(
        self,
        root: BKNode,
        bk_nodes_dict: dict[str, BKNode],
        fn_weights: Callable | None = None,
    ):
        """
        Builder method of the class BKTree.

        Args:
            root (BKNode): the root node of the tree
            bk_nodes_dict (dict[str, BKNode): the list of all the nodes
            fn_weights (Callable | None): the function used to calculate the weights
        Raises:
            KeyError: if the set is empty
            TypeError: if the set is empty

        Example:
        >>> tree = BKTree(BKNode("cake"), {"cake": BKNode("cake")}
        """
        self._bk_nodes_dict: dict[str, BKNode] = bk_nodes_dict
        self._root: BKNode = root
        self._fn_weights: Callable | None = fn_weights

    def __getitem__(self, string: str) -> BKNode:
        """
        Return the Node associated to the string in the tree

        Args:
            string (str): the name of the node in the tree

        Returns:
            BKNode: the pointer of the node

        Raises:
            KeyError: if the string is not associated to a node

        Example:
        >>> tree["node"]
        <__module_name__ object at <memory_address>
        """
        if not self.has_node(string):
            raise KeyError(f"The node `{string}` not exists")

        return self._bk_nodes_dict[string]

    def __repr__(self) -> str:
        """
        Return the formatted representation of the BK tree

        Returns:
            str: the formatted representation of the BK tree

        Example:
        >>> tree

        book
        |-- (1) books
        | |-- (1) book
        |-- (2) Books
        |-- (3) cakbook
        """
        class_output: list[str] = []

        stack: list[BKNode] = [
            self._root,
        ]
        node_level: dict[BKNode, tuple[int, int]] = {self._root: (0, 0)}

        distances: list[int] = []

        while stack:
            current_node = stack.pop()

            distances = list(current_node.get_links().keys())
            distances.sort(reverse=True)

            for distance in distances:
                stack.append(current_node.get_link(distance))
                node_level[current_node.get_link(distance)] = (
                    node_level[current_node][0] + 1,
                    distance,
                )

            class_output.append("\n" + "| " * (node_level[current_node][0] - 1))
            class_output.append(
                f"|-- ({node_level[current_node][1]}) "
                if node_level[current_node][0] != 0
                else ""
            )
            class_output.append(
                f"{current_node.get_value()}"
                + (" [inactive]" if not current_node.is_active() else "")
            )

        return "".join(class_output)

    def get_num_nodes(self) -> int:
        """
        Return the number of the nodes in the tree

        Returns:
            int: the numer of the nodes in the tree

        Example:
        >>> tree.get_num_nodes()
        15
        """
        return len(self._bk_nodes_dict)

    def get_nodes(self) -> set[str]:
        """
        Return a set with all the string in the tree

        Returns:
            set[str]: a set with all the string in the tree

        Example:
        >>> tree.get_nodes()
        {'cake', 'cook', 'book', 'bed'}
        """
        return set(self._bk_nodes_dict.keys())

    def get_neighbors(self, string: str, max_distance: int = 1) -> dict[int, set[str]]:
        """
        Return the similar strings of the argument with equal or less distance from the max distance

        Args:
            string (str): the string to search the neighbors
            max_distance (int) = 1: the max distance from the string

        Returns:
            dict[int, set[str]]: the distances from the string and the relative neighbors with the same distance

        Example:
        >>> tree.get_neighbors("cake")
        {1:{"cakes", "Cake"}}

        >>> tree.get_neighbors("cake", max_distance = 3)
        {1:{"cakes", "Cake"}, 3:{"Carcake"}}

        """
        neighbors: dict[int, set[str]] = {}
        stack: list[BKNode] = []
        stack.append(self._root)
        lev_dist: int = 0

        while stack:
            current_node: BKNode = stack.pop()
            lev_dist = levenshtein_distance(
                string,
                current_node.get_value(),
                fn_weights=self._fn_weights if self._fn_weights is not None else None,
            )

            if lev_dist <= max_distance and current_node.is_active():
                neighbors.setdefault(lev_dist, set()).add(current_node.get_value())

            for node_distance, ptr_node in current_node.get_links().items():
                if (
                    (lev_dist - max_distance)
                    <= node_distance
                    <= (lev_dist + max_distance)
                ):
                    stack.append(ptr_node)

        return neighbors

    def has_node(self, string: str) -> bool:
        """
        Check if the node exists in the tree

        Args:
            string (str): the name of the node

        Returns:
            bool: True if the string is associated to a node, False otherwise

        Example:
        >>> tree.has_node("cake")
        True

        >>> tree.has_ndoe("cacke")
        False
        """
        return string in self._bk_nodes_dict

    def add_node(self, string: str):
        """
        Add the node in the correct position in the tree based on the Levensthein distance

        Args:
            string (str): the string to add to the tree

        Raises:
            ValueError: if the string already exists

        Example:
        >>> tree.add_node("bakery")
        """
        if self.has_node(string):
            raise ValueError(f"The string {string} already exists in the tree")

        lev_dist: int
        bk_node: BKNode = BKNode(string)

        self._bk_nodes_dict[string] = bk_node

        current_bk_node: BKNode = self._root
        while True:
            lev_dist = levenshtein_distance(
                current_bk_node.get_value(),
                bk_node.get_value(),
                fn_weights=self._fn_weights if self._fn_weights is not None else None,
            )

            if not current_bk_node.has_distance(lev_dist):
                current_bk_node.add_link(lev_dist, bk_node)
                break
            else:
                current_bk_node = current_bk_node.get_link(lev_dist)

    def suggest_correction(self, string: str) -> str | None:
        """
        Return the most similar word from the given string

        Args:
            string (str): the string to search similar strings

        Returns:
            (str | None): None in case the string already exists (distance 0) or there are no similar strings, otherwise one string between the one's with less edit distance

        Example:
        >>>tree.suggest_correction("Cake")
        'cake'
        """
        if self.has_node(string) and self[string].is_active():
            return None

        suggestions = self.get_neighbors(
            string, max_distance=max(round(len(string) / 5) + 1, 2)
        )

        if not suggestions:
            return None

        best_suggestions_list: list[str] = list(suggestions[min(suggestions.keys())])
        best_suggestions_list.sort()

        return best_suggestions_list[0]

    def to_dict(
        self,
    ) -> dict[str, str | list[dict[str, str | bool | list[dict[str, int | str]]]]]:
        """
        Return the istance as a string in json format

        Returns:
            dict[str, str | list[dict[str, str | bool | list[dict[str, int | str]]]]]: the tree as dictionary

        Example:
        {
          'root':'node',
          'nodes':[
            {
              "value":"node",
              "is_active":True,
              "links":[
                {"distance":"2", "Node":"subnode"},
                {"distance":"1", "Node":"other_subnode"}
              ]
            }
          ]
        }

        """
        return {
            "root": self._root.get_value(),
            "nodes": [node.to_dict() for node in self._bk_nodes_dict.values()],
        }

    def dumps(self, indent: int = 2) -> str:
        """
        Return the istance as a string in json format

        Args:
            indent (int) = 2: Number of spaces used for indentation

        Returns:
            str: the instance as a string in json format

        Example:
        >>> print(bk_tree.dumps(indent = 2))
        {
          'root':'node',
          'nodes':[
            {
              "value":"node",
              "is_active":true,
              "links":[
                {"distance":"2", "Node":"subnode"},
                {"distance":"1", "Node":"other_subnode"}
              ]
            }
          ]
        }

        """
        return json.dumps(self.to_dict(), indent=indent)

    def dump(self, ptr_file, indent: int = 0):
        """
        Write the istance in the given file in json format

        Args:
            ptr_file (SupportsWrite[str]): the file to write the istance
            indent (int) = 0: the number of spaces for the indentation

        Example:
        >>> with open("bk_tree.json", "w+") as file:
        ...   tree.dump(file, indent=2)
        """
        json.dump(self.to_dict(), ptr_file, indent=indent)


@BKTree.register_builder("from_set")
def bk_tree_builder_from_set(
    strings_set: set[str], fn_weights: Callable | None = None
) -> BKTree:
    """
    Builder for the class BKTree, giving a set of string return a BK-tree

    Args:
        strings_set (str): a set of string
        fn_weights (Callable | None): the fn_weights used

    Returns:
        BKTree: a BK-tree populated with the string in the set

    Raises:
        ValueError: if the set is empty

    Example:
        >>> BKTree.build("from_set", {"book", "cake", "bed"}
    """
    if not strings_set:
        raise ValueError(
            "Argument `strings_set` expected to have at least 1 element, got 0 elements"
        )

    root: BKNode = BKNode(strings_set.pop())
    bk_tree: BKTree = BKTree(root, {root.get_value(): root}, fn_weights=fn_weights)

    for string in strings_set:
        bk_tree.add_node(string)

    return bk_tree


@BKTree.register_builder("from_json")
def bk_tree_builder_from_json(ptr_file, fn_weights: Callable | None = None) -> BKTree:
    """
    Builder for the class BKTree, giving a json file return a BK-tree

    Args:
        ptr_file (SupportsRead[str | bytes]): the pointer to the json file
        fn_weights (Callable | None): the fn_weights used

    Returns:
        BKTree: a BK-tree populated as specified in the file

    Example:
    >>> with open("file.json") as file:
    ...   BKTree.build("from_json", file)
    """
    bk_tree_dict: dict[
        str, str | list[dict[str, str | bool | list[dict[str, str]]]]
    ] = json.load(ptr_file)

    return BKTree.build("from_dict", bk_tree_dict, fn_weights=fn_weights)


@BKTree.register_builder("from_dict")
def bk_tree_builder_from_dict(
    bk_tree_dict: dict[str, str | bool | list[dict[str | int, str]]],
    fn_weights: Callable | None = None,
) -> BKTree:
    """
    Builder for the class BKTree, giving a dictionary return a BK-tree

    Args:
        bk_tree_dict (dict[str, str | bool | list[str | int, str]]]): the dictionary with the structure of the BK-tree
        fn_weights (Callable | None): the fn_weights used

    Returns:

        BKTree: a BK-tree populated as specified in the dictionary

    Raises:
        ValueError: if the dictionary is empty
        KeyError: if a node is defined as link but not as a node

    Example:
    >>> BKTree.build("from_dict", {"root":"cake", "nodes":[{"value":"cake", "is_active":"true", "links":{}]}
    """
    if not bk_tree_dict:
        raise ValueError("The argument `bk_tree_dict` is empty!")

    bk_nodes_dict: dict[str, BKNode] = {
        node["value"]: BKNode(node["value"], is_active=node["is_active"])
        for node in bk_tree_dict["nodes"]
    }

    root: BKNode = bk_nodes_dict[bk_tree_dict["root"]]

    node_value: str = ""

    for node_dict in bk_tree_dict["nodes"]:
        node_value = node_dict["value"]

        for distance, node in node_dict["links"].items():
            if node not in bk_nodes_dict:
                raise KeyError(f"Subnode `{node}` not defined as node")

            bk_nodes_dict[node_value].add_link(int(distance), bk_nodes_dict[node])

    return BKTree(root, bk_nodes_dict, fn_weights=fn_weights)


@BKTree.register_builder("from_file")
def bk_tree_builder_from_file(
    ptr_file, delimiter: str = ",", fn_weights: Callable | None = None
) -> BKTree:
    """
    Builder for the class BKTree, giving a file return a BK-tree

    Args:
        ptr_file (SupportsRead[str | bytes]): pointer to the file with the strings
        delimiter (str) = ",": the delimiter to separate the strings
        fn_weights (Callable | None): the fn_weights used

    Returns:
        BKTree: a BK-tree populated with the strings in the file

    Example:
    >>> with open("words.tst") as file:
    ...   BKTree.build("from_file", file, delimiter=";")
    """
    return BKTree.build(
        "from_set", set(ptr_file.read().split(delimiter)), fn_weights=fn_weights
    )
