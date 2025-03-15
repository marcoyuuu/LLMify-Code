# Contributing to LLMify-Code

Thank you for your interest in contributing to **LLMify-Code**! We welcome contributions that improve the project, fix bugs, or enhance its features. This document outlines the guidelines for contributing to ensure a smooth collaboration process.

---

## Table of Contents

- [How to Contribute](#how-to-contribute)
- [Reporting Bugs](#reporting-bugs)
- [Suggesting Enhancements](#suggesting-enhancements)
- [Pull Request Process](#pull-request-process)
- [Coding Guidelines](#coding-guidelines)
- [Commit Messages](#commit-messages)
- [License](#license)

---

## How to Contribute

Contributions to LLMify-Code can take many forms, including:

- **Bug Reports:** If you encounter any bugs, please check the [issue tracker](https://github.com/yourusername/LLMify-Code/issues) before opening a new issue.
- **Enhancements:** If you have suggestions for new features or improvements, please open an issue first to discuss your idea.
- **Code Contributions:** Fork the repository, make your changes, and submit a pull request. Ensure your changes adhere to the coding guidelines below.
- **Documentation:** Contributions to improve or update documentation, including this file, are always welcome.

---

## Reporting Bugs

When reporting a bug, please include:

- A **clear description** of the problem.
- **Steps to reproduce** the issue.
- The **expected behavior** and what actually happened.
- Information about your **environment** (OS, Python version, etc.).
- Any relevant **logs or screenshots**.

Please open an issue in the [issue tracker](https://github.com/yourusername/LLMify-Code/issues).

---

## Suggesting Enhancements

If you have an idea for a new feature or an improvement:

1. **Search** the existing issues to ensure it hasn’t already been suggested.
2. **Open a new issue** describing your idea in detail.
3. If you are comfortable with coding, consider opening a pull request with your proposed changes after discussing the idea.

---

## Pull Request Process

Before submitting a pull request (PR), please follow these steps:

1. **Fork** the repository and create your branch from `main`.
2. **Ensure** that your branch is up-to-date with the latest code.
3. **Write tests** for your changes, if applicable.
4. **Run all tests** to ensure nothing is broken.
5. **Document your changes** thoroughly.
6. **Submit a pull request** describing your changes, referencing any related issues.

A good PR description should include:
- **Context:** What problem does this PR address?
- **Solution:** How does the PR solve the problem?
- **Testing:** How have you tested the changes?
- **Impact:** Any potential impacts or backward-incompatible changes.

---

## Coding Guidelines

To maintain code quality, please adhere to the following guidelines:

- **Code Style:** Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/).
- **Documentation:** Write clear docstrings for functions and classes.
- **Testing:** Include unit tests for new functionality. Use `pytest` for running tests.
- **Linting:** Run [Pylint](https://pylint.org/) before submitting your code to ensure it meets our standards.

---

## Commit Messages

Please use clear and descriptive commit messages. Here’s a suggested format:

- **Title:** A short summary (less than 50 characters).
- **Body (optional):** A detailed description of what and why.
- **Footer (optional):** References to any related issues (e.g., "Fixes #123").

Example:

```
Improve token counting error handling

Added specific exception handling for tokenization errors to prevent crashes
when tiktoken encounters unexpected input. This fixes issue #45.
```

---

## License

By contributing to LLMify-Code, you agree that your contributions will be licensed under the project's [MIT License](LICENSE).

---

## Final Note

We appreciate your contributions and thank you for helping to make LLMify-Code better for everyone. If you have any questions or need guidance, please feel free to reach out via the issue tracker or contact the maintainers directly.

Happy coding!
