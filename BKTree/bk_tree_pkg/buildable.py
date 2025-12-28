from typing import Callable


class Buildable:
    _BUILDERS: dict[str, Callable] = {}

    def __init_subclass__(cls, **kwargs):
        # Continue the chan of inheritance calling the next class that extend
        super().__init_subclass__(**kwargs)
        # Set the global dictionary _BUILDERS to empty for each class that extend this class
        cls._BUILDERS = {}

    @classmethod
    def register_builder(cls, func_name: str) -> Callable:
        """
        Register the string given as argument in the decorator as name of the function and add the function in the dictionary

        Args:
            func_name (str): the name of the function

        Returns:
            Callable: the function

        Example:
        @Class_1.build("from_json")
        def class_1_builder_from_json(ptr_file) -> Class_1:
          ...

        """

        def decorator(func: Callable) -> Callable:
            """
            Add a function in the dictionary under the key passed as argument in the decorator

            Args:
                func (Callable): a function

            Returns:
                Callable: a function

            Example:
            @Class_1.build("from_json")
            def class_1_builder_from_json(ptr_file) -> Class_1:
              ...
            """
            cls._BUILDERS[func_name] = func

            return func

        return decorator

    @classmethod
    def build(cls, func_name: str, *args, **kwargs) -> Callable:
        """
        Call the builder class for the class

        Args:
            func_name (str): the name of the function to call
            *args: the args of the function
            **kwargs: the keyword arguments of the function

        Returns:
            The requested function

        Raises:
            ValueError: if the function is not defined

        Example:
        >>> Class_1.build("from_set", {"cake", "books", "cook"})
        >>> Class_2.build("from_dict", {"a": (0, 0), "b": (5, 5), "z":(-1, 5)}
        """
        if func_name not in cls._BUILDERS:
            raise ValueError(f"Builder method '{func_name}' not defined")

        return cls._BUILDERS[func_name](*args, **kwargs)
