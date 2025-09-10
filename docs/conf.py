# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options.
# See the full documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

import os
import sys
import datetime

# -- Path setup --------------------------------------------------------------

# Add the root of the project so autodoc can find your package
sys.path.insert(0, os.path.abspath(".."))

# -- Project information -----------------------------------------------------

project = "pesuacademy"
author = "Aditeya Baral and Samarth Mohan"
copyright = f"{datetime.datetime.now().year}, {author}"

try:
    import pesuacademy

    release = pesuacademy.__version__
except ImportError:
    release = "0.0.1"

# -- General configuration ---------------------------------------------------

# Sphinx extensions for enhanced documentation
extensions = [
    "sphinx.ext.autodoc",  # Automatically document code from docstrings
    "sphinx.ext.napoleon",  # Support Google style and NumPy style docstrings
    "sphinx.ext.viewcode",  # Add links to source code
    "sphinx.ext.intersphinx",  # Link to external docs (Python stdlib, requests, etc)
    "sphinx.ext.todo",  # Support for todo directives
    "sphinx.ext.coverage",  # Coverage report of documentation
    "sphinx.ext.githubpages",  # Add .nojekyll for GitHub Pages
    "sphinx_autodoc_typehints",  # Better display of Python type hints
]

# Templates path
# templates_path = ['_templates']

# Files and directories to exclude
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

# Show todos in the generated docs (turn off in production if desired)
todo_include_todos = False

# -- Options for HTML output -------------------------------------------------

html_theme = "sphinx_rtd_theme"  # ReadTheDocs theme, clean and widely used

# html_static_path = ['_static']   # For custom CSS/JS if needed

# Add custom CSS files here (optional)
# html_css_files = [
#     'css/custom.css',
# ]

# Show last updated timestamp on each page
html_last_updated_fmt = "%b %d, %Y"

html_theme_options = {
    "navigation_depth": 4,
    "collapse_navigation": False,
    "sticky_navigation": True,
}

# -- Intersphinx configuration -----------------------------------------------

# Link to other project docs for cross-references
intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None),
    "requests": ("https://requests.readthedocs.io/en/latest/", None),
    "pydantic": ("https://pydantic-docs.helpmanual.io/", None),
    "httpx": ("https://www.python-httpx.org/en/stable/", None),
    "beautifulsoup4": ("https://beautiful-soup-4.readthedocs.io/en/latest/", None),
    "selectolax": ("https://selectolax.readthedocs.io/en/latest/", None),
}

# -- Autodoc options ---------------------------------------------------------

autodoc_member_order = "bysource"  # Document members in the order they appear in source

autodoc_typehints = "description"  # Show type hints in descriptions, cleaner output

autodoc_default_options = {
    "members": True,
    "undoc-members": True,
    "show-inheritance": True,
    "inherited-members": True,
}

autodoc_typehints_format = "fully-qualified"

# -- Napoleon options --------------------------------------------------------

napoleon_google_docstring = True
napoleon_numpy_docstring = False
napoleon_include_init_with_doc = True
napoleon_include_private_with_doc = False
napoleon_include_special_with_doc = True
napoleon_use_admonition_for_examples = True
napoleon_use_param = True
napoleon_use_rtype = True
napoleon_attr_annotations = True

# -- Coverage options --------------------------------------------------------

coverage_show_missing_items = True

# -- Viewcode options --------------------------------------------------------

# Default behavior is fine (links to highlighted source)

# -- Additional options ------------------------------------------------------

# You can add custom substitutions or extensions here if needed


# -- End of conf.py -----------------------------------------------------------
