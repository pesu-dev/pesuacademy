# 🤝 Contributing to PESUAcademy

Thank you for your interest in contributing to PESUAcademy! This document will guide you through the process of setting up your environment and making your first contribution.

---

<details>
<summary>📚 Table of Contents</summary>

- [🤝 Contributing to PESUAcademy](#-contributing-to-PESUAcademy)
- [📜 Code of Conduct](#-code-of-conduct)
- [🚧 Getting Started](#-getting-started)
- [🛠️ Development Environment Setup](#-development-environment-setup)
  - [Prerequisites](#prerequisites)
  - [Installation Steps](#installation-steps)
  - [Set Up Environment Variables](#set-up-environment-variables)
- [🧪 Testing and Code Quality](#-testing-and-code-quality)
  - [Pre-commit Hooks](#pre-commit-hooks)
  - [Linting & Formatting](#linting--formatting)
- [🧪 Running Tests](#-running-tests)
  - [Writing Tests](#writing-tests)
- [🚀 Submitting Changes](#-submitting-changes)
  - [🔀 Create a Branch](#-create-a-branch)
  - [✏️ Make and Commit Changes](#️-make-and-commit-changes)
  - [📤 Push and Open a Pull Request](#-push-and-open-a-pull-request)
- [❓ Need Help?](#-need-help)
- [🔐 Security](#-security)
- [✨ Code Style Guide](#-code-style-guide)
  - [✅ General Guidelines](#-general-guidelines)
  - [📝 Docstrings & Comments](#-docstrings--comments)
- [🏷️ GitHub Labels](#%EF%B8%8F-github-labels)
- [🧩 Feature Suggestions](#-feature-suggestions)
- [📄 License](#-license)

</details>

---

## 🚧 Getting Started

We encourage developers to work on their own forks of the repository. This allows you to work on features or fixes witout affecting the main codebase until your changes are ready to be merged. We use a standard **fork-and-pull** workflow with a `dev` branch for staging changes.

### 🔄 Development Workflow

The standard workflow for contributing is as follows:

1. **Fork and Clone**: Fork the repository on GitHub and clone it to your local machine.
2. **Create a Branch**: Create a new branch from `dev` for your changes.
   - `git checkout dev`
   - `git pull origin dev`
   - `git checkout -b your-feature-name`
3. **Make Changes**: Implement your feature.
4. **Commit changes**: Commit your changes using the [Conventional Commits](https://www.conventionalcommits.org/) format.
5. **Push:** Push your branch to your forked repository.
6. **Create a Pull Request (PR)**: Open a PR from your branch to the `pesu-dev/pesuacademy:dev` branch (not `main`).
7. **Review**: Wait for feedback from maintainers. Address any requested changes.
8. **Merge**: Once approved, your changes will be merged into the `dev` branch and deployed to staging for testing.
9. After successful testing in staging, changes are promoted from `dev` to `main` for production deployment.

> [!NOTE]
> Please note that you will not be able to push directly to either the `dev` or `main` branches of the repository. All PRs must be raised from a feature branch of your forked repository and target the `dev` branch. **Direct PRs to `main` branch will be closed.**

---

## 🛠️ Development Environment Setup

A virtual environment is highly recommended to manage project dependencies.

### Prerequisites

- Python 3.11+
- Git

### Installation Steps

1. **Create and activate a virtual environment: (using `uv`)**

   ```bash
   uv venv
   source .venv/bin/activate
   ```

2. **Install dependencies:**
   ```bash
   uv sync --all-extras
   ```

### Set Up Environment Variables

> [!WARNING]
> Never commit your `.env` file to Git. It should only exist on your local machine. This project uses a `.env` file to manage credentials for both testing and general use. The `.gitignore` file is already configured to ignore `.env`, ensuring you never accidentally commit your secrets.

1. **Copy the example environment file to create your own:**

   ```bash
   cp .env.example .env
   ```

2. **Configure your credentials:**
   Open the `.env` file you just created. You will see two sections of variables.

   1. **Production Credentials (Production):**
      - These are the standard `PESU_USERNAME` and `PESU_PASSWORD` variables.
      - They are used when you run example scripts or use the library as an end-user would.
   2. **Test User Credentials (Development/Contributions) :**
      - These variables (all prefixed with `TEST_`) are **essential** for running the automated test suite (`pytest`).
      - Fill in all `TEST_...` variables with the details of a valid account.

## 🧪 Testing and Code Quality

We enforce code quality and correctness using `pre-commit`, which runs formatters, linters, upgrade checks, and the test suite automatically before every commit.

### Pre-commit Hooks

The following checks are enforced:

- ✅ `ruff` for linting and formatting (with auto-fix)
- ✅ `blacken-docs` to format code blocks inside Markdown files
- ✅ `pyupgrade` to upgrade syntax to Python 3.9+
- ✅ `end-of-file-fixer`, `trailing-whitespace`, `check-yaml`, `check-toml`, `requirements-txt-fixer` for formatting
- ✅ `name-tests-test` to enforce test naming conventions
- ✅ `debug-statements` to prevent committed `print()` or `pdb`
- ✅ A local `pytest` hook that runs the full test suite

Install the pre-commit hooks by running:

```bash
pre-commit install
```

> [!WARNING]
> You will not be able to commit code that fails these checks.

### Linting & Formatting

All linting and formatting is handled by `ruff`, `blacken-docs`, and `pyupgrade`. Run the following command to check all files:

```bash
pre-commit run --all-files
```

---

## 🧪 Running Tests

We use `pytest`, and a pre-commit hook ensures tests are run automatically before every commit.

To run tests manually:

```bash
pytest
```

To check coverage:

```bash
pytest --cov
```

> [!NOTE]
> The pre-commit hook runs `python scripts/run_tests.py`, which uses the same `pytest` runner.

### Writing Tests

- Write tests for all new features and bug fixes
- Place them in the `tests/` directory
- Name your test files and functions with the `test_` prefix (required by `pytest` and validated by pre-commit)
- Keep test cases small, meaningful, and well-named

---

## 🚀 Submitting Changes

### 🔀 Create a Branch

Start by creating a new branch for your work:

```bash
git checkout -b your-feature-name
```

Replace `your-feature-name` with a descriptive name related to the change (e.g., `fix-token-expiry-bug` or `docs-update-readme`).

### ✏️ Make and Commit Changes

After making your changes, commit them with a clear, conventional message:

```bash
git add .
git commit -m "fix: resolve token expiry issue"
```

Use [Conventional Commits](https://www.conventionalcommits.org/) to keep commit history consistent:

| Type        | Use for…                                       |
| ----------- | ---------------------------------------------- |
| `feat:`     | New features                                   |
| `fix:`      | Bug fixes                                      |
| `docs:`     | Documentation changes                          |
| `style:`    | Formatting (no code change)                    |
| `refactor:` | Code changes that aren't bug fixes or features |
| `test:`     | Adding or modifying tests                      |
| `chore:`    | Maintenance (build, deps, etc.)                |

### 📤 Push and Open a Pull Request

1. Push your branch to your fork:

   ```bash
   git push origin your-feature-name
   ```

2. Open a Pull Request (PR) on GitHub targeting the `dev` branch.

3. In your PR:

   - Use a clear and descriptive title
   - Include a summary of your changes
   - Link any related issues using `Closes #issue-number`
   - Add screenshots, terminal output, or examples if relevant

The maintainers will review your PR, provide feedback, and may request changes. Once approved, your PR will be merged into the `dev` branch and deployed to staging for testing. After successful validation, changes will be promoted to production.

---

## ❓ Need Help?

If you get stuck or have questions:

1. Check the [README.md](../README.md) for setup and usage info.
2. Review [open issues](https://github.com/pesu-dev/pesuacademy/issues) or [pull requests](https://github.com/pesu-dev/pesuacademy/pulls) to see if someone else encountered the same problem.
3. Reach out to the maintainers on [PESU Discord](https://discord.gg/eZ3uFs2).
   - Use the `#pesuacademy-py` channel for questions related to this repository.
   - Search for existing discussions before posting.
4. Open a new issue if you're facing something new or need clarification.

---

## 🔐 Security

If you discover a security vulnerability, **please do not open a public issue**.

Instead, report it privately by contacting the maintainers. We take all security concerns seriously and will respond promptly.

Read [SECURITY](SECURITY.md) for more information.

---

## ✨ Code Style Guide

To keep the codebase clean and maintainable, please follow these conventions:

### ✅ General Guidelines

- Write clean, readable code
- Use meaningful variable and function names
- Avoid large functions; keep logic modular and composable
- Use Python 3.11+ syntax when appropriate (e.g., `match`, `|` union types)
- Keep imports sorted and remove unused ones (handled automatically via `ruff`)

### 📝 Docstrings & Comments

- Add docstrings to all public functions, classes, and modules
- Use [Google-style docstrings](https://google.github.io/styleguide/pyguide.html#38-comments-and-docstrings).
- Write comments when logic is non-obvious and avoid restating the code

> [!IMPORTANT]
> Our official documentation on the website is automatically generated directly from these docstrings using Sphinx. Please write clear, complete, and user-friendly explanations, as they will be read by the library's users.

Example:

```python
async def get_profile(self) -> Profile:
   """Fetches the student's detailed profile information.

   Returns:
       Profile: A Pydantic model containing personal, parent, and address details.

   Example:
       >>> profile = await session.get_profile()
       >>> print(f"Name: {profile.student_details.name}")
   """
   ...
```

---

## 🏷️ GitHub Labels

We use GitHub labels to categorize issues and PRs. Here’s a quick guide to what they mean:

| Label              | Purpose                                         |
| ------------------ | ----------------------------------------------- |
| `good first issue` | Beginner-friendly, simple issues to get started |
| `bug`              | Something is broken or not working as intended  |
| `enhancement`      | Proposed improvements or new features           |
| `documentation`    | Docs, comments, or README-related updates       |
| `question`         | Open questions or clarifications                |
| `help wanted`      | Maintainers are seeking help or collaboration   |

When creating or working on an issue/PR, feel free to suggest an appropriate label if not already applied.

---

## 🧩 Feature Suggestions

If you want to propose a new feature:

1. Check if it already exists in [issues](https://github.com/pesu-dev/pesuacademy/issues)
2. Open a new issue using the **"Feature Request"** template if available
3. Clearly explain the use case, proposed solution, and any relevant context

---

## 📜 Code Of Conduct

All contributors are expected to read and adhere to our [Code of Conduct](../CODE_OF_CONDUCT.md). Please be respectful and professional in all interactions.

---

## 📄 License

By contributing to this repository, you agree that your contributions will be licensed under the **MIT License**.
See [LICENSE](../LICENSE) for full license text.
