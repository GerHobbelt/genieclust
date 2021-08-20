# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
# import os
# import sys
# sys.path.insert(0, os.path.abspath('.'))

import sys
import os
import sphinx_rtd_theme
import genieclust
import sphinx
import matplotlib.sphinxext
import IPython.sphinxext

# -- Project information -----------------------------------------------------

project = 'genieclust'
copyright = '2018-2021, Marek Gagolewski'
author = 'Marek Gagolewski'

# The full version, including alpha/beta/rc tags
version = genieclust.__version__
release = version

github_project_url = "https://github.com/gagolews/genieclust/"
html_baseurl = "https://genieclust.gagolewski.com/"

# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    'myst_parser',
    'matplotlib.sphinxext.plot_directive',
    'sphinx.ext.autodoc',
    'sphinx.ext.autosummary',
    'sphinx.ext.inheritance_diagram',
    'sphinx.ext.doctest',
    'sphinx.ext.todo',
    'sphinx.ext.coverage',
    'sphinx.ext.mathjax',
    'sphinxcontrib.bibtex',
    'sphinx_rtd_theme',
    'numpydoc'
    #'sphinx.ext.viewcode',
    #'sphinx.ext.imgmath',
    # 'sphinx.ext.napoleon',
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

todo_include_todos = True

source_suffix = ['.md', '.rst']

plot_include_source = True
plot_html_show_source_link = False
plot_pre_code = """
import numpy as np
import genieclust
import matplotlib.pyplot as plt
np.random.seed(123)
"""

# https://www.sphinx-doc.org/en/master/usage/extensions/autosummary.html
autosummary_imported_members = True
autosummary_generate = True

# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = 'sphinx_rtd_theme'

html_theme_options = {
    'prev_next_buttons_location': 'both',
    #'style_nav_header_background': '#ff704d',
    #'display_github': True,
    #'github_url': github_project_url,
}

html_theme_path = [sphinx_rtd_theme.get_html_theme_path()]
html_show_sourcelink = False

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']
html_css_files = ['css/custom.css']

numpydoc_use_plots = True


doctest_global_setup = plot_pre_code

pygments_style = 'colorful'

bibtex_bibfiles = ['bibliography.bib']
bibtex_default_style = 'alpha'
