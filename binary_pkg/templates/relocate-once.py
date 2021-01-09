#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Rewrite Paths

This script replaces incidences of the root path installed by buildbot with the
path to a symlink which points to the root of this installation.  The installation
is identified by a uuid created in this script, which runs only once because it
deletes itself upon successful completion.
"""

from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import os
import getopt
import sys
import uuid

buildbot_path = "{{search_string}}"

def usage():
    print("relocate-once.py -d<destination>")


try:
    opts, args = getopt.getopt(sys.argv[1:], "hd:", ["help", "destination="])
except getopt.GetoptError:
    usage()
    sys.exit(2)

ROOT_PATH = os.path.abspath(os.path.dirname(__file__))
DESTINATION = ""

for opt, arg in opts:
    if opt in ('-h', '--help'):
        usage()
        sys.exit(0)
    elif opt in ('-d', '--destination'):
        DESTINATION = arg


{% include 'patch.py' %}

if not DESTINATION:
    print("""
This appears to be a brand new Sage installation. Some configuration is needed
before it can be used.
""")
    # Generate an identifier for this Sage installation.
    install_uuid = uuid.uuid4().hex
    if os.geteuid() == 0:
        # Always make the installation public if Sage is being installed by root.
        DESTINATION = '/var/tmp/sage-%s'%install_uuid
    else:
        print("""
Normally Sage is installed for use by all users. In that case an administrator
password is needed to complete the configuration process. If you are not an
administrator for this system you may install a private version of Sage.
""")
        answer = None
        print("Would you like to create a private Sage installation?")
        try:
            while answer not in ("yes", "no"):
                answer = input("Please answer yes or no (or ^C to exit): ")
        except KeyboardInterrupt:
            sys.exit(3)
        if answer == "yes":
            print("Creating a private Sage installation for %s."%os.environ["USER"])
            home = os.getenv("HOME")
            if not home or not os.path.exists(home):
                print("No home directory!  Private installation is not possible.")
                sys.exit(1)
            dot_sage = os.path.join(home, '.sage')
            if not os.path.exists(dot_sage):
                os.mkdir(dot_sage, mode=0o700)
            locations = os.path.join(home, '.sage', 'locations')
            os.mkdir(locations, mode=0o755)
            DESTINATION = os.path.join(locations, install_uuid)
        else:
            DESTINATION = '/var/tmp/sage-%s'%install_uuid
    # Save the installation-specific symlink in a bash script which
    # can be sourced by the sage startup script.
    script_path = os.path.join(ROOT_PATH, "runpath.sh")
    with open(script_path, "w") as script:
        script.write('SAGE_SYMLINK="%s"\n'%DESTINATION)
    os.chmod(script_path, 0o755)
    # Create the symlink.
    os.symlink(ROOT_PATH, DESTINATION)

print("""
Configuring your new Sage installation
======================================

This might take a few minutes but only has to be done once.
""")

p = SearchAndReplace(ROOT_PATH, buildbot_path, DESTINATION)

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

# If we are being run as root, exit with status 2 as a signal to the sage
# script that it should exit, to avoid messing up the permissions on the
# user's .sage directory.
if os.geteuid() == 0:
    sys.exit(2)
