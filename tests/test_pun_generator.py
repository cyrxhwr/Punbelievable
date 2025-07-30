#!/usr/bin/env python3
"""
Comprehensive test suite for the Pun Generator project.
"""

import unittest
import sys
import os
import json
import csv
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from schemata import Lotus
from templates import GrammaticalTemplate
from generate_dataset import PunDatasetGenerator


class TestLotus(unittest.TestCase):
    """Test cases for the main Lotus class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.lotus = Lotus()
    
    def test_initialization(self):
        """Test Lotus class initialization."""
        self.assertIsNotNone(self.lotus)
        self.assertIsNotNone(self.lotus.nplist)
        self.assertEqual(self.lotus.found_puns, [])
    
    def test_semantic_similarity(self):
        """Test semantic similarity calculation."""
        # Test similar words
        sim = self.lotus.semantic_similarity("food", "meal")
        self.assertGreater(sim, 0.0)
        self.assertLessEqual(sim, 1.0)
        
        # Test unrelated words
        sim = self.lotus.semantic_similarity("food", "computer")
        self.assertLess(sim, 0.5)
    
    def test_find_related_words(self):
        """Test finding related words."""
        related = self.lotus.find_related_words("food")
        self.assertIsInstance(related, list)
        self.assertGreater(len(related), 0)
    
    def test_generate_themed_pun(self):
        """Test themed pun generation."""
        lotus = Lotus("food")
        # Should not raise an exception
        self.assertIsNotNone(lotus)


class TestGrammaticalTemplate(unittest.TestCase):
    """Test cases for the GrammaticalTemplate class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.template = GrammaticalTemplate()
    
    def test_initialization(self):
        """Test GrammaticalTemplate initialization."""
        self.assertIsNotNone(self.template)
        self.assertIsNotNone(self.template.lemmatizer)
    
    def test_find_verb_form_automatic(self):
        """Test automatic verb form detection."""
        # Test -ing form
        result = self.template._find_verb_form_automatic("meeting")
        self.assertIsInstance(result, str)
        
        # Test noun to verb conversion
        result = self.template._find_verb_form_automatic("teacher")
        self.assertIsInstance(result, str)
    
    def test_conjugate_verb_automatic(self):
        """Test automatic verb conjugation."""
        # Test regular verb
        result = self.template._conjugate_verb_automatic("run")
        self.assertEqual(result, "runs")
        
        # Test irregular verb
        result = self.template._conjugate_verb_automatic("be")
        self.assertEqual(result, "is")
        
        # Test verb ending in y
        result = self.template._conjugate_verb_automatic("try")
        self.assertEqual(result, "tries")


class TestPunDatasetGenerator(unittest.TestCase):
    """Test cases for the PunDatasetGenerator class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.generator = PunDatasetGenerator()
    
    def test_initialization(self):
        """Test PunDatasetGenerator initialization."""
        self.assertIsNotNone(self.generator)
        self.assertEqual(self.generator.dataset, [])
        self.assertEqual(self.generator.successful_puns, 0)
        self.assertEqual(self.generator.failed_themes, [])
    
    def test_capture_pun_output(self):
        """Test pun output capture."""
        question, answer = self.generator.capture_pun_output("food")
        # Should return either valid output or None
        if question is not None:
            self.assertIsInstance(question, str)
            self.assertIsInstance(answer, str)
            self.assertIn("What do you call", question)


class TestDatasetFiles(unittest.TestCase):
    """Test cases for dataset file integrity."""
    
    def test_csv_dataset_exists(self):
        """Test that CSV dataset files exist."""
        csv_files = [
            "data/pun_dataset_100.csv",
            "data/pun_dataset_expanded.csv"
        ]
        for file_path in csv_files:
            self.assertTrue(os.path.exists(file_path), f"File {file_path} does not exist")
    
    def test_json_dataset_exists(self):
        """Test that JSON dataset files exist."""
        json_files = [
            "data/pun_dataset_100.json",
            "data/pun_dataset_expanded.json"
        ]
        for file_path in json_files:
            self.assertTrue(os.path.exists(file_path), f"File {file_path} does not exist")
    
    def test_csv_format(self):
        """Test CSV dataset format."""
        csv_file = "data/pun_dataset_100.csv"
        if os.path.exists(csv_file):
            with open(csv_file, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                self.assertIn('theme_word', reader.fieldnames)
                self.assertIn('question', reader.fieldnames)
                self.assertIn('answer', reader.fieldnames)
    
    def test_json_format(self):
        """Test JSON dataset format."""
        json_file = "data/pun_dataset_100.json"
        if os.path.exists(json_file):
            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.assertIsInstance(data, list)
                if data:
                    self.assertIn('theme_word', data[0])
                    self.assertIn('question', data[0])
                    self.assertIn('answer', data[0])


class TestDocumentation(unittest.TestCase):
    """Test cases for documentation files."""
    
    def test_readme_exists(self):
        """Test that README.md exists."""
        self.assertTrue(os.path.exists("README.md"))
    
    def test_license_exists(self):
        """Test that LICENSE file exists."""
        self.assertTrue(os.path.exists("LICENSE"))
    
    def test_requirements_exists(self):
        """Test that requirements.txt exists."""
        self.assertTrue(os.path.exists("requirements.txt"))
    
    def test_setup_exists(self):
        """Test that setup.py exists."""
        self.assertTrue(os.path.exists("setup.py"))


def run_tests():
    """Run all tests."""
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add test cases
    test_classes = [
        TestLotus,
        TestGrammaticalTemplate,
        TestPunDatasetGenerator,
        TestDatasetFiles,
        TestDocumentation
    ]
    
    for test_class in test_classes:
        tests = loader.loadTestsFromTestCase(test_class)
        suite.addTests(tests)
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return result.wasSuccessful()


if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1) 