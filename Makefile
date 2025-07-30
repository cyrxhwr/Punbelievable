# Makefile for Pun Generator Project

.PHONY: help install test clean lint format docs run-example generate-dataset

# Default target
help:
	@echo "Available commands:"
	@echo "  install        - Install dependencies"
	@echo "  test           - Run all tests"
	@echo "  lint           - Run linting checks"
	@echo "  format         - Format code with black"
	@echo "  clean          - Clean up generated files"
	@echo "  docs           - Generate documentation"
	@echo "  run-example    - Run basic usage example"
	@echo "  generate-dataset - Generate new dataset"
	@echo "  install-dev    - Install development dependencies"

# Install dependencies
install:
	pip install -r requirements.txt
	python -c "import nltk; nltk.download('wordnet'); nltk.download('brown'); nltk.download('cmudict'); nltk.download('punkt'); nltk.download('averaged_perceptron_tagger')"

# Install development dependencies
install-dev: install
	pip install -r requirements.txt[dev]

# Run tests
test:
	python -m pytest tests/ -v

# Run linting
lint:
	flake8 src/ tests/ --max-line-length=88 --ignore=E203,W503
	mypy src/ --ignore-missing-imports

# Format code
format:
	black src/ tests/ --line-length=88

# Clean up generated files
clean:
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	rm -rf build/ dist/ .pytest_cache/ .coverage htmlcov/

# Generate documentation
docs:
	sphinx-build -b html docs/ docs/_build/html

# Run basic usage example
run-example:
	python examples/basic_usage.py

# Generate new dataset
generate-dataset:
	python src/generate_dataset.py

# Run pun generator interactively
run-generator:
	python src/schemata.py

# Check project structure
check-structure:
	@echo "Checking project structure..."
	@test -f README.md || echo "❌ README.md missing"
	@test -f requirements.txt || echo "❌ requirements.txt missing"
	@test -f setup.py || echo "❌ setup.py missing"
	@test -f LICENSE || echo "❌ LICENSE missing"
	@test -f .gitignore || echo "❌ .gitignore missing"
	@test -d src || echo "❌ src/ directory missing"
	@test -d tests || echo "❌ tests/ directory missing"
	@test -d data || echo "❌ data/ directory missing"
	@test -d docs || echo "❌ docs/ directory missing"
	@echo "✅ Project structure check complete"

# Full development setup
setup-dev: install-dev check-structure format lint test
	@echo "✅ Development environment setup complete!"

# Quick development cycle
dev-cycle: format lint test
	@echo "✅ Development cycle complete!" 