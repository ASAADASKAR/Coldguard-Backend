import os
import sys
import django

# Add project root to path so Sphinx can find Django apps
sys.path.insert(0, os.path.abspath('../..'))

# Configure Django settings
os.environ['DJANGO_SETTINGS_MODULE'] = 'coldguard.settings'
django.setup()

# -- Project information ──────────────────────────────
project = 'ColdGuard'
copyright = '2026, Asaad Askar'
author = 'Asaad Askar'
release = '1.0.0'

# -- General configuration ────────────────────────────
extensions = [
    'sphinx.ext.autodoc',   # reads docstrings automatically
    'sphinx.ext.viewcode',  # adds source code links
    'sphinx.ext.napoleon',  # supports Google style docstrings
]

templates_path = ['_templates']
exclude_patterns = []

# -- HTML output ──────────────────────────────────────
html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']