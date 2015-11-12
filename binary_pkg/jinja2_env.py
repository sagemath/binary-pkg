"""
Jinja2 Environment For Generated Python
"""

import os

import logging
log = logging.getLogger()

from jinja2 import Environment, FileSystemLoader

jinja2_env = Environment(
    loader=FileSystemLoader([
        os.path.join(
            os.path.dirname(__file__),
            'templates',
        )
    ]),
    autoescape=True,
    trim_blocks=True,
    lstrip_blocks=True,
)
