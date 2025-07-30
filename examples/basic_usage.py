#!/usr/bin/env python3
"""
Basic usage example for the Pun Generator.

This script demonstrates how to use the pun generator to create themed puns.
"""

import sys
import os

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from schemata import Lotus
from templates import GrammaticalTemplate


def demonstrate_basic_usage():
    """Demonstrate basic usage of the pun generator."""
    print("🎭 Enhanced Pun Generator - Basic Usage Example")
    print("=" * 50)
    
    # Example 1: Generate a themed pun
    print("\n1. Generating a themed pun:")
    print("-" * 30)
    
    theme_word = "food"
    print(f"Theme: {theme_word}")
    
    lotus = Lotus(theme_word)
    print("✓ Pun generated successfully!")
    
    # Example 2: Test grammar correction
    print("\n2. Testing grammar correction:")
    print("-" * 30)
    
    template = GrammaticalTemplate()
    
    test_words = ["meeting", "teacher", "running", "computing"]
    for word in test_words:
        verb_form = template._find_verb_form_automatic(word)
        print(f"'{word}' → '{verb_form}'")
    
    # Example 3: Test semantic similarity
    print("\n3. Testing semantic similarity:")
    print("-" * 30)
    
    word_pairs = [
        ("food", "meal"),
        ("computer", "machine"),
        ("music", "song"),
        ("food", "computer")  # Unrelated pair
    ]
    
    for word1, word2 in word_pairs:
        similarity = lotus.semantic_similarity(word1, word2)
        print(f"Similarity between '{word1}' and '{word2}': {similarity:.3f}")
    
    # Example 4: Find related words
    print("\n4. Finding related words:")
    print("-" * 30)
    
    test_theme = "music"
    related_words = lotus.find_related_words(test_theme)
    print(f"Words related to '{test_theme}':")
    for i, word in enumerate(related_words[:10], 1):  # Show first 10
        print(f"  {i}. {word}")
    print(f"  ... and {len(related_words) - 10} more words")


def demonstrate_dataset_generation():
    """Demonstrate dataset generation capabilities."""
    print("\n" + "=" * 50)
    print("📊 Dataset Generation Example")
    print("=" * 50)
    
    from generate_dataset import PunDatasetGenerator
    
    # Create a small test dataset
    test_themes = ["food", "music", "sports", "technology"]
    
    print(f"Generating puns for {len(test_themes)} test themes...")
    
    generator = PunDatasetGenerator()
    generator.generate_dataset(test_themes)
    
    print(f"\nResults:")
    print(f"- Successful puns: {generator.successful_puns}")
    print(f"- Failed themes: {len(generator.failed_themes)}")
    
    if generator.dataset:
        print(f"\nSample puns generated:")
        for i, pun in enumerate(generator.dataset[:3], 1):
            print(f"{i}. Theme: {pun['theme_word']}")
            print(f"   Q: {pun['question']}")
            print(f"   A: {pun['answer']}")
            print()


def main():
    """Main function to run the examples."""
    try:
        demonstrate_basic_usage()
        demonstrate_dataset_generation()
        
        print("\n" + "=" * 50)
        print("✅ All examples completed successfully!")
        print("=" * 50)
        
    except Exception as e:
        print(f"\n❌ Error running examples: {str(e)}")
        print("Make sure you have installed all dependencies:")
        print("  pip install -r requirements.txt")
        print("  python -c \"import nltk; nltk.download('wordnet'); nltk.download('brown'); nltk.download('cmudict'); nltk.download('punkt'); nltk.download('averaged_perceptron_tagger')\"")


if __name__ == "__main__":
    main() 