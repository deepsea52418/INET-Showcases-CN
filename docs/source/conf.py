# Configuration file for the Sphinx documentation builder.

# -- Project information
import sphinx_rtd_theme

project = 'INET Showcases CN'
copyright = '2024, Deepsea52418'
author = 'Deepsea52418, PrunierLiang'

release = '0.1'
version = '0.1.0'

# -- General configuration

extensions = [
    'sphinxnotes.strike',
    'sphinx.ext.graphviz',
    'sphinx.ext.duration',
    'sphinx.ext.doctest',
    'sphinx.ext.autodoc',
    'sphinx.ext.autosummary',
    'sphinx.ext.imgconverter',
    'sphinx.ext.intersphinx',
    'sphinxcontrib.video',
    'sphinxcontrib.youtube',
]

intersphinx_mapping = {
    'python': ('https://docs.python.org/3/', None),
    'sphinx': ('https://www.sphinx-doc.org/en/master/', None),
}
intersphinx_disabled_domains = ['std']

templates_path = ['_templates']

# -- Options for HTML output

html_theme = 'sphinx_rtd_theme'

# -- Options for EPUB output
epub_show_urls = 'footnote'
