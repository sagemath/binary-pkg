#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Rewrite Paths

This script can be used exactly once to move the directory to a
different location.
"""

from __future__ import (absolute_import, division, print_function, unicode_literals)

import os, getopt, sys

def usage():
    print("relocate-once.py -d <destination>")
    

try:
    opts, args = getopt.getopt(sys.argv[1:], "hd:", ["help", "destination="])
except getopt.GetoptError:
    usage()
    sys.exit(2)

    
ROOT_PATH = DESTINATION = os.path.abspath(os.path.dirname(__file__))
    
for opt, arg in opts:
    if opt in ('-h', '--help'):
        usage()
        sys.exit(0)
    elif opt in ('-d', '--destination'):
        DESTINATION = arg


{% include 'patch.py' %}

print("""
Rewriting paths for your new installation directory
===================================================

This might take a few minutes but only has to be done once.
""")
        
p = SearchAndReplace(ROOT_PATH, '{{search_string}}', DESTINATION)

{% for filename, patches in patches.items() %}
    {% if isinstance(patches, SearchReplacePatch) %}
p('{{filename}}').substitute().save()
    {% else %}
f = p('{{filename}}').binary()
        {% for patch in patches %}
f.patch({{patch.start}}, {{patch.end}})
        {% endfor %}
f.save()
    {% endif %}
{% endfor %}

os.remove(__file__)


