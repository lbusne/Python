"""
BK-Tree Package

Implementation of the Burkhard-Keller metric Tree for an efficient fuzzy string matching.
The metric is calculated by the Levenshtein algorithm, with support for the weighted distances.
"""

__version__ = "0.0.1"
__author__ = "Luca Busnelli"

from .bk_tree import BKTree
from .keyboard import Keyboard
from .node import Node
from .functions import levenshtein_distance, euclidean_distance

__all__ = ["BKTree", "Keyboard", "Node", "levenshtein_distance", "euclidean_distance"]
