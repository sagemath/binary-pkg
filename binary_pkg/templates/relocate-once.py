#!/usr/bin/env python
"""
Rewrite Paths

This script can be used exactly once to move the directory to a
different location.
"""

import os, getopt, sys

def usage():
    print "relocate-once.py -d <destination>"
try:
    opts, args = getopt.getopt(sys.argv[1:], "hd:", ["help", "destination="])
except getopt.GetoptError:
    usage()
    sys.exit(2)
for opt, arg in opts:
    if opt in ('-h', '--help'):
        usage()
    elif opt in ('-d', '--destination'):
        ROOT_PATH = arg

try:
    ROOT_PATH
except NameError:
    ROOT_PATH = os.path.abspath(os.path.dirname(__file__))

{% include 'patch.py' %}

print("""
Rewriting paths for your new installation directory
===================================================

This might take a few minutes but only has to be done once.
""")
        
p = SearchAndReplace('{{search_string}}', ROOT_PATH)

{% for filename, patches in patches.items() %}
    {% if isinstance(patches, SearchReplacePatch) %}
p('{{filename}}').substitute().save()
    {% else %}
p('{{filename}}'){% for patch in patches %}.patch({{patch.start}}, {{patch.end}}){% endfor %}.save()
    {% endif %}
{% endfor %}

os.remove(__file__)


