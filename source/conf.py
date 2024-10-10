# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information
import sphinx_rtd_theme
project = 'CCI_OPEN5G'
copyright = '2024, Rajat Nagar'
author = 'Rajat Nagar'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = []

templates_path = ['_templates']
exclude_patterns = []



# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output


html_theme_options = {
'logo_only': True,
'style_nav_header_background': 'black',
'display_version': False,
}

html_theme = 'sphinx_rtd_theme'
html_logo = '_static/xG-rev-4c-01.png'
#make logo smaller
html_static_path = ['_static']
html_css_files = ['width.css']