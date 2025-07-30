#!/usr/bin/env python3
"""
Test script for the dataset generator
"""

from generate_dataset import PunDatasetGenerator

def test_dataset_generator():
    """Test the dataset generator with a few theme words."""
    test_words = ["food", "music", "sports", "computer", "cat"]
    
    generator = PunDatasetGenerator()
    generator.generate_dataset(test_words)
    
    if generator.dataset:
        print("\nGenerated puns:")
        for entry in generator.dataset:
            print(f"Theme: {entry['theme_word']}")
            print(f"Q: {entry['question']}")
            print(f"A: {entry['answer']}")
            print("-" * 40)
    
    return generator.successful_puns > 0

if __name__ == "__main__":
    success = test_dataset_generator()
    print(f"\nTest {'PASSED' if success else 'FAILED'}") 