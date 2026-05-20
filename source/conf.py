# Configuration file for the Sphinx documentation builder.

project = 'Sprawozdanie z laboratorium'
copyright = '2026, Gal 2'
author = 'Gal 2'
release = '0.0.1'

# General configuration
extensions = []  # ← USUŃ 'rst2pdf.pdfbuilder'

templates_path = ['_templates']
exclude_patterns = []
language = 'pl'

# HTML output
html_theme = 'alabaster'
html_static_path = ['_static']

# LaTeX output (dla make latexpdf)
latex_engine = 'pdflatex'
latex_elements = {
    'inputenc': r'\usepackage[utf8]{inputenc}',
    'fontenc': r'\usepackage[T1]{fontenc}',
    'babel': r'\usepackage[polish]{babel}',
    'preamble': r'''
        \usepackage{fncychap}
        \usepackage{wrapfig}
        \usepackage{enumitem}
    ''',
}