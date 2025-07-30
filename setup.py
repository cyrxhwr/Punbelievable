#!/usr/bin/env python3
"""
Setup script for Pun Generator package.
"""

from setuptools import setup, find_packages
import os

# Read the README file
def read_readme():
    with open("README.md", "r", encoding="utf-8") as fh:
        return fh.read()

# Read requirements
def read_requirements():
    with open("requirements.txt", "r", encoding="utf-8") as fh:
        return [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="pun-generator",
    version="1.0.0",
    author="CS372 Student",
    author_email="student@university.edu",
    description="Enhanced Pun Generator with semantic similarity and grammatical correction",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/pun-generator",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Education",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Text Processing :: Linguistic",
    ],
    python_requires=">=3.7",
    install_requires=read_requirements(),
    extras_require={
        "dev": [
            "pytest>=6.0.0",
            "pytest-cov>=2.10.0",
            "black>=21.0.0",
            "flake8>=3.8.0",
            "mypy>=0.910",
        ],
        "docs": [
            "sphinx>=4.0.0",
            "sphinx-rtd-theme>=0.5.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "pun-generator=src.schemata:main",
            "generate-dataset=src.generate_dataset:main",
        ],
    },
    include_package_data=True,
    package_data={
        "": ["*.txt", "*.csv", "*.json"],
    },
    keywords="nlp, puns, humor, wordnet, semantic-similarity, morphological-processing",
    project_urls={
        "Bug Reports": "https://github.com/yourusername/pun-generator/issues",
        "Source": "https://github.com/yourusername/pun-generator",
        "Documentation": "https://github.com/yourusername/pun-generator#readme",
    },
) 