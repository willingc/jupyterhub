# -*- coding: utf-8 -*-
#
import sys
import os
import shlex

# For conversion from markdown to html
import recommonmark.parser

# Set paths
sys.path.insert(0, os.path.abspath('.'))

# -- General configuration ------------------------------------------------

# Minimal Sphinx version
needs_sphinx = '1.4'

# Sphinx extension modules
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.intersphinx',
    'sphinx.ext.napoleon',
    'autodoc_traits',
    'jupyter_alabaster_theme',
]

templates_path = ['_templates']

# The master toctree document.
master_doc = 'index'

# General information about the project.
project = u'JupyterHub'
copyright = u'2016, Project Jupyter team'
author = u'Project Jupyter team'

# Autopopulate version
from os.path import dirname
docs = dirname(dirname(__file__))
root = dirname(docs)
sys.path.insert(0, root)
sys.path.insert(0, os.path.join(docs, 'sphinxext'))

import jupyterhub
# The short X.Y version.
version = '%i.%i' % jupyterhub.version_info[:2]
# The full version, including alpha/beta/rc tags.
release = jupyterhub.__version__

language = None
exclude_patterns = []
pygments_style = 'sphinx'
todo_include_todos = False

# Set the default role so we can use `foo` instead of ``foo``
default_role = 'literal'

# -- Source -------------------------------------------------------------

source_parsers = {
    '.md': 'recommonmark.parser.CommonMarkParser',
}

source_suffix = ['.rst', '.md']

# -- Options for HTML output ----------------------------------------------

# The theme to use for HTML and HTML Help pages.
html_theme = 'jupyter_alabaster_theme'

# Paths that contain custom static files (such as style sheets)
html_static_path = ['_static']

htmlhelp_basename = 'JupyterHubdoc'

# -- Options for LaTeX output ---------------------------------------------

latex_elements = {
#'papersize': 'letterpaper',
#'pointsize': '10pt',
#'preamble': '',
#'figure_align': 'htbp',
}

# Grouping the document tree into LaTeX files. List of tuples
# (source start file, target name, title,
#  author, documentclass [howto, manual, or own class]).
latex_documents = [
  (master_doc, 'JupyterHub.tex', u'JupyterHub Documentation',
   u'Project Jupyter team', 'manual'),
]

# -- manual page output -------------------------------------------------

# One entry per manual page. List of tuples
# (source start file, name, description, authors, manual section).
man_pages = [
    (master_doc, 'jupyterhub', u'JupyterHub Documentation',
     [author], 1)
]

# -- Texinfo output -----------------------------------------------------

# Grouping the document tree into Texinfo files. List of tuples
# (source start file, target name, title, author,
#  dir menu entry, description, category)
texinfo_documents = [
  (master_doc, 'JupyterHub', u'JupyterHub Documentation',
   author, 'JupyterHub', 'One line description of project.',
   'Miscellaneous'),
]

# -- Epub output --------------------------------------------------------

# Bibliographic Dublin Core info.
epub_title = project
epub_author = author
epub_publisher = author
epub_copyright = copyright

# A list of files that should not be packed into the epub file.
epub_exclude_files = ['search.html']

# -- Intersphinx ----------------------------------------------------------

intersphinx_mapping = {'https://docs.python.org/3/': None}

# -- Read The Docs --------------------------------------------------------

on_rtd = os.environ.get('READTHEDOCS', None) == 'True'
if not on_rtd:
    import jupyter_alabaster_theme
    html_theme = 'jupyter_alabaster_theme'
    html_theme_path = [jupyter_alabaster_theme.get_path()]
else:
    import sphinx_rtd_theme
    html_theme = 'sphinx_rtd_theme'

