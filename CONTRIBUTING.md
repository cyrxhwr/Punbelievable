# Contributing to Pun Generator

Thank you for your interest in contributing to the Pun Generator project! This document provides guidelines and information for contributors.

## 🚀 Quick Start

1. **Fork the repository**
2. **Clone your fork**
   ```bash
   git clone https://github.com/yourusername/pun-generator.git
   cd pun-generator
   ```
3. **Set up development environment**
   ```bash
   make install-dev
   ```
4. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

## 📋 Development Guidelines

### Code Style

We follow PEP 8 style guidelines with some modifications:

- **Line length**: 88 characters (Black default)
- **Import organization**: Standard library, third-party, local imports
- **Docstrings**: Google style docstrings
- **Type hints**: Use type hints for function parameters and return values

### Code Formatting

We use [Black](https://black.readthedocs.io/) for code formatting:

```bash
make format
```

### Linting

We use [flake8](https://flake8.pycqa.org/) for linting:

```bash
make lint
```

### Testing

Write tests for all new features and bug fixes:

```bash
make test
```

## 🧪 Testing Guidelines

### Writing Tests

1. **Test structure**: Use `unittest.TestCase` or `pytest`
2. **Test naming**: Use descriptive test method names
3. **Test coverage**: Aim for >80% code coverage
4. **Test isolation**: Each test should be independent

### Example Test

```python
def test_semantic_similarity(self):
    """Test semantic similarity calculation."""
    lotus = Lotus()
    similarity = lotus.semantic_similarity("food", "meal")
    self.assertGreater(similarity, 0.0)
    self.assertLessEqual(similarity, 1.0)
```

## 📝 Documentation

### Code Documentation

- **Docstrings**: All public functions and classes should have docstrings
- **Comments**: Add comments for complex logic
- **Type hints**: Use type hints for better code understanding

### Example Docstring

```python
def semantic_similarity(self, word1: str, word2: str) -> float:
    """Calculate semantic similarity between two words.
    
    Args:
        word1: First word for comparison
        word2: Second word for comparison
        
    Returns:
        float: Similarity score between 0.0 and 1.0
        
    Raises:
        ValueError: If either word is empty or None
    """
```

## 🔄 Pull Request Process

1. **Create a feature branch** from `main`
2. **Make your changes** following the guidelines above
3. **Write tests** for your changes
4. **Update documentation** if needed
5. **Run the full test suite**
   ```bash
   make dev-cycle
   ```
6. **Submit a pull request** with a clear description

### Pull Request Template

```markdown
## Description
Brief description of the changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Documentation update
- [ ] Test addition
- [ ] Refactoring

## Testing
- [ ] All tests pass
- [ ] New tests added for new functionality
- [ ] Code coverage maintained or improved

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Documentation updated
- [ ] No breaking changes
```

## 🐛 Bug Reports

When reporting bugs, please include:

1. **Environment details**: Python version, OS, dependencies
2. **Steps to reproduce**: Clear, step-by-step instructions
3. **Expected behavior**: What you expected to happen
4. **Actual behavior**: What actually happened
5. **Error messages**: Full error traceback if applicable

## 💡 Feature Requests

When requesting features, please include:

1. **Problem description**: What problem does this solve?
2. **Proposed solution**: How should it work?
3. **Use cases**: Examples of how it would be used
4. **Alternatives considered**: Other approaches you've considered

## 🏷️ Issue Labels

We use the following labels for issues:

- `bug`: Something isn't working
- `enhancement`: New feature or request
- `documentation`: Improvements or additions to documentation
- `good first issue`: Good for newcomers
- `help wanted`: Extra attention is needed
- `question`: Further information is requested

## 📊 Performance Guidelines

When contributing performance-related changes:

1. **Benchmark**: Measure performance before and after
2. **Profile**: Use profiling tools to identify bottlenecks
3. **Test**: Ensure changes don't break existing functionality
4. **Document**: Document performance improvements

## 🔒 Security

If you discover a security vulnerability:

1. **Don't open a public issue**
2. **Email**: security@yourdomain.com
3. **Include**: Detailed description and reproduction steps
4. **Wait**: For acknowledgment and resolution

## 📚 Resources

- [Python Style Guide (PEP 8)](https://www.python.org/dev/peps/pep-0008/)
- [Google Python Style Guide](https://google.github.io/styleguide/pyguide.html)
- [NLTK Documentation](https://www.nltk.org/)
- [WordNet Documentation](https://wordnet.princeton.edu/)

## 🤝 Community

- **Be respectful**: Treat all contributors with respect
- **Be helpful**: Help others learn and grow
- **Be patient**: Everyone learns at their own pace
- **Be constructive**: Provide constructive feedback

## 📞 Contact

- **Issues**: [GitHub Issues](https://github.com/yourusername/pun-generator/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/pun-generator/discussions)
- **Email**: project@yourdomain.com

Thank you for contributing to the Pun Generator project! 🎭 