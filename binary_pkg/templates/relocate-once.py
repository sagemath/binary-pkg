#!/usr/bin/env python
"""
Rewrite Paths

This script can be used exactly once to move the directory to a
different location.
"""

import os

{% include 'patch.py' %}

        
p = SearchAndReplace('{{search_string}}', os.getcwd())

{% for filename, patches in patches.items() %}
    {% if isinstance(patches, SearchReplacePatch) %}
p('{{filename}}').substitute().save()
    {% else %}
p('{{filename}}'){% for patch in patches %}.patch({{patch.start}}, {{patch.end}}){% endfor %}.save()
    {% endif %}
{% endfor %}

os.remove(__file__)


