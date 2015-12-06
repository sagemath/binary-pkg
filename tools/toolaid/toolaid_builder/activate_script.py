
import os
import stat


TEMPLATE = """
#!/usr/bin/env bash

# This is the root dir
export REPO_ROOT_DIR="$(git rev-parse --show-toplevel)"
if [ ! -d "$REPO_ROOT_DIR/.git" ] ; then
    echo "Wrong directory? ($REPO_ROOT_DIR)"
    exit 1
fi

export PATH={config.target_directory}/bin:$PATH
export GEM_HOME={config.target_directory}
unset MAKE

if [ -n "$BASH" -o -n "$ZSH_VERSION" ] ; then
    hash -r 2>/dev/null
fi

if [ $# -ge 1 ] ; then
   "$@"
fi
"""



def write_activate_script(config):
    filename = os.path.join(config.target_directory, 'activate')
    script = TEMPLATE.format(config=config)
    with open(filename, 'wt') as f:
        f.write(script)
    os.chmod(filename, stat.S_IRWXU)
