import json


class Node:
    def __init__(
        self,
        value: str,
        links: dict[int, "Node"] | None = None,
        is_active: bool = True,
    ):
        """
        Initialize the istance

        Args:
            value (str): the value of the node
            links (dict[int | Node] | None) = None: the edges of the node
            is_active (bool): the status of the node
        """
        self._value: str = value
        self._is_active: bool = is_active
        self._links: dict[int, "Node"] = {} if links is None else links

    def __repr__(self) -> str:
        """
        Return the representation of the node

        Example:
        >>> print(node)
        Node: node
        Is Active: Y
        Links:
          Distance: 1, Node: nodes
          Distance: 2, Node: NodeS
        """

        class_output: list[str] = [
            f"Node: {self._value}",
            f"\nIs Active: {'Y' if self._is_active else 'N'}",
        ]
        distances: list[int] = []

        if self._links:
            class_output.append("\nLinks:")

            distances = list(self._links.keys())
            distances.sort()

            for distance in distances:
                class_output.append(
                    f"\n  Distance: {distance}, Node: {self.get_link(distance).get_value()}"
                )

        return "".join(class_output)

    def get_value(self) -> str:
        """
        Return the value of the node

        Returns:
            str: The value of the node

        Example:
            >>> node.get_value()
            'books'
        """
        return self._value

    def get_links(self) -> dict[int, "Node"]:
        """
        Return a copy of the dictionary with the distances as keys and the pointer to the respective node as value

        Returns:
            dict[int, Node]: The copy of the dictionary with the links and the distance from the actual node

        Example:
            >>> node.get_links()
            {'1': <__module_name__ object at <memory address>, '4': <__module_name__ object at <memory address>}
        """
        return self._links.copy()

    def get_link(self, distance: int) -> "Node":
        """
        Return the node with the distance passed as argument

        Args:
            distance (int): the distance of the node to get

        Returns:
            Node: the node with the distance requested

        Raises:
            KeyError: if the distance not exists

        Example:
        >>> node.get_link(10)
        <__module_name__ object at <memory address>
        """

        if self.has_distance(distance):
            return self._links[distance]
        else:
            raise KeyError(f"The distance {distance} not exists")

    def is_active(self) -> bool:
        """
        Return `True` if the node is active, otherwise return `False`

        Returns:
            bool: The state of the node

        Example:
            >>> node.is_active()
            True
        """
        return self._is_active

    def has_distance(self, distance: int) -> bool:
        """
        Check if the node has a child node with the given distance and return `True`, otherwise return `False`

        Args:
            distance (int): The distance to check in the list of children

        Returns:
            bool: `True` in case a child with the same distance, otherwise return `False`

        Example:
            >>> node.has_distance(10)
            False
        """
        return distance in self._links

    def set_active(self):
        """
        Set the state of the node active

        Example:
            >>> node.set_active()
        """
        self._is_active = True

    def set_inactive(self):
        """
        Set the state of the node disactive

        Example:
            >>> node.set_inactive()
        """
        self._is_active = False

    def add_link(self, distance: int, node: "Node"):
        """
        Add a link to a child node

        Args:
            distance (int): The distance between the current node and the node to add
            node (node): The pointer to the node

        Raises:
            KeyError: if already exists a node with the same distance

        Example:
            >>> node.add_link(1, Node("test"))
        """

        if self.has_distance(distance):
            raise KeyError(
                f"The same node cannot have multiple links with the same distance, distance {distance} already exists"
            )
        else:
            self._links[distance] = node

    def del_link(self, distance: int):
        """
        Remove the link to the child node based on the given distance

        Args:
            distance (int): The distance to be removed

        Raises:
            KeyError: if not exists a node with the distance given

        Example:
            >>> node.del_link(10)
        """

        if self.has_distance(distance):
            del self._links[distance]
        else:
            raise KeyError(f"The distance {distance} not exists")

    def clear_links(self):
        """
        Clear the links of the child nodes
        """
        self._links.clear()

    def to_dict(self) -> dict[str, str | bool | dict[str, int | str]]:
        """
        Convert the node in a dictionary format

        Returns:
            dict[str, str | bool | list[dict[str, int | str]]]: the node in a dictionary format

        Example:
        >>> node.to_dict()
        {
          'value':'node',
          'is_active':true,
          'links':[
            {'distance':1, 'Node': 'nodes'},
            {'distance':4, 'Node': 'node_abc'}
          ]
        }
        """

        return {
            "value": self._value,
            "is_active": self._is_active,
            "links": {
                distance: link.get_value() for distance, link in self._links.items()
            },
        }

    def dumps(self, indent: int = 2) -> str:
        """
        Return the istance as a string in json format

        Args:
            indent (int) = 2: Number of spaces used for the indentation

        Returns:
            str: the istance in json format

        Example:
        >>> node.dump()
        {
          "value":"node",
          "is_active":true,
          "links":[
            {"distance":"2", "Node":"subnode"},
            {"distance":"1", "Node":"other_subnode"}
          ]
        }
        """

        return json.dumps(self.to_dict(), indent=indent)
