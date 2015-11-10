
import os
from glob import glob


GITIGNORE_HEADER = """
# This file is generated automatically, do not edit

bootstrap/
""".lstrip()





def update_gitignore(tools_dir):
    tools_dir = os.path.abspath(tools_dir)
    gitignore = [GITIGNORE_HEADER]
    for yaml_file in sorted(glob(os.path.join(tools_dir, '*.yaml'))):
        directory = os.path.splitext(yaml_file)[0]
        name = os.path.basename(directory)        
        gitignore.append(name + '/')
    with open(os.path.join(tools_dir, '.gitignore'), 'wt') as f:
        f.write('\n'.join(gitignore))
        f.write('\n')
