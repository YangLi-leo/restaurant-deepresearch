# Contributing to Restaurant Deep Research

Thank you for considering contributing to Restaurant Deep Research! This document provides guidelines and instructions for contributing to this project.

## Code of Conduct

By participating in this project, you agree to abide by our code of conduct:

- Be respectful and inclusive
- Provide constructive feedback
- Focus on what is best for the community
- Show empathy towards other community members

## How Can I Contribute?

### Reporting Bugs

Before creating bug reports, please check the existing issues to see if the problem has already been reported. When you are creating a bug report, please include as many details as possible:

- A clear and descriptive title
- Steps to reproduce the issue
- Expected behavior
- Actual behavior
- Screenshots (if applicable)
- Environment details (OS, Python version, etc.)

### Suggesting Enhancements

Enhancement suggestions are tracked as GitHub issues. When creating an enhancement suggestion, please include:

- A clear and descriptive title
- A detailed description of the proposed functionality
- Any potential implementation approaches you have in mind
- Why this enhancement would be useful to most users

### Pull Requests

1. Fork the repository
2. Create a new branch from `main` (`git checkout -b feature/your-feature-name`)
3. Make your changes
4. Add or update tests as needed
5. Run tests and make sure they pass
6. Update documentation if necessary
7. Commit your changes with clear commit messages
8. Push to your branch
9. Submit a pull request to the `main` branch

#### Pull Request Process

1. Update the README.md or documentation with details of changes if needed
2. Make sure your code follows the project's style guidelines
3. The PR should work for Python 3.8+
4. PRs will be merged once they have been reviewed and approved

## Development Setup

1. Fork and clone the repository
2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```
3. Install development dependencies:
   ```bash
   pip install -e ".[dev]"
   ```
4. Set up environment variables:
   ```bash
   cp .env.example .env
   # Edit .env with your API keys
   ```

## Style Guidelines

- Follow PEP 8 style guide for Python code
- Use meaningful variable and function names
- Write docstrings for all functions, classes, and modules
- Keep code modular and maintain separation of concerns
- Include type hints where appropriate

## Testing

- Write tests for new features and bug fixes
- Run tests before submitting a PR
- Aim to maintain or increase test coverage

## Documentation

- Update documentation for any changes to the API or functionality
- Write clear, concise documentation that is accessible to users
- Include examples where appropriate

Thank you for your contributions!
