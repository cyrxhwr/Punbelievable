"""
Pun Generator Package

A Natural Language Processing project for generating semantically relevant puns
with automatic grammatical correction.

This package provides:
- Semantic similarity-based pun generation
- Automatic morphological processing
- Theme-relevant compound noun discovery
- Dataset generation and validation tools
"""

__version__ = "1.0.0"
__author__ = "CS372 Student"
__email__ = "student@university.edu"

from .schemata import Lotus
from .templates import GrammaticalTemplate
from .generate_dataset import PunDatasetGenerator

__all__ = [
    "Lotus",
    "GrammaticalTemplate", 
    "PunDatasetGenerator"
] 