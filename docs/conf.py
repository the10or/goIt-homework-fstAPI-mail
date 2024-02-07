import os
import sys

sys.path.append(os.path.abspath('..'))

project = 'Contacts API'
copyright = '2024, the10or'
author = 'the10or'
release = '0.0.1'

extensions = ['sphinx.ext.autodoc']

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

html_theme = 'classic'
html_sidebars = {
    '**': [
        'localtoc.html',
        'sourcelink.html',
        'searchbox.html',
        'relations.html',
      ],
}
html_static_path = ['_static']
