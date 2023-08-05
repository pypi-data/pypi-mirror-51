""" DKIST Sphinx Theme """
import os

__version__ = "1.0.0"

import sphinx_bootstrap_theme


def get_html_theme_path():
    """Return list of HTML theme paths."""
    cur_dir = os.path.abspath(os.path.dirname(__file__))
    return [cur_dir] + sphinx_bootstrap_theme.get_html_theme_path()
