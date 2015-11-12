#!/usr/bin/env python

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


