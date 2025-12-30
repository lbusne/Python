from typing import Callable


def levenshtein_distance(
    s1: str,
    s2: str,
    max_distance: int | None = None,
    fn_weights: Callable | None = None,
    case_sensitive: bool = True,
) -> int:
    """
    Calculate the distance between two strings, based on number of substitutions, deletions and insertions.
    If the weight function is given it will calculate the substitution distance based on the function.

    Args:
        s1 (str): First string to compare
        s2 (str): Second string to compare
        max_distance (int | None) = None: the max distance allowed, if the distance is more the function will stop immedialty
        fn_weights (Callable | None) = None: the function to calculate the weight of the substitution
        case_sensitive (bool) = True: enable or disable the case sensitive during the comparison

    Returns:
        int: The distance between s1 and s2

    Raises:
        TypeError: if s1 or s2 are not str

    Example:
        >>> levenshtein_distance("cake", "Cake")
        1
        >>> levenshtein_distance("cake", "cackeees", is_bound=True, max_distance=2)
        2 # actual levenshtein distance is 3
        >>> levenshtein_distance("cake", "Cake", case_sensitive=False)
        0
    """

    if not isinstance(s1, str) or not isinstance(s2, str):
        raise TypeError(
            f"Argument `s1` and `s2` expected to be str, got `s1`: {type(s1).__name__}, `s2`: {type(s2).__name__}"
        )

    if not case_sensitive:
        s1 = s1.casefold()
        s2 = s2.casefold()

    if not s1 or not s2:
        return max(len(s1), len(s2))
    elif s1 == s2:
        return 0
    elif len(s1) < len(s2):
        s1, s2 = s2, s1

    current_distances: list[int] = list(range(len(s2) + 1))
    min_row_distance: int = current_distances[0]

    for idx_s1, val_s1 in enumerate(s1):
        previous_distances = current_distances
        current_distances = [
            idx_s1 + 1,
        ]

        min_row_distance = current_distances[0]

        for idx_s2, val_s2 in enumerate(s2):
            current_distances.append(
                previous_distances[idx_s2]
                if val_s1 == val_s2
                else min(
                    previous_distances[idx_s2]
                    + (
                        fn_weights(val_s1, val_s2) if fn_weights is not None else 1
                    ),  # Substitution
                    previous_distances[1 + idx_s2] + 1,  # Insertion
                    current_distances[idx_s2] + 1,  # Deletion
                )
            )

            min_row_distance = min(min_row_distance, current_distances[-1])

        if max_distance is not None and min_row_distance >= max_distance:
            return min_row_distance

    return current_distances[-1]


def euclidean_distance(p1: tuple[float, float], p2: tuple[float, float]) -> float:
    """
    Calculated the euclidean distance between two points

    Args:
        p1 (tuple[float, float]): the first point
        p2 (tuple[float, float]): the second point

    Returns:
        float: the euclidean distance between the points

    Example:
    >>> euclidean_distance((1.0, 1.0), (2.5, 4.5))
    3.807886...
    """
    return ((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2) ** 0.5
